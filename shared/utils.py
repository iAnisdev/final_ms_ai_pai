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

