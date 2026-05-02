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

def add_allocation_percentages(df):
    """
    Add allocation percentage for each asset based on total portfolio value.
    """

    total_value = df["total_value"].sum()

    if total_value == 0:
        df["allocation_percentage"] = 0
    else:
        df["allocation_percentage"] = (df["total_value"] / total_value) * 100

    return df

def get_historical_value(tickers, quantities, period="30d"):
    """
    Fetch historical prices and calculate total portfolio value over time.

    Returns:
        DataFrame with date and total_portfolio_value
    """

    historical_values = pd.DataFrame()  # Creates an empty table

    for ticker, quantity in zip(tickers, quantities):
        asset = yf.Ticker(ticker)
        history = asset.history(period=period) #Fetches historical prices

        if history.empty:
            continue

        asset_value = history["Close"] * quantity  # Calculate value of this holding over time
        historical_values[ticker] = asset_value

    historical_values["total_portfolio_value"] = historical_values.sum(axis=1) # Sum across columns to get total value for each date

    result = historical_values[["total_portfolio_value"]].reset_index()

    return result