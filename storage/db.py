import sqlite3
from datetime import datetime
from typing import List, Tuple

DB_PATH = "data/market_data.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def initialize_db():
    """
    Create required tables and indexes if they do not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            price REAL NOT NULL,
            quantity REAL NOT NULL,
            ingestion_time TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_ticks_symbol_time
        ON ticks (symbol, timestamp);
    """)

    conn.commit()
    conn.close()


def insert_tick(symbol: str, timestamp: str, price: float, quantity: float):
    """
    Insert a single tick into the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ticks (symbol, timestamp, price, quantity, ingestion_time)
        VALUES (?, ?, ?, ?, ?);
    """, (
        symbol,
        timestamp,
        price,
        quantity,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def fetch_ticks(
    symbol: str,
    start_time: str = None,
    end_time: str = None
) -> List[Tuple]:
    """
    Fetch ticks for a given symbol and optional time range.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT timestamp, price, quantity
        FROM ticks
        WHERE symbol = ?
    """
    params = [symbol]

    if start_time:
        query += " AND timestamp >= ?"
        params.append(start_time)

    if end_time:
        query += " AND timestamp <= ?"
        params.append(end_time)

    query += " ORDER BY timestamp ASC;"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()
    return rows
