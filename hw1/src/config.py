# src/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/
DB_PATH = os.path.join(BASE_DIR, "../db/crypto.db")    # will create db in hw1/db/

# Path to SQLite DB (will be created if missing)
DB_PATH = "../db/crypto.db"   # relative to src/ (adjust if you run from a different cwd)

# Data source configuration
DATA_SOURCE = "coingecko"
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

# How many top coins to fetch
TOP_N_COINS = 1000

# Some basic rate-limit friendly settings
REQUEST_TIMEOUT = 15      # seconds
SLEEP_BETWEEN_REQUESTS = 10  # seconds; increase if you get rate-limited

# For the initial-download behavior: how many years back if API allows
YEARS_BACK_DEFAULT = 10

# Useful user-agent for polite requests
USER_AGENT = "CryptoScope/1.0 (student project)"
