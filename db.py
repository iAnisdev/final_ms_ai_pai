import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


async def create_table(connection, table_name):
    await connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP UNIQUE,
            open NUMERIC(20, 8) NOT NULL,
            high NUMERIC(20, 8) NOT NULL,
            low NUMERIC(20, 8) NOT NULL,
            close NUMERIC(20, 8) NOT NULL,
            volume NUMERIC(20, 8) NOT NULL,
            number_of_trades NUMERIC(20, 8) NOT NULL
        )
        """
    )
    print(f"Table {table_name} created")


async def insert_data(connection, table_name, data):
    print(f"Inserting {len(data)} rows into {table_name}")
    query = f"""
        INSERT INTO {table_name} (timestamp, open, high, low, close, volume, number_of_trades)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (timestamp) DO NOTHING
    """
    await connection.executemany(query, data)
    print(f"Data inserted into {table_name} successfully")


async def close_connection(connection):
    # Close the connection
    await connection.close()
    print("Database connection closed")


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


if __name__ == "__main__":
    asyncio.run(main())
