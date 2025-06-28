import streamlit as st
import pandas as pd
import os
from helpers.categorizer import hybrid_categorize, rule_based_categorize, ml_categorize
from helpers.predictor import forecast_expenses
from helpers.suggestions import analyze_forecast
from visuals.charts import category_pie_chart, monthly_trend_line, top_expense_bar

st.set_page_config(page_title="FinWise - Personal Finance Assistant")
st.title("💸 FinWise - Personal Finance Dashboard")

# File Upload
st.header("Step 1: Upload Your Bank Statement")
file = st.file_uploader("Upload CSV or Excel File", type=['csv', 'xlsx'])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.success("File uploaded successfully!")
    st.subheader("Preview:")
    st.dataframe(df.head(), use_container_width=True)

    # Basic Cleaning
    st.header("Step 2: Clean & Prepare Data")
    df.columns = df.columns.str.strip().str.capitalize()

    if 'Date' in df.columns and 'Description' in df.columns and 'Amount' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)

        st.success("Date parsing complete. Data is ready!")

        # Categorization
        st.header("Step 3: Categorize Transactions")
        method = st.selectbox("Select Categorization Method", ["Hybrid", "ML", "Rule-Based"])

        if method == "ML":
            df["Category"] = df["Description"].apply(ml_categorize)
        elif method == "Rule-Based":
            df["Category"] = df["Description"].apply(rule_based_categorize)
        else:
            df["Category"] = df["Description"].apply(hybrid_categorize)

        st.dataframe(df.head(), use_container_width=True)

        # Visualizations
        st.header("Step 4: Visual Insights")
        expense_df = df[df["Amount"] < 0].copy()
        expense_df["Amount"] = expense_df["Amount"].abs()

        tab1, tab2, tab3 = st.tabs(["Pie Chart", "Monthly Trend", "Top Expenses"])

        with tab1:
            st.plotly_chart(category_pie_chart(expense_df), use_container_width=True)
        with tab2:
            st.plotly_chart(monthly_trend_line(expense_df), use_container_width=True)
        with tab3:
            st.plotly_chart(top_expense_bar(expense_df), use_container_width=True)

        # Forecasting
        st.header("Step 5: Forecast Future Spending")
        if st.button("Generate Forecast for Next 30 Days"):
            forecast_df, model = forecast_expenses(df)
            st.session_state.forecast_df = forecast_df
            st.session_state.model = model
            st.success("Forecast generated!")

        if "forecast_df" in st.session_state:
            forecast_df = st.session_state.forecast_df
            model = st.session_state.model

            st.subheader("📆 Forecast Table")
            st.dataframe(forecast_df.tail(30), use_container_width=True)

            from prophet.plot import plot_plotly
            st.subheader("📊 Forecast Chart")
            fig = plot_plotly(model, forecast_df)
            st.plotly_chart(fig, use_container_width=True)

            # Smart Suggestion
            st.subheader("💡 Smart Suggestion")
            tip, action = analyze_forecast(forecast_df, expense_df)
            st.markdown(f"**{tip}**")
            st.info(action)

            # Budget Goal
            st.header("Step 6: Budget Goal & Savings Tracker")
            budget = st.number_input("Set your Monthly Budget (₹)", min_value=0, value=20000, step=1000)

            forecasted_total = forecast_df.tail(30)["yhat"].sum()
            this_month = pd.Timestamp.now().strftime('%Y-%m')
            df["Amount"] = df["Amount"].astype(float)
            actual_monthly_total = df[df["Date"].dt.strftime('%Y-%m') == this_month]["Amount"].sum()

            remaining_budget = budget - forecasted_total

            if remaining_budget > 0:
                st.success(f"✅ You may save ₹{int(remaining_budget)} this month.")
            else:
                st.error(f"⚠️ Likely to overspend by ₹{int(abs(remaining_budget))}.")

            df_this_month = df[df["Date"].dt.strftime('%Y-%m') == this_month]
            df_this_month["Amount"] = df_this_month["Amount"].abs()
            top_cats = df_this_month.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3)

        # Export pdf
        st.header('Export your Report (optional)')

        if st.checkbox('I want to downlaod my forecast and budget summary'):
            import io

            if 'forecast_df' in st.session_state:
                forecast_df = st.session_state.forecast_df.copy()

                csv_buffer = io.StringIO()
                forecast_df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label='Download Forecast Report CSV',
                    data = csv_buffer.getvalue(),
                    file_name='forecast_report.csv',
                    mime='text/csv'
                )
                
                # Budget Summary Export
                import io

                this_month = pd.Timestamp.now().strftime('%Y-%m')
                forecasted_total = forecast_df.tail(30)["yhat"].sum()
                remaining_budget = budget - forecasted_total

                # Generate summary as plain text
                insight_text = f"""
                FinWise Budget Summary - {this_month}

                Monthly Budget Set: ₹{int(budget)}
                Forecasted Spending: ₹{int(forecasted_total)}
                Expected Balance: ₹{int(remaining_budget)}

                Suggestion:
                {'✅ Stay within your budget and save money!' if remaining_budget > 0 else '⚠️ You are likely to overspend. Consider reducing expenses.'}
                """

                # Download button
                st.download_button(
                    label="Download Budget Summary (TXT)",
                    data=insight_text,
                    file_name="budget_summary.txt",
                    mime="text/plain"
                )

        

    else:
        st.error("File must include 'Date', 'Description', and 'Amount' columns.")
