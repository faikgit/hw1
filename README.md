# hw1
Homework 1 – Crypto Exchange Analytics Platform
This repository contains the files and code for the first homework assignment in the Software Design and Architecture course.
The assignment requires building a data ingestion pipeline and documenting the overall project.
The project focuses on analysing historical cryptocurrency data using the pipe‑and‑filter architecture style.
Contents
project_description.md – A one‑page overview of the entire semester project, including objectives, data sources, chosen technologies, and expected outcomes.
requirements_specification.md – A comprehensive specification of functional and non‑functional requirements (5‑10 pages) with user personas and scenarios.
data_pipeline.py – Python code implementing the pipe‑and‑filter data ingestion pipeline. The script retrieves the top 1 000 cryptocurrency symbols, determines the last saved date for each symbol and downloads missing OHLCV data.
crypto_data.db (created at runtime) – SQLite database storing symbol metadata and historical OHLCV data.
Setup and Usage
Prerequisites
Python 3.10+ (tested with Python 3.11)
aiohttp
 for asynchronous HTTP requests
ccxt
 (optional) for direct exchange access
pandas (optional) for analysis and CSV export
Install dependencies using pip:
pip install aiohttp ccxt pandas
Running the Pipeline
Navigate to the Homework 1 directory.
Run the pipeline:
python data_pipeline.py

The script will initialise the SQLite database (crypto_data.db by default), fetch the list of the top 1 000 coins from CoinGecko,
check the database for existing data and download missing data. 
Data are inserted into the ohlcv table and can be queried with SQL or exported to CSV using a tool of your choice.
To change the database file location or other parameters, set environment variables:
CRYPTO_DB_PATH – Path to the SQLite database. Default is crypto_data.db.
TOP_N – Number of coins to fetch (default 1000). Modify the constant in data_pipeline.py if needed.

Notes
The script uses the public CoinGecko API and may be subject to rate limits. If you encounter HTTP 429 (Too Many Requests) errors, 
reduce the concurrency limit (semaphore in run_pipeline) or add delays between requests.
The current implementation assigns the closing price to open/high/low values for daily data because CoinGecko’s market_chart endpoint does not provide OHLC data. 
For more accurate OHLCV data, consider using the ccxt library to fetch data directly from exchanges like Binance or Kraken.
Data collected through free APIs should not be redistributed commercially without permission. Review the terms of service of the data providers.

Database Schema
Table	Purpose	Key columns
symbols	Metadata about each coin	symbol (primary key), name, market_cap_rank
ohlcv	Daily OHLCV market data	symbol, timestamp, open, high, low, close, volume, market_cap, exchange
