import streamlit as st
import pandas as pd 
from helpers.categorizer import rule_based_categorize, ml_categorize, hybrid_categorize
from visuals.charts import category_pie_chart, monthly_trend_line, top_expense_bar

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
method = st.selectbox("Categorization Method", ["Hybrid", "ML", "Rule-Based"])

# let user choose method
if method == "ML":
    df["Category"] = df["Description"].apply(ml_categorize)
elif method == "Rule-Based":
    df["Category"] = df["Description"].apply(rule_based_categorize)
else:
    df["Category"] = df["Description"].apply(hybrid_categorize)


# visulization
st.header("📈 Visual Insights")

# Filter only debit transactions (expenses)
expense_df = df[df['Amount']<0].copy()
expense_df['Amount'] = expense_df['Amount'].abs() #making it positive for chart

tab1, tab2, tab3 = st.tabs(['Pie Chart', 'Trend Line', 'Top Expenses'])

with tab1:
    st.plotly_chart(category_pie_chart(expense_df), use_container_width=True)

with tab2:
    st.plotly_chart(monthly_trend_line(expense_df), use_container_width=True)

with tab3:
    st.plotly_chart(top_expense_bar(expense_df), use_container_width=True)