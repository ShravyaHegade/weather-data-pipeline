# Automated Weather Data Pipeline

## What it does
An automated ETL (Extract, Transform, Load) pipeline that fetches 
real-time weather data for Mumbai every 5 mins, cleans it using 
Python and Pandas, and stores it in a PostgreSQL database automatically.

## Architecture
Open-Meteo API → Python → PostgreSQL database

## Tools used
- Python (requests, pandas, psycopg2)
- PostgreSQL
- Automated scheduling (while loop + time.sleep)
- Logging

## How it works
1. Fetches live weather data (temperature, humidity, wind speed)
2. Cleans and transforms it into a structured table
3. Inserts it into PostgreSQL with a timestamp
4. Repeats automatically every 5 mins

## Sample data collected
| recorded_at | temperature | humidity | wind_speed | city |
|-------------|-------------|----------|------------|------|
| 2026-06-01 17:20:32.890651 |32.3 | 64 | 13.2 | Mumbai |
| 2026-06-01 17:32:53.56369  |32.2 | 64 | 13   | Mumbai |

## What I learned
- How to fetch data from REST APIs using Python
- Data cleaning and transformation with Pandas
- Storing structured data in PostgreSQL
- Building automated pipelines with error handling and logging
- Debugging real errors independently
- Linux basics and Git Bash navigation
