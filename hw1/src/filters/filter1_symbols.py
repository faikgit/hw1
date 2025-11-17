# src/filters/filter1_symbols.py
"""
Filter 1: fetch top N active symbols from CoinGecko, filter invalids, store in DB.
"""
import sys
import os
import time
import requests
import sqlite3
from datetime import datetime

# Add src folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import config
from config import COINGECKO_BASE, TOP_N_COINS, REQUEST_TIMEOUT, SLEEP_BETWEEN_REQUESTS, USER_AGENT

HEADERS = {"User-Agent": USER_AGENT}

# -------------------------------
# Helper functions
# -------------------------------

def fetch_top_coins_coingecko(top_n=TOP_N_COINS):
    """
    Use CoinGecko /coins/markets endpoint to fetch coins by market cap desc.
    CoinGecko supports pagination (per_page max 250).
    Returns list of coin dicts (as returned by CoinGecko).
    """
    coins = []
    per_page = 250
    page = 1
    while len(coins) < top_n:
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": "false"
        }
        url = f"{COINGECKO_BASE}/coins/markets"
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            page_coins = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        if not page_coins:
            break
        coins.extend(page_coins)
        print(f"Fetched page {page}, got {len(page_coins)} coins (total {len(coins)})")
        page += 1
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return coins[:top_n]

def is_valid_coin_entry(c):
    """
    Basic validation rules:
    - must have id, symbol, name
    - must have market_cap and total_volume fields
    - filter extreme low-volume coins
    """
    if not c.get("id") or not c.get("symbol") or not c.get("name"):
        return False
    if c.get("market_cap") is None or c.get("total_volume") is None:
        return False
    if c.get("total_volume", 0) < 1000:  # low liquidity filter
        return False
    return True

def init_db(db_path: str):
    """
    Create database and symbols table if they don't exist
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS symbols (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            source_id TEXT,
            is_active INTEGER,
            market_cap REAL,
            volume_24h REAL
        )
        """)
        conn.commit()
    finally:
        conn.close()

def insert_symbols_into_db(db_path: str, cleaned):
    """
    Insert cleaned symbols into the database
    """
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        for s in cleaned:
            cur.execute("""
                INSERT OR IGNORE INTO symbols
                (symbol, name, source_id, is_active, market_cap, volume_24h)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (s["symbol"], s["name"], s["source_id"], 1, s.get("market_cap"), s.get("volume_24h")))
        conn.commit()
    finally:
        conn.close()

# -------------------------------
# Main function
# -------------------------------

def run_filter1_symbols(db_path: str):
    print("Filter1: initializing database...")
    init_db(db_path)

    print(f"Filter1: fetching top {TOP_N_COINS} coins from CoinGecko...")
    raw = fetch_top_coins_coingecko()
    print(f"Filter1: total fetched {len(raw)} entries")

    cleaned = []
    for c in raw:
        if not is_valid_coin_entry(c):
            continue
        cleaned.append({
            "symbol": (c["symbol"] or "").upper(),
            "name": c["name"],
            "source_id": c["id"],        # e.g., 'bitcoin'
            "market_cap": c.get("market_cap"),
            "volume_24h": c.get("total_volume")
        })

    print(f"Filter1: after cleaning -> {len(cleaned)} symbols")
    print("Filter1: inserting into DB...")
    insert_symbols_into_db(db_path, cleaned)
    print("Filter1: done.")

# -------------------------------
# Run as script
# -------------------------------

if __name__ == "__main__":
    # Default database path relative to src/
    from config import DB_PATH
    run_filter1_symbols(DB_PATH)
