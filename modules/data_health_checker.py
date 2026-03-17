import pandas as pd
def data_health_report(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data to analyse."
    lines  = []
    issues = 0
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        issues += 1
        lines.append(
            "Missing values: "
            + ", ".join(f"{col} ({n})" for col, n in missing.items())
        )
    dupes = df.duplicated().sum()
    if dupes:
        issues += 1
        lines.append(f"{dupes} duplicate rows detected.")
    for col in ["views", "likes", "comments", "shares", "duration_sec"]:
        if col in df.columns:
            neg = (df[col] < 0).sum()
            if neg:
                issues += 1
                lines.append(f"{neg} negative values in '{col}'.")
    if "sentiment_score" in df.columns:
        out_of_range = ((df["sentiment_score"] < -1) | (df["sentiment_score"] > 1)).sum()
        if out_of_range:
            issues += 1
            lines.append(f"{out_of_range} sentiment scores outside -1 to 1 range.")
    lines.append(f"Total rows analysed: {len(df):,}")
    if issues == 0:
        return "Data health looks good. " + lines[-1]
    return "\n".join(lines)