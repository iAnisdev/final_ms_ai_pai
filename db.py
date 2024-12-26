import asyncpg
import os
from dotenv import load_dotenv
from shared.process_data import process_data

load_dotenv()

# Global variable to store the connection pool
db_pool = None

async def get_connection():
    """
    Create a connection pool for the database.
    """
    global db_pool
    if not db_pool:
        db_pool = await asyncpg.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
    return db_pool

async def initialize_data():
    """
    Initialize the database with data for btc, eth, bnb, and sol for 5 years.
    """
    pool = await get_connection()
    async with pool.acquire() as connection:
        print("Connection established successfully" if connection else "Connection failed")
        await process_data(connection, "BTCUSDT", "bitcoin", '1d', 5)
        await process_data(connection, "ETHUSDT", "ethereum", '1d', 5)
        await process_data(connection, "BNBUSDT", "binance", '1d', 5)
        await process_data(connection, "SOLUSDT", "solana", '1d', 5)

# This function is only used for standalone scripts
async def main():
    await initialize_data()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
