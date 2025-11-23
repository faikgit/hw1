# 💹 CryptoScope – Data Ingestion Pipeline

This repository contains the **back-end data ingestion pipeline** for **CryptoScope**, a cryptocurrency analysis platform.  
The pipeline fetches **daily OHLCV (open, high, low, close, volume)** data for the **top 1000 active coins** and stores it in a local **SQLite database**.  
It is implemented in **Python** using asynchronous network requests and follows the **Pipe–and–Filter architectural style**.

---

## 🚀 Features

- **Automated Symbol Discovery** – retrieves the top N cryptocurrencies by market capitalisation using the [CryptoCompare API](https://www.cryptocompare.com/).  
- **Hybrid Data Sources** – downloads historical OHLCV data from **Binance** where available and falls back to **CryptoCompare** when a coin is not listed on Binance.  
- **Asynchronous I/O** – uses `asyncio` and `aiohttp` to perform many network requests concurrently, improving throughput.  
- **Incremental Updates** – fetches only missing data since the last stored date for each symbol.  
- **SQLite Storage** – saves data in a portable database suitable for later analysis or export.  

---

## 🧩 Prerequisites

CryptoScope is written in **Python 3** and requires the following package:

- `aiohttp`

### Install on macOS (recommended inside a virtual environment)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install aiohttp
⚙️ Configuration
The script uses environment variables to configure its behaviour:

Variable	Description	Default
CRYPTOCOMPARE_API_KEY	Required. API key for the CryptoCompare service. Obtain a free key at cryptocompare.com.	–
DB_PATH	Path to the SQLite database file.	crypto_data.db
TOP_N	Number of top coins to ingest.	1000
MAX_CONCURRENCY	Maximum number of concurrent HTTP requests.	5

Example setup
bash
Copy code
export CRYPTOCOMPARE_API_KEY=your_free_api_key
export MAX_CONCURRENCY=8
export TOP_N=1000
export DB_PATH=crypto_data.db
💡 On macOS (zsh), add these lines to your ~/.zshrc file to make them permanent.

▶️ Running the Pipeline
Activate your Python environment (optional but recommended):

bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
pip install aiohttp
Export your configuration variables:

bash
Copy code
export CRYPTOCOMPARE_API_KEY=your_free_api_key
export MAX_CONCURRENCY=8
export TOP_N=1000
export DB_PATH=crypto_data.db
Run the pipeline script:

bash
Copy code
python data_pipeline.py
The script will:

Create the database if it does not exist

Fetch the top coins

Download missing OHLCV data for each symbol

Print the total runtime upon completion

🕒 The first run may take a while depending on your network conditions.

🧠 Inspecting the Database (Optional)
You can explore the generated SQLite file using:

sqlite3 (CLI tool)

DB Browser for SQLite

Tables:

symbols — contains metadata for each cryptocurrency

ohlcv — stores daily OHLCV records

🍏 Notes for macOS Users
Ensure you are using the correct shell (bash or zsh).

To fix SSL certificate issues, run:

bash
Copy code
open /Applications/Python\ 3.x/Install\ Certificates.command
Use python3 if python points to Python 2.

🧭 Further Development
This repository covers only the data ingestion layer (Homework 1).
Future milestones will include:

Building a REST API to serve the stored data

Implementing a web front-end for charts and comparisons

Adding indicators and advanced analysis features

See the accompanying SRS document for a comprehensive description of project goals and requirements.
