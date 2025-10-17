import os
import requests
from dotenv import load_dotenv

# 1. Load the API key from .env
load_dotenv()  
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city: str) -> dict:
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    resp = requests.get(endpoint, params=params)

    resp.raise_for_status() # Raise an error for bad responses (4xx, 5xx)

    # print("Before json", resp)
    data = resp.json()
    # print("After json", data)
    weather = {
        "temp_c": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity_pct": data["main"]["humidity"],
        "wind_kph": data["wind"]["speed"] * 3.6  # m/s → km/h
    }
    # temperature = weather["temp_c"]
    return weather

# city = input("Enter city name: ")
# print(get_weather("Seoul"))