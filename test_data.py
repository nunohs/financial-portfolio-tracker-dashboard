import yfinance as yf  #library that talks to Yahoo Finance
import requests        #lets Python make web requests (like a browser)

# Test stock data, Apple, Microsoft, Tesla
stock_tickers = ["AAPL", "MSFT", "TSLA"]

print("STOCK DATA")
for ticker in stock_tickers:
    stock = yf.Ticker(ticker) # Object that represents a stock, "Connection to Apple's data"
    price = stock.history(period="1d")["Close"].iloc[-1] #Gets historical data for the last 1 day, gets the latest closing price, 
    print(f"{ticker}: ${price:.2f}")

#Test crypto data from CoinGecko
print("\nCRYPTO DATA")

url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin, ethereum, solana",
    "vs_currencies": "usd"
    }

response = requests.get(url, params=params) 
crypto_data = response.json()

for coin, data in crypto_data.items():
    print(f"{coin}: ${data['usd']}")