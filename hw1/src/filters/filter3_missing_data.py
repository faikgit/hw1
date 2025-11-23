# src/filters/filter3_missing_data.py
"""
Filter 3: Fill in missing historical data for each cryptocurrency.
"""
# src/filters/filter3_missing_data.py
import sys
import os

# Add src folder to sys.path so 'config' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
import sqlite3
from datetime import datetime, timedelta
from config import DB_PATH, COINGECKO_BASE, REQUEST_TIMEOUT, SLEEP_BETWEEN_REQUESTS, YEARS_BACK_DEFAULT, USER_AGENT

HEADERS = {"User-Agent": USER_AGENT}




# Ensure the db folder exists
db_folder = os.path.dirname(DB_PATH)
os.makedirs(db_folder, exist_ok=True)

# -------------------------------
# Database helpers
# -------------------------------

def create_tables_if_missing(db_path: str):
    conn = sqlite3.connect(db_path)
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
    finally:
        conn.close()

def get_all_symbols(db_path: str):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT symbol, source_id FROM symbols WHERE is_active=1")
        return cur.fetchall()  # list of tuples (symbol, source_id)
    finally:
        conn.close()

def get_last_saved_date(db_path: str, symbol: str):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT MAX(date) FROM historical_data WHERE symbol=?", (symbol,))
        row = cur.fetchone()
        if row and row[0]:
            return datetime.strptime(row[0], "%Y-%m-%d")
        else:
            return None
    finally:
        conn.close()

def insert_historical_data(db_path: str, symbol: str, data_list: list):
    if not data_list:
        return
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        for d in data_list:
            cur.execute("""
                INSERT OR IGNORE INTO historical_data
                (symbol, date, open, high, low, close, volume, last_price, high_24h, low_24h, liquidity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                symbol,
                d.get("date"),
                d.get("open"),
                d.get("high"),
                d.get("low"),
                d.get("close"),
                d.get("volume"),
                d.get("last_price"),
                d.get("high_24h"),
                d.get("low_24h"),
                d.get("liquidity")
            ))
        conn.commit()
    finally:
        conn.close()

# -------------------------------
# API / Data fetch
# -------------------------------

def fetch_historical_coingecko(symbol_id: str, start_date: datetime, end_date: datetime):
    """
    Fetch daily historical OHLCV from CoinGecko
    """
    days = (end_date - start_date).days
    # Limit to max 365 days to avoid CoinGecko errors
    days = min(days, 365)

    url = f"{COINGECKO_BASE}/coins/{symbol_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    result = resp.json()
    data_list = []
    # result contains 'prices', 'market_caps', 'total_volumes'
    prices = result.get("prices", [])
    volumes = result.get("total_volumes", [])
    for i in range(len(prices)):
        date_str = datetime.utcfromtimestamp(prices[i][0]/1000).strftime("%Y-%m-%d")
        data_list.append({
            "date": date_str,
            "open": prices[i][1],
            "high": prices[i][1],
            "low": prices[i][1],
            "close": prices[i][1],
            "volume": volumes[i][1] if i < len(volumes) else None,
            "last_price": prices[i][1],
            "high_24h": prices[i][1],
            "low_24h": prices[i][1],
            "liquidity": volumes[i][1] if i < len(volumes) else None
        })
    return data_list


# -------------------------------
# Main Filter 3 function
# -------------------------------

def run_filter3_missing_data(db_path: str):
    print("Filter3: ensure tables exist...")
    create_tables_if_missing(db_path)

    symbols = get_all_symbols(db_path)
    print(f"Filter3: found {len(symbols)} active symbols")

    for symbol, source_id in symbols:
        print(f"Filter3: processing {symbol} ({source_id})")
        last_date = get_last_saved_date(db_path, symbol)
        if last_date:
            start_date = last_date + timedelta(days=1)
        else:
            start_date = datetime.now() - timedelta(days=YEARS_BACK_DEFAULT*365)
        end_date = datetime.now()

        if start_date >= end_date:
            print(f"Filter3: {symbol} is already up to date")
            continue

        try:
            data_list = fetch_historical_coingecko(source_id, start_date, end_date)
            insert_historical_data(db_path, symbol, data_list)
            print(f"Filter3: {symbol} - inserted {len(data_list)} records")
        except Exception as e:
            print(f"Filter3: ERROR fetching data for {symbol}: {e}")
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print("Filter3: done.")

# -------------------------------
# Run filter if called directly
# -------------------------------

if __name__ == "__main__":
    run_filter3_missing_data(DB_PATH)
