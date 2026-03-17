import pandas as pd
def select_chart(intent: dict, df: pd.DataFrame = None) -> dict:
    group_by        = intent.get("group_by", [])
    intent_type     = intent.get("intent", "summary")
    forecast_months = intent.get("forecast_months", 0)
    cols            = list(df.columns) if df is not None else []
    if forecast_months and forecast_months > 0:
        return {"type": "forecast", "x": "timestamp", "y": "views"}
    if "timestamp" in group_by:
        color = None
        if "category" in group_by:
            color = "category"
        elif "region" in group_by:
            color = "region"
        return {
            "type": "line",
            "x": "timestamp",
            "y": _best_y(cols),
            "color": color
        }
    if "category" in group_by and "region" not in group_by:
        return {
            "type": "bar",
            "x": "category",
            "y": _best_y(cols),
            "color": None
        }
    if "region" in group_by and "category" not in group_by:
        return {
            "type": "bar",
            "x": "region",
            "y": _best_y(cols),
            "color": None
        }
    if "region" in group_by and "category" in group_by:
        return {
            "type": "bar",
            "x": "region",
            "y": _best_y(cols),
            "color": "category"
        }
    if "language" in group_by:
        return {
            "type": "bar",
            "x": "language",
            "y": _best_y(cols),
            "color": None
        }
    if "ads_enabled" in group_by:
        return {
            "type": "pie",
            "x": "ads_enabled",
            "y": _best_y(cols),
            "color": None
        }
    if df is not None and len(df) <= 8 and intent_type == "breakdown":
        x = group_by[0] if group_by else (cols[0] if cols else "category")
        return {"type": "pie", "x": x, "y": _best_y(cols), "color": None}
    x = group_by[0] if group_by else (cols[0] if cols else "category")
    return {"type": "bar", "x": x, "y": _best_y(cols), "color": None}
def _best_y(cols: list) -> str:
    for preferred in ["views", "likes", "comments", "shares",
                      "sentiment_score", "duration_sec"]:
        if preferred in cols:
            return preferred
    return cols[-1] if cols else "views"