# src/config.py


# src/config.py
import os

# Get the absolute path to the hw1/db folder
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # parent of src/
DB_PATH = os.path.join(PROJECT_DIR, 'db', 'crypto.db')

# Make sure the folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

print(f"DB_PATH: {DB_PATH}")
print(f"Folder exists: {os.path.exists(os.path.dirname(DB_PATH))}")
print("Can write?", os.access(os.path.dirname(DB_PATH), os.W_OK))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/
DB_PATH = os.path.join(BASE_DIR, "../db/crypto.db")    # will create db in hw1/db/

# Path to SQLite DB (will be created if missing)
DB_PATH = "./db/crypto.db"   

# Data source configuration
DATA_SOURCE = "coingecko"
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

TOP_N_COINS = 1000

REQUEST_TIMEOUT = 15      # seconds
SLEEP_BETWEEN_REQUESTS = 10  # seconds; 

YEARS_BACK_DEFAULT = 10

USER_AGENT = "CryptoScope/1.0 (student project)"
