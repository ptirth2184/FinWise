import pandas as pd

def analyze_forecast(forecast_df, current_df):
    future_sum = forecast_df.tail(30)['yhat'].sum()
    past_sum = current_df['Amount'].sum()

    percent_change = ((future_sum - abs(past_sum)) / abs(past_sum))*100
    
    if percent_change > 20:
        tip = "⚠️ Your spending is expected to increase by {:.1f}% next month.".format(percent_change)
        action = "Consider reducing discretionary expenses like Food, Shopping, or Entertainment."

    elif percent_change < -10:
        tip = "✅ Great! You're expected to spend {:.1f}% less next month.".format(abs(percent_change))
        action = "Keep up the good habits. Consider saving or investing the surplus."

    else:
        tip = "📊 Your spending is likely to remain stable (±10%)."
        action = "Keep tracking and reviewing your budget to stay consistent."

    return tip, action
