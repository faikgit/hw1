# src/filters/filter2_last_date.py
"""
Filter 2: For each symbol in DB, determine the last saved date.
Returns a list of dicts:
  { symbol_id, symbol, source_id, last_date }  where last_date is 'YYYY-MM-DD' or None
"""

import sqlite3

def get_symbols_with_last_date(db_path: str):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, s.symbol, s.source_id, MAX(dp.date) as last_date
            FROM symbols s
            LEFT JOIN daily_prices dp ON dp.symbol_id = s.id
            GROUP BY s.id, s.symbol, s.source_id
            ORDER BY s.market_cap DESC NULLS LAST
        """)
        rows = cur.fetchall()
        result = []
        for r in rows:
            symbol_id, symbol, source_id, last_date = r
            result.append({
                "symbol_id": symbol_id,
                "symbol": symbol,
                "source_id": source_id,
                "last_date": last_date  # may be None
            })
        return result
    finally:
        conn.close()
