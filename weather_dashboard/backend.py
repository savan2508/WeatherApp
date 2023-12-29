import os

from weathermap import Weather
from dotenv import load_dotenv

load_dotenv()

openweather_api = os.getenv("OPENWEATHER_API")


def get_date(place, forecast_days=5, kind="Temperature"):
    weather = Weather(apikey=openweather_api, city=place, track_location=False)
    weather_response = weather.get_forecast()
    weather_response_condensed = weather_response["list"][: forecast_days * 8]

    return weather_response_condensed


if __name__ == "__main__":
    print(get_date(place="London", kind="sky"))
