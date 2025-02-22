from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import re
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Regex for validating ticker format
TICKER_PATTERN = re.compile(r'^[A-Z]{1,5}\d{6}[CP]\d{5,8}$')

def is_valid_ticker(ticker):
    return bool(TICKER_PATTERN.match(ticker))

def fetch_option_data(ticker):
    try:
        stock_symbol = ticker[:-15]
        stock = yf.Ticker(stock_symbol)

        print(f"📌 Fetching data for stock: {stock_symbol}")

        # Get the most recent stock prices
        stock_history = stock.history(period="30d")
        if stock_history.empty:
            return {"error": "No stock price data available."}

        stock_prices = stock_history['Close'].dropna().tolist()

        # Fetch option expiration dates
        expiration_dates = stock.options
        if not expiration_dates:
            print("❌ No expiration dates found!")
            return {"error": "No expiration dates available."}

        print(f"✅ Expiration dates available: {expiration_dates}")

        # Fetch the first available option chain
        option_chain = stock.option_chain(expiration_dates[0])
        calls, puts = option_chain.calls, option_chain.puts

        if calls.empty or puts.empty:
            print("❌ No option data found!")
            return {"error": "No option data found."}

        # Sort option data by strike price (ascending)
        calls = calls.sort_values(by="strike")
        puts = puts.sort_values(by="strike")

        call_prices = calls['lastPrice'].dropna().tolist()
        put_prices = puts['lastPrice'].dropna().tolist()

        # **Ensure Equal Lengths**
        min_length = min(len(stock_prices), len(call_prices), len(put_prices))

        stock_prices = stock_prices[:min_length]
        call_prices = call_prices[:min_length]
        put_prices = put_prices[:min_length]

        # **Sort Data by Stock Prices (X-axis left to right)**
        sorted_indices = np.argsort(stock_prices)
        stock_prices = np.array(stock_prices)[sorted_indices].tolist()
        call_prices = np.array(call_prices)[sorted_indices].tolist()
        put_prices = np.array(put_prices)[sorted_indices].tolist()

        # **Truncate Stock Prices to Two Decimal Places for Display**
        display_stock_prices = [f"{x:.2f}" for x in stock_prices]

        # 🔍 DEBUGGING: Print Data to Verify Alignment
        print(f"📊 Sorted Stock Prices (Displayed): {display_stock_prices}")
        print(f"📈 Call Prices (Sorted): {call_prices}")
        print(f"📉 Put Prices (Sorted): {put_prices}")

        print("✅ Successfully fetched, sorted & truncated option & stock data!")
        return {
            "stock_prices": stock_prices,
            "display_stock_prices": display_stock_prices,  # Send formatted values for display
            "call_prices": call_prices,
            "put_prices": put_prices
        }

    except Exception as e:
        print(f"❌ Error in fetch_option_data: {str(e)}")
        return {"error": str(e)}

@app.route('/get-option-data', methods=['GET'])
def get_option_data():
    ticker = request.args.get('ticker')

    print(f"📌 Received request for ticker: {ticker}")

    if not ticker or not is_valid_ticker(ticker):
        print("❌ Invalid ticker format!")
        return jsonify({"error": "Invalid ticker format."}), 400

    data = fetch_option_data(ticker)

    print(f"✅ Returning API response: {data}")

    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")  # Enable CORS
    return response

if __name__ == '__main__':
    app.run(debug=True)