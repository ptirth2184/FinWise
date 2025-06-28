import plotly.express as px
import pandas as pd

def category_pie_chart(df: pd.DataFrame):
    fig = px.pie(df, names='Category', values='Amount', title='Expenses by Category')
    return fig

def monthly_trend_line(df):
    df.columns = df.columns.astype(str).str.strip()
    df = df.dropna(subset=['Date'])
    df['Month'] = pd.to_datetime(df['Date'], errors='coerce').dt.to_period('M').astype(str)
    df = df.dropna(subset=['Month'])
    monthly_data = df.groupby('Month')['Amount'].sum().reset_index()
    fig = px.line(monthly_data, x='Month', y='Amount', title='Monthly Spending Trend')
    return fig


def top_expense_bar(df: pd.DataFrame):
    top_txns = df.sort_values('Amount', ascending=False).head(5)
    fig = px.bar(top_txns, x='Description', y='Amount', title='Top 5 Expenses', text='Amount')
    return fig
