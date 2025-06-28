import streamlit as st
import pandas as pd 

st.title('FinWise: Smart Expense Categorizer & Budget Planner')

st.header('step1: Upload your bank statement')
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