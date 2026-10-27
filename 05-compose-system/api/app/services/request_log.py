"""Request log: one row per /predict call in a SQLite file (standard sqlite3)."""
import os
import sqlite3
from datetime import datetime

DB_PATH = os.getenv("LOG_DB", "logs/requests.db")


def init_db():
    # Create the parent folder and the table (only if they are missing)
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY, "
                 "time TEXT, question TEXT, answer TEXT, confidence REAL, "
                 "latency_ms REAL, status INTEGER)")
    conn.commit()
    conn.close()


def log_request(question, answer, confidence, latency_ms, status):
    # Open, insert one row, commit, close (simple, not fast)
    now = datetime.now().isoformat(timespec="seconds")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO requests (time, question, answer, confidence, "
                 "latency_ms, status) VALUES (?, ?, ?, ?, ?, ?)",
                 (now, question, answer, confidence, latency_ms, status))
    conn.commit()
    conn.close()


def recent(limit=10):
    # Newest rows first, as a list of dicts (ready to return as JSON)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM requests ORDER BY id DESC LIMIT ?",
                        (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]
