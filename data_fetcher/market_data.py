import yfinance as yf
import pandas as pd

def fetch_historical_data(symbol, period='1y', interval='1d'):
    """
    Fetch historical OHLCV data for a given symbol.
    Args:
        symbol (str): Ticker symbol (e.g., 'AAPL')
        period (str): Data period (e.g., '1y', '6mo')
        interval (str): Data interval (e.g., '1d', '1h')
    Returns:
        pd.DataFrame: DataFrame with OHLCV data
    """
    df = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=False)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    return df 