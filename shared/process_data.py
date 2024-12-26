from .fetch_data import fetch_market_data
from .utils import create_table, insert_data


async def process_data(connection, symbol, table_name, interval, years):
    # Create the table
    await create_table(connection, table_name)
    # fetch data from binance for the given symbol and interval
    data = fetch_market_data(symbol, interval, years * 365)

    data = [
        (
            record["timestamp"],
            float(record["open"]),
            float(record["high"]),
            float(record["low"]),
            float(record["close"]),
            float(record["volume"]),
            float(record["number_of_trades"]),
        )
        for record in data.to_dict("records")
    ]
    # Insert data
    await insert_data(connection, table_name, data)

    return data
