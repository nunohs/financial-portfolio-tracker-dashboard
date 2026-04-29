import pandas as pd # pandas is for making tables
import yfinance as yf

def get_stock_data(tickers, quantities):
     """
    Fetch current prices for a list of tickers and calculate total value.

    Parameters:
        tickers: list of ticker symbols, e.g. ["AAPL", "MSFT", "BTC-USD"]
        quantities: list of quantities owned, e.g. [2, 3, 0.1]

    Returns:
        pandas DataFrame with ticker, quantity, current_price, total_value
    """
     portfolio_data=[]
     for ticker, quantity in zip(tickers, quantities):
        asset = yf.Ticker(ticker)
        history = asset.history(period="1d")  # Give me today's price history for this ticker.

        if history.empty:
            current_price = 0
        else:
            current_price = history["Close"].iloc[-1]  #Take the Closing price and take the last row

        total_value = current_price * quantity  # Calculate holding value

        portfolio_data.append({  # Adds a row of data for the table
            "ticker": ticker,
            "quantity": quantity,
            "current_price": current_price,
            "total_value": total_value
        })

     df = pd.DataFrame(portfolio_data)

     return df


if __name__ == "__main__":               # Only run the code below if I run data.py directly.
    test_tickers = ["AAPL", "MSFT", "BTC-USD"]
    test_quantities = [2, 3, 0.1]

    df = get_stock_data(test_tickers, test_quantities)
    print(df)
