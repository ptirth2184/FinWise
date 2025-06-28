import streamlit as st
import pandas as pd 




st.title('FinWise: Smart Expense Categorizer & Budget Planner')

uploaded_file = st.file_uploader('upload your CSV or Excel file', type=['csv', 'excel'])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success('File uploaded succesfully')
    st.subheader('🔍 Preview of Transactions')
    st.dataframe(df.head(10))

else:
    st.info('please upload a bank statement to continue')



# categorization
from helpers.categorizer import rule_based_categorize, ml_categorize, hybrid_categorize

method = st.selectbox("Categorization Method", ["Hybrid", "ML", "Rule-Based"])

# let user choose method
if method == "ML":
    df["Category"] = df["Description"].apply(ml_categorize)
elif method == "Rule-Based":
    df["Category"] = df["Description"].apply(rule_based_categorize)
else:
    df["Category"] = df["Description"].apply(hybrid_categorize)


# visulization
from visuals.charts import category_pie_chart, monthly_trend_line, top_expense_bar
st.header("Visual Insights")

# Filter only debit transactions (expenses)
expense_df = df[df['Amount']<0].copy()
expense_df['Amount'] = expense_df['Amount'].abs() #making it positive for chart

total_income = df[df['Type'] == 'Credit']['Amount'].sum()
total_expense = df[df['Type'] == 'Debit']['Amount'].sum()
total_expense = abs(total_expense)
savings = total_income - total_expense

st.subheader("💼 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Income", f"₹{total_income:,.0f}")
col2.metric("Expenses", f"₹{total_expense:,.0f}")
col3.metric("Savings", f"₹{savings:,.0f}")


tab1, tab2, tab3 = st.tabs(['Pie Chart', 'Trend Line', 'Top Expenses'])

with tab1:
    st.plotly_chart(category_pie_chart(expense_df), use_container_width=True)

with tab2:
    st.plotly_chart(monthly_trend_line(expense_df), use_container_width=True)

with tab3:
    st.plotly_chart(top_expense_bar(expense_df), use_container_width=True)


# Forcasting
from helpers.predictor import forecast_expenses

st.header("Forecast Your Future Expenses")

if st.button('Generate Forecast for next 30 days'):
    forecast_df, model = forecast_expenses(df)

    st.success('Forecast Generated!')
    st.subheader('Forecast table (next 30 days)')
    st.dataframe(forecast_df.tail(30), use_container_width=True)

    from prophet.plot import plot_plotly
    st.subheader('Expense Forecast Chart')
    fig = plot_plotly(model, forecast_df)
    st.plotly_chart(fig, use_container_width=True)


# Forecasting
from helpers.suggestions import analyze_forecast

# Prepare original expense data
expense_df = df[df["Amount"] < 0].copy()
expense_df["Amount"] = expense_df["Amount"].abs()

# Generate suggestions
tip, action = analyze_forecast(forecast_df, expense_df)

st.subheader("💡 Smart Suggestion")
st.markdown(f"**{tip}**")
st.info(action)
