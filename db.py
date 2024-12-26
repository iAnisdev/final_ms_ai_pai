import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from shared.process_data import process_data

load_dotenv()

async def main():
    # Connect to the database
    connection = await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    print("Connection established successfully" if connection else "Connection failed")

    # fetch data for btc, eth , bnb and sol for 5 years
    await process_data(connection, "BTCUSDT", "bitcoin", '1d', 5)
    await process_data(connection, "ETHUSDT", "ethereum", '1d', 5)
    await process_data(connection, "BNBUSDT", "binance", '1d', 5)
    await process_data(connection, "SOLUSDT", "solana", '1d', 5)


if __name__ == "__main__":
    asyncio.run(main())
