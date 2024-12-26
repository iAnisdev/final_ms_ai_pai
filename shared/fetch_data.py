from binance.client import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

load_dotenv()

# Get API key
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Create a client
client = Client(api_key, api_secret)


def fetch_market_data(symbol, interval="1d", days=5 * 365):
    """
    Get history OHLCV data for Bitcoin (BTC)
    :param symbol:  trading pair, 'BTCUSDT', 'ETHUSDT' , 'BNBUSDT' , 'SOLUSDT'
    :param interval: K-line period, '1d'
    :return: pandas DataFrame
    """
    # Calculate the date from 5 years ago and format it in 'YYYY-MM-DD UTC' format
    five_years_ago = datetime.now() - timedelta(days=days)
    start_date = five_years_ago.strftime("%Y-%m-%d")

    # Get historical data
    klines = client.get_historical_klines(symbol, interval, start_str=start_date)

    # Convert data to -- pandas DataFrame
    ohlcv_data = pd.DataFrame(
        klines,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )

    # Converts the timestamp to date format
    ohlcv_data["timestamp"] = pd.to_datetime(ohlcv_data["timestamp"], unit="ms")

    # return
    return ohlcv_data[
        ["timestamp", "open", "high", "low", "close", "volume", "number_of_trades"]
    ]
