import asyncpg
import asyncio

# Database connection parameters
DB_CONFIG = {
    "user": "root",
    "password": "password",
    "database": "crypto_analysis",
    "host": "localhost",
    "port": 5432,
}

# Function to connect to the database.
async def connect_to_db():
    return await asyncpg.connect(**DB_CONFIG)

# Function to create a table
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
    print(f"Table {table_name} created.")

# Function to insert test data
async def insert_data(connection, table_name, data):
    print(f"Inserting {len(data)} rows into {table_name}...")
    query = f"""
        INSERT INTO {table_name} (timestamp, open, high, low, close, volume, number_of_trades)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (timestamp) DO NOTHING
    """
    await connection.executemany(query, data)
    print(f"Data inserted into {table_name} successfully.")

# Function to close the connection
async def close_connection(connection):
    await connection.close()
    print("Database connection closed.")

# Main script
async def main():
    # Test data
    sample_data = [
        ("2024-12-27 10:00:00", 50000.00, 51000.00, 49500.00, 50500.00, 120.5, 300),
        ("2024-12-27 11:00:00", 50500.00, 51500.00, 50000.00, 51000.00, 130.7, 320),
    ]

    try:
        # Connect to the database
        connection = await connect_to_db()
        print("Connected to the database.")

        # Create tables
        await create_table(connection, "bitcoin")
        await create_table(connection, "ethereum")
        await create_table(connection, "binance")
        await create_table(connection, "solana")

        # Insert test data into the Bitcoin table
        await insert_data(connection, "bitcoin", sample_data)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        if connection:
            await close_connection(connection)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())