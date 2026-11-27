import os
import sqlite3
from contextlib import closing

import pandas as pd

DB_PATH = os.path.join("data", "soil.db")


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create the soil_records table if it does not exist."""
    with closing(get_connection()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS soil_records (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
                ph          REAL NOT NULL,
                moisture    REAL NOT NULL,
                density     REAL NOT NULL,
                organic     REAL NOT NULL,
                strength    TEXT NOT NULL,
                usage       TEXT NOT NULL,
                report      TEXT
            )
            """
        )
        conn.commit()


def insert_record(ph, moisture, density, organic, strength, usage, report=None):
    """Save one analysis (inputs + outputs). Returns the new record id."""
    with closing(get_connection()) as conn:
        cur = conn.execute(
            """
            INSERT INTO soil_records
                (ph, moisture, density, organic, strength, usage, report)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (ph, moisture, density, organic, strength, usage, report),
        )
        conn.commit()
        return cur.lastrowid


def update_report(record_id, report):
    """Attach the written report to an existing record."""
    with closing(get_connection()) as conn:
        conn.execute(
            "UPDATE soil_records SET report = ? WHERE id = ?",
            (report, record_id),
        )
        conn.commit()


def fetch_records():
    """Return all saved analyses as a DataFrame, newest first."""
    with closing(get_connection()) as conn:
        return pd.read_sql_query(
            "SELECT * FROM soil_records ORDER BY id DESC", conn
        )


def delete_record(record_id):
    with closing(get_connection()) as conn:
        conn.execute("DELETE FROM soil_records WHERE id = ?", (record_id,))
        conn.commit()