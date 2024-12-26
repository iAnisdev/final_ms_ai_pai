import asyncio
import asyncpg
import os
from dotenv import load_dotenv

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


if __name__ == "__main__":
    asyncio.run(main())
