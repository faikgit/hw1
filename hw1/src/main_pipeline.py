# src/main_pipeline.py
"""
Main orchestrator for Homework 1 pipeline (Pipe & Filter).
Runs:
  - Filter 1: fetch & save top symbols
  - Filter 2: determine last stored date per symbol
  - Filter 3: fetch & insert missing OHLCV daily data
"""

import os
import time
import sqlite3
from datetime import datetime
from config import DB_PATH
from filters.filter1_symbols import run_filter1_symbols
from filters.filter2_last_date import get_symbols_with_last_date
from filters.filter3_missing_data import run_filter3_fill_missing

# SQL schema to create if DB doesn't exist
SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS symbols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    source_id TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    market_cap REAL,
    volume_24h REAL,
    UNIQUE(symbol, source_id)
);

CREATE TABLE IF NOT EXISTS daily_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol_id INTEGER NOT NULL,
    date TEXT NOT NULL,          -- 'YYYY-MM-DD'
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    last_price_24h REAL,
    high_24h REAL,
    low_24h REAL,
    volume_24h REAL,
    liquidity REAL,
    source TEXT,
    UNIQUE(symbol_id, date),
    FOREIGN KEY(symbol_id) REFERENCES symbols(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_daily_prices_symbol_date ON daily_prices(symbol_id, date);
"""

def ensure_db_exists(db_path: str):
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()

def main():
    print("=== CryptoScope Homework 1 Pipeline ===")
    print(f"DB: {DB_PATH}")
    ensure_db_exists(DB_PATH)

    total_start = time.time()

    # Filter 1: fetch and store symbols
    t0 = time.time()
    print("\n--- Running Filter 1: Fetch & store top symbols ---")
    run_filter1_symbols(db_path=DB_PATH)
    print(f"Filter1 completed in {time.time() - t0:.2f}s")

    # Filter 2: get symbols with last_date
    t1 = time.time()
    print("\n--- Running Filter 2: Determine last saved dates ---")
    symbols_info = get_symbols_with_last_date(db_path=DB_PATH)
    print(f"Found {len(symbols_info)} symbols in DB.")
    print(f"Filter2 completed in {time.time() - t1:.2f}s")

    # Filter 3: fill missing data
    t2 = time.time()
    print("\n--- Running Filter 3: Download & insert missing historical data ---")
    run_filter3_fill_missing(symbols_info=symbols_info, db_path=DB_PATH)
    print(f"Filter3 completed in {time.time() - t2:.2f}s")

    total_end = time.time()
    print("\n=== Pipeline finished ===")
    print(f"Total duration: {total_end - total_start:.2f} seconds")

if __name__ == "__main__":
    main()
