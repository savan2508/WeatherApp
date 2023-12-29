import os

from weathermap import Weather
from dotenv import load_dotenv

load_dotenv()

openweather_api = os.getenv("OPENWEATHER_API")


def get_date(place, forecast_days=5, kind="Temperature"):
    weather = Weather(apikey=openweather_api, city=place, track_location=False)
    weather_response = weather.get_forecast()
    weather_response_condensed = weather_response["list"][: forecast_days * 8]

    if kind.lower() == "temperature":
        filtered_data = [dicty["main"]["temp"] for dicty in weather_response_condensed]
        return filtered_data

    elif kind.lower() == "sky":
        filtered_data = [
            dicty["weather"][0]["main"] for dicty in weather_response_condensed
        ]
        return filtered_data

    return 0


if __name__ == "__main__":
    print(get_date(place="London", kind="sky"))
