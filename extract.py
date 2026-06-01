# Import libraries
import requests
import pandas as pd

# No API key needed — this URL fetches Mumbai weather for free
URL = URL = "https://api.open-meteo.com/v1/forecast?latitude=19.0760&longitude=72.8777&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

# Fetch the data
response=requests.get(URL)
data=response.json()

# Print raw data to see what we got
print(data)