import sqlite3
import os
import time
import pandas as pd
def load_csv_to_sqlite(
    csv_path: str,
    db_path: str    = "database/database.db",
    table_name: str = "sales"
) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)
    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    # Parse timestamp column
    for col in df.columns:
        if "timestamp" in col or "date" in col or "time" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    # Ensure database folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with sqlite3.connect(db_path, timeout=10) as conn:
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                written_cols = [row[1] for row in cursor.fetchall()]
                print(f"[data_loader] Columns in DB: {written_cols}")
            break
        except sqlite3.OperationalError as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            raise
    return df