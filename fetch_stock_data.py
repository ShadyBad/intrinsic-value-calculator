import os
import yfinance as yf
import pandas as pd
import csv
import json
import logging
from dotenv import load_dotenv
from fredapi import Fred
from datetime import datetime
from multiprocessing import Pool, cpu_count

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")
fred = Fred(api_key=FRED_API_KEY)

def get_risk_free_rate():
    """Fetches the latest 10-Year Treasury Yield from FRED."""
    try:
        risk_free_rate = fred.get_series_latest_release("DGS10")
        return risk_free_rate.iloc[-1] / 100 if isinstance(risk_free_rate, pd.Series) else 0.04
    except Exception as e:
        logging.error(f"Error fetching risk-free rate from FRED: {e}")
        return 0.04  # Default to 4%

def extract_key_metrics(ticker):
    """Extracts key financial metrics from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    try:
        income_statement = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        history = stock.history(period="1y")
        
        current_price = history["Close"].iloc[-1] if not history.empty else stock.info.get("previousClose", None)
        company_name = stock.info.get("shortName", "Unknown")
        
        avg_fcf = (
            cash_flow.loc["Operating Cash Flow"].iloc[:5].mean() -
            cash_flow.loc["Capital Expenditure"].iloc[:5].mean()
        ) if "Operating Cash Flow" in cash_flow.index and "Capital Expenditure" in cash_flow.index else None
        
        return {
            "Ticker": ticker,
            "Company Name": company_name,
            "Free Cash Flow": avg_fcf,
            "Current Price": current_price,
            "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logging.error(f"Error retrieving data for {ticker}: {e}")
        return None

def save_to_csv(filename, data):
    """Saves or updates stock data in a CSV file."""
    file_exists = os.path.isfile(filename)
    fieldnames = ["Ticker", "Company Name", "Free Cash Flow", "Current Price", "DCF Intrinsic Value", "Last Updated"]
    
    try:
        with open(filename, mode="a" if file_exists else "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        logging.info(f"Data saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving data to {filename}: {e}")

def save_to_json(filename, data):
    """Saves or updates stock data in a JSON file."""
    try:
        json_data = []
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    json_data = json.load(file)
                except json.JSONDecodeError:
                    pass
        json_data.append(data)
        with open(filename, "w") as file:
            json.dump(json_data, file, indent=4)
        logging.info(f"Data saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving data to {filename}: {e}")

def process_stock(ticker):
    """Processes a single stock."""
    logging.info(f"Analyzing {ticker}...")
    metrics = extract_key_metrics(ticker)
    if not metrics:
        logging.warning(f"Skipping {ticker} due to missing data.")
        return None
    
    risk_free_rate = get_risk_free_rate()
    dcf_value = metrics.get("Free Cash Flow") * 10 if metrics.get("Free Cash Flow") else None  # Simplified DCF estimation
    metrics["DCF Intrinsic Value"] = dcf_value
    
    save_to_csv("valuations.csv", metrics)
    save_to_json("valuations.json", metrics)
    
    return metrics

if __name__ == "__main__":
    user_input = input("Enter stock ticker(s) separated by spaces: ").strip().upper()
    tickers = user_input.split()
    if not tickers:
        logging.error("No stock tickers provided. Exiting.")
        exit()
    
    with Pool(processes=min(len(tickers), cpu_count())) as pool:
        pool.map(process_stock, tickers)
    
    logging.info("Batch processing complete. Data saved to CSV and JSON.")