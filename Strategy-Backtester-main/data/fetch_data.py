import pandas as pd
from datetime import datetime
import time
from alpha_vantage.timeseries import TimeSeries
import os
from dotenv import load_dotenv


def fetch_historical_data(ticker: str, start_date: str, end_date: str, max_retries: int = 3) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given ticker and date range using Alpha Vantage.
    
    Args:
        ticker (str): Stock ticker symbol
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        pd.DataFrame: DataFrame containing OHLCV data
    """
    # Load API key
    load_dotenv('config/config.env')
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key or api_key == 'demo':
        raise ValueError("Please set your Alpha Vantage API key in config.env. Get one at https://www.alphavantage.co/support/#api-key")
    
    # Initialize Alpha Vantage
    ts = TimeSeries(key=api_key, output_format='pandas')
    
    for attempt in range(max_retries):
        try:
            # Fetch data
            data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
            
            # Rename columns 
            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Convert index to datetime 
            data.index = pd.to_datetime(data.index)
            
            # Sort index in ascending order
            data = data.sort_index()
            
            # Convert date strings to datetime objects
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            # Filter data using boolean indexing
            mask = (data.index >= start_dt) & (data.index <= end_dt)
            data = data.loc[mask]
            
            # Verify data
            if data.empty:
                raise ValueError(f"No data found for {ticker} between {start_date} and {end_date}")
            
            # Verify we have enough data points
            if len(data) < 200:  # Minimum required for SMA calculation
                raise ValueError(f"Insufficient data points for {ticker}. Need at least 200 days of data.")
            
            return data
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                print(f"Waiting {5 * (attempt + 1)} seconds before retry...")
                time.sleep(5 * (attempt + 1))  # Progressive delay
            else:
                raise Exception(f"Error fetching data for {ticker} after {max_retries} attempts: {str(e)}") 