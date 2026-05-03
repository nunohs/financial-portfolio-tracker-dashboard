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
     invalid_tickers = []

     for ticker, quantity in zip(tickers, quantities):
        try:
            asset = yf.Ticker(ticker)
            history = asset.history(period="1d")  # Give me today's price history for this ticker.

            if history.empty:
                invalid_tickers.append(ticker)
                continue

            current_price = history["Close"].iloc[-1]  #Take the Closing price and take the last row
            total_value = current_price * quantity  # Calculate holding value

            portfolio_data.append({  # Adds a row of data for the table
                "ticker": ticker,
                "quantity": quantity,
                "current_price": current_price,
                "total_value": total_value
            })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            invalid_tickers.append(ticker)

     df = pd.DataFrame(portfolio_data)

     return df, invalid_tickers

def add_allocation_percentages(df):
    """
    Add allocation percentage for each asset based on total portfolio value.
    """
    if df.empty:
        df["allocation_percentage"] = []
        return df

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
        try:
            asset = yf.Ticker(ticker)
            history = asset.history(period=period) #Fetches historical prices

            if history.empty:
                continue

            asset_value = history["Close"] * quantity  # Calculate value of this holding over time
            historical_values[ticker] = asset_value
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            continue

        if historical_values.empty:
            return pd.DataFrame(columns=["Date", "total_portfolio_value"])
        
    historical_values["total_portfolio_value"] = historical_values.sum(axis=1) # Sum across columns to get total value for each date

    result = historical_values[["total_portfolio_value"]].reset_index()

    return result

def get_performance_metrics(tickers, quantities, period="30d"):
    """
    Calculate total portfolio return, best performing asset, and worst performing asset.
    """

    asset_returns = []
    starting_total_value = 0
    ending_total_value = 0

    for ticker, quantity in zip(tickers, quantities):
        try:
            asset = yf.Ticker(ticker)
            history = asset.history(period=period)

            if history.empty:
                continue

            starting_price = history["Close"].iloc[0]
            ending_price = history["Close"].iloc[-1]

            starting_value = starting_price * quantity
            ending_value = ending_price * quantity

            starting_total_value += starting_value
            ending_total_value += ending_value

            asset_return_percentage = ((ending_price - starting_price) / starting_price) * 100

            asset_returns.append({
                "ticker": ticker,
                "return_percentage": asset_return_percentage
            })
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            continue

    if starting_total_value == 0:
        total_return_percentage = 0
    else:
        total_return_percentage = (
            (ending_total_value - starting_total_value) / starting_total_value
        ) * 100

    returns_df = pd.DataFrame(asset_returns)

    if returns_df.empty:
        best_asset = "N/A"
        best_return = 0
        worst_asset = "N/A"
        worst_return = 0
    else:
        best_row = returns_df.loc[returns_df["return_percentage"].idxmax()]
        worst_row = returns_df.loc[returns_df["return_percentage"].idxmin()]

        best_asset = best_row["ticker"]
        best_return = best_row["return_percentage"]

        worst_asset = worst_row["ticker"]
        worst_return = worst_row["return_percentage"]

    return {
        "total_return_percentage": total_return_percentage,
        "best_asset": best_asset,
        "best_return": best_return,
        "worst_asset": worst_asset,
        "worst_return": worst_return
    }


if __name__ == "__main__":               # Only run the code below if I run data.py directly.
    test_tickers = ["AAPL", "MSFT", "BTC-USD"]
    test_quantities = [2, 3, 0.1]

    df = get_stock_data(test_tickers, test_quantities)
    print(df)

