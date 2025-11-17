# src/create_tables.py
import sqlite3
from config import DB_PATH  # should point to db/crypto.db

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS symbols (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE,
                name TEXT,
                source_id TEXT,
                is_active INTEGER,
                market_cap REAL,
                volume_24h REAL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historical_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                last_price REAL,
                high_24h REAL,
                low_24h REAL,
                liquidity REAL,
                UNIQUE(symbol, date)
            )
        """)
        conn.commit()
        print("Tables created (or already existed)")
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()
