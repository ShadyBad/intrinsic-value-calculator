# **Intrinsic Value Calculator**

## **Overview**
The **Intrinsic Value Calculator** is a Python-based tool that calculates the intrinsic value of stocks using the **Discounted Cash Flow (DCF) model**. It fetches real-time financial data from Yahoo Finance and risk-free rates from the **FRED API**, processes the data, and stores the results in **CSV** and **JSON** formats.

This project is designed for investors and analysts who want an automated method to determine whether a stock is undervalued or overvalued.

## **Features**
- ✅ **Fetches real-time stock data** (from Yahoo Finance API)
- ✅ **Uses Discounted Cash Flow (DCF) Model** for valuation
- ✅ **Batch processing** (Analyze multiple stocks at once)
- ✅ **Risk-free rate from FRED API** (for accurate discount rate calculations)
- ✅ **Saves results to CSV & JSON** (for easy tracking and analysis)
- ✅ **Parallel processing for efficiency** (faster data retrieval)
- ✅ **Handles missing or incomplete financial data gracefully**

---

## **Installation**
### **1️. Clone the Repository**
```sh
git clone https://github.com/your-username/Intrinsic-Value-Calculator.git
cd Intrinsic-Value-Calculator
```

### **2. Set Up a Virtual Environment (Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3️. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️. Set Up API Key for FRED**
1. Get a **FRED API key** from [FRED API](https://fred.stlouisfed.org/).
2. Create a `.env` file in the project directory and add:
```sh
FRED_API_KEY=your_fred_api_key_here
```

---

## **Usage**
### **Run the Script**
To analyze a single stock:
```sh
python intrinsic_value_calculator.py
```
Then, enter the stock ticker when prompted (e.g., `AAPL`).

To analyze multiple stocks in batch mode:
```sh
python intrinsic_value_calculator.py
```
Then, enter stock tickers separated by spaces (e.g., `AAPL MSFT TSLA`).

### **Example Output**
```
Analyzing AAPL...
Analyzing MSFT...
Batch processing complete. Data saved to CSV and JSON.
```

---

## **Output Data**
The program saves results in:
- `valuations.csv` – A CSV file storing stock valuations.
- `valuations.json` – A JSON file storing stock valuations.

Each entry includes:
- **Ticker Symbol**
- **Company Name**
- **Free Cash Flow (FCF)**
- **Current Market Price**
- **Intrinsic Value (DCF-Based)**
- **Last Updated Timestamp**

---

## **Future Enhancements**
- 🔹 **CLI Arguments** for specifying stock tickers and output formats.
- 🔹 **Automate Data Updates** using GitHub Actions.
- 🔹 **Stock Screening Feature** to list undervalued stocks.
- 🔹 **Interactive Visualization** using Streamlit or Plotly.

---

## **🤝 Contributing**
Contributions are welcome! If you find a bug or want to improve the project, feel free to open an **issue** or submit a **pull request**.
