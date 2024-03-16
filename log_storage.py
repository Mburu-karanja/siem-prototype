import sqlite3
import pandas as pd

def create_database(db_name="system_logs.db"):
    """Creates a SQLite database for storing parsed logs (modify table schema as needed)."""

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logs (timestamp DATETIME, facility TEXT, level TEXT, message TEXT)")
    conn.commit()
    conn.close()

def store_logs(logs_df, db_name="system_logs.db"):
    """Stores parsed logs in the SQLite database."""

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for index, row in logs_df.iterrows():
        c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", row.to_list())

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    logs_df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-03-16 19:37:00"]),
        "facility": ["user"],
        "level": ["INFO"],
        "message": ["This is an informational message."]
    })
    store_logs(logs_df)
