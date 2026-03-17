import sqlite3
import pandas as pd
def ensure_schema(
    db_path: str = "database/database.db",
    df: pd.DataFrame = None
):
    with sqlite3.connect(db_path) as conn:
        if df is not None:
            df.to_sql("sales", conn, if_exists="replace", index=False)
        else:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    timestamp      TEXT,
                    video_id       TEXT,
                    category       TEXT,
                    language       TEXT,
                    region         TEXT,
                    duration_sec   INTEGER,
                    views          INTEGER,
                    likes          INTEGER,
                    comments       INTEGER,
                    shares         INTEGER,
                    sentiment_score REAL,
                    ads_enabled    TEXT
                );
            """)
        conn.commit()
def get_schema_description(db_path: str = "database/database.db") -> str:
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(sales)")
            cols = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) FROM sales")
            row_count = cursor.fetchone()[0]
        col_names = [c[1] for c in cols]
        col_types = {c[1]: c[2] for c in cols}
        lines = [
            f"Table: sales ({row_count:,} rows)",
            f"Columns: {', '.join(col_names)}",
            "Column types:"
        ]
        for name, dtype in col_types.items():
            lines.append(f"  - {name}: {dtype}")
        return "\n".join(lines)
    except Exception as e:
        return f"Schema unavailable: {e}"