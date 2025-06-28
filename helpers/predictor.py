from prophet import Prophet
import pandas as pd

def prepare_data(df):
    df = df.copy()
    df = df[df['Amount'] < 0]
    df['Amount'] = df['Amount'].abs()
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.groupby('Date')['Amount'].sum().reset_index()
    df = df.rename(columns={'Date': 'ds', 'Amount': 'y'})
    return df


def forecast_expenses(df, days=30):
    df_prepared = prepare_data(df)
    model = Prophet()
    model.fit(df_prepared)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], model
