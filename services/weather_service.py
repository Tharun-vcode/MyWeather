import requests
import os
from functools import lru_cache

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


@lru_cache(maxsize=100)
def fetch_weather(city):
    current_params = {"q": city, "appid": API_KEY, "units": "metric"}
    current_resp = requests.get(BASE_CURRENT_URL, params=current_params)

    if current_resp.status_code != 200:
        return None, current_resp.status_code

    current_data = current_resp.json()

    lat, lon = current_data['coord']['lat'], current_data['coord']['lon']
    city_name = current_data['name']

    forecast_params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    forecast_resp = requests.get(BASE_FORECAST_URL, params=forecast_params)

    forecast_data = []

    if forecast_resp.status_code == 200:
        forecast_json = forecast_resp.json()
        daily_data = {}

        for item in forecast_json['list']:
            date_str = item['dt_txt'].split(' ')[0]
            temp = item['main']['temp']

            if date_str not in daily_data:
                daily_data[date_str] = {
                    'date': item['dt'],
                    'temp_max': temp,
                    'temp_min': temp,
                }
            else:
                daily_data[date_str]['temp_max'] = max(daily_data[date_str]['temp_max'], temp)
                daily_data[date_str]['temp_min'] = min(daily_data[date_str]['temp_min'], temp)

        for date_str in sorted(daily_data.keys())[:5]:
            forecast_data.append(daily_data[date_str])

    result = {
        "current": {
            "city_name": city_name,
            "temp": current_data["main"]["temp"],
            "feels_like": current_data["main"]["feels_like"],
            "humidity": current_data["main"]["humidity"],
            "pressure": current_data["main"]["pressure"],
            "wind_speed": current_data["wind"]["speed"],
            "visibility": current_data.get("visibility", 0) / 1000,  # convert meters to km
            "condition": current_data["weather"][0]["description"].capitalize(),
            "icon": current_data["weather"][0]["icon"],
            "sunrise": current_data["sys"]["sunrise"],
            "sunset": current_data["sys"]["sunset"]
       },
        "forecast": forecast_data
    }


    return result, 200
