import psycopg2
from app.core.config import settings

# Connect to the database
conn = psycopg2.connect(
    dbname="market_db",
    user="postgres",
    password="",
    host="localhost"
)

# Create a cursor
cur = conn.cursor()

try:
    # Execute query
    cur.execute("SELECT id, name, image_url FROM markets")
    
    # Fetch all rows
    markets = cur.fetchall()
    
    print("\nMarket Data:")
    print("-" * 50)
    for market in markets:
        print(f"ID: {market[0]}")
        print(f"Name: {market[1]}")
        print(f"Image URL: {market[2]}")
        print("-" * 50)

finally:
    # Close cursor and connection
    cur.close()
    conn.close() 