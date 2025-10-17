import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY= os.getenv("WEATHER_API_KEY")

def get_weather(city: str) -> dict: # -> dict 는 optional
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    resp = requests.get(endpoint, params=params)

    resp.raise_for_status()

    data = resp.json() # 안하면 address가 나옴
    weather = {
        "temp_c": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity_pct": data["main"]["humidity"],
        "wind_kph": data["wind"]["speed"] * 3.6 # m/s -> km/h로 바꿔주는 값
    }

    return weather

# city = input("enter city name: ")
# print(get_weather(city))