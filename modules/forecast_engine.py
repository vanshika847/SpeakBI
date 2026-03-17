import pandas as pd
def build_forecast(df: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    time_col = None
    for col in ["timestamp", "date"]:
        if col in df.columns:
            time_col = col
            break
    if not time_col or "views" not in df.columns:
        raise ValueError(
            "DataFrame must contain a timestamp/date column and 'views' column."
        )
    history = df[[time_col, "views"]].copy()
    history[time_col] = pd.to_datetime(history[time_col], errors="coerce")
    history = history.dropna(subset=[time_col, "views"])
    history = history.rename(columns={time_col: "ds", "views": "y"})
    if len(history) < 2:
        raise ValueError(
            "Not enough data points for forecasting. Need at least 2 rows."
        )
    try:
        from prophet import Prophet
        model    = Prophet(yearly_seasonality=True, weekly_seasonality=False)
        model.fit(history)
        future   = model.make_future_dataframe(periods=periods, freq="MS")
        forecast = model.predict(future)
        forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        forecast = forecast.rename(
            columns={"ds": "timestamp", "yhat": "views"}
        )
        return forecast
    except ImportError:
        raise ImportError("Prophet not installed. Run: pip install prophet")
