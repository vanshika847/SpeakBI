import pandas as pd
def generate_insights(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data available for insights."
    lines = []
    if "views" in df.columns:
        lines.append(f"Total views: {df['views'].sum():,.0f}")
    if "likes" in df.columns:
        lines.append(f"Total likes: {df['likes'].sum():,.0f}")
    if "comments" in df.columns:
        lines.append(f"Total comments: {df['comments'].sum():,.0f}")
    if "shares" in df.columns:
        lines.append(f"Total shares: {df['shares'].sum():,.0f}")
    if "sentiment_score" in df.columns:
        avg_sentiment = df["sentiment_score"].mean()
        mood = "Positive" if avg_sentiment > 0 else "Negative"
        lines.append(f"Average sentiment: {avg_sentiment:.3f} ({mood})")
    if "category" in df.columns and "views" in df.columns:
        by_cat = df.groupby("category")["views"].sum()
        if not by_cat.empty:
            lines.append(
                f"Top category: {by_cat.idxmax()} "
                f"({by_cat.max():,.0f} views)"
            )
            lines.append(
                f"Lowest category: {by_cat.idxmin()} "
                f"({by_cat.min():,.0f} views)"
            )
    if "region" in df.columns and "views" in df.columns:
        by_region = df.groupby("region")["views"].sum()
        if not by_region.empty:
            lines.append(
                f"Top region: {by_region.idxmax()} "
                f"({by_region.max():,.0f} views)"
            )
    if "likes" in df.columns and "views" in df.columns:
        total_views = df["views"].sum()
        total_likes = df["likes"].sum()
        if total_views:
            lines.append(
                f"Engagement rate: {total_likes / total_views:.2%}"
            )
    return "\n".join(lines) if lines else "Not enough columns for insights."
