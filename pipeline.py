import requests 
import pandas as pd 
import psycopg2
import logging
import time
from datetime import datetime 

# Set up logging
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s-%(message)s"
)

URL = "https://api.open-meteo.com/v1/forecast?latitude=19.0760&longitude=72.8777&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

DB= {
    "host":"localhost",
    "database":"weather_db",
    "user":"postgres",
    "password":"YOUR_PASSWORD_HERE"
}

# The Extract Function
def extract():
    logging.info("Extracting Data...")
    response=requests.get(URL)
    current=response.json()["current"]
    logging.info("Data fetched Successfully")
    return current 

# The Transform Function
def transform(current):
    logging.info("Transforming Data...")
    df=pd.DataFrame([{
        "recorded_at":datetime.now(),
        "temperature":current["temperature_2m"],
        "humidity":current["relative_humidity_2m"],
        "wind_speed":current["wind_speed_10m"],
        "city":"Mumbai"
    }])
    return df 

# The Load function 
def load(df):
    logging.info("Loading into database...")
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
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
    
    # Extract values directly — fixes the conversion error
    recorded_at = df["recorded_at"].iloc[0]
    temperature = float(df["temperature"].iloc[0])
    humidity    = int(df["humidity"].iloc[0])
    wind_speed  = float(df["wind_speed"].iloc[0])
    city        = str(df["city"].iloc[0])
    
    cur.execute("""
        INSERT INTO weather (recorded_at, temperature, humidity, wind_speed, city)
        VALUES (%s, %s, %s, %s, %s)
    """, (recorded_at, temperature, humidity, wind_speed, city))
    
    conn.commit()
    cur.close()
    conn.close()
    logging.info("Data loaded successfully!")

# The run_pipeline function
def run_pipeline():
    try:
        logging.info("=== Pipeline started ===")
        current=extract()
        df=transform(current)
        load(df)
        print(f"Pipeline ran successfully at {datetime.now()}")
        logging.info("=== Pipeline completed ===")
    except Exception as e:
        logging.error(f"Pipeline failed {e}")
        print(f"Error{e}")

# The automatic loop
while(True):
    run_pipeline()
    print("Waiting 5 mins before next run...")
    time.sleep(300)
