import requests
import pandas as pd
import psycopg2
from datetime import datetime

# Fetch weather data
URL="https://api.open-meteo.com/v1/forecast?latitude=19.0760&longitude=72.8777&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
response=requests.get(URL)
data=response.json()

# Extract just the current weather values
current=data["current"]

# Create a clean table with one row
df=pd.DataFrame([{
    "recorded_at":datetime.now(),
    "temperature":current["temperature_2m"],
    "humidity": current["relative_humidity_2m"],
    "wind_speed": current["wind_speed_10m"],
    "city":"Mumbai"
}])

print("Clean data:")
print(df)

# Connect to PostgreSQL
conn=psycopg2.connect(
    host="localhost",
    database="weather_db",
    user="postgres",
    password="YOUR_PASSWORD_HERE")

cur=conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id SERIAL PRIMARY KEY,
        recorded_at TIMESTAMP,
        temperature FLOAT,
        humidity INT,
        wind_speed FLOAT,
        city TEXT
    )
""")

# Insert the row
cur.execute("""
    INSERT INTO weather (recorded_at, temperature, humidity, wind_speed, city)
    VALUES (%s, %s, %s, %s, %s)
""", (
    df["recorded_at"][0],
    float(df["temperature"][0]),
    int(df["humidity"][0]),
    float(df["wind_speed"][0]),
    str(df["city"][0])
))

conn.commit()
cur.close()
conn.close()
print("Data saved to database successfully!")