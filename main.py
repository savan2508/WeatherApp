import requests
import os
from dotenv import load_dotenv

# Load the contents of the .env file into the environment variables
load_dotenv()

openweather_api = os.getenv('OPENWEATHER_API')

# url = f"https://api.openweathermap.org/data/2.5/forecast?q=London,uk&APPID={openweather_api}"


class Weather:

    def __init__(self, apikey, city=None, lat=None, lon=None, units="imperial"):

        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},uk&APPID={apikey}&units={units}"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            pass

    def next_12h(self):
        pass

    def next_12h_simplified(self):
        pass


weather = Weather(apikey=openweather_api, city="London")
print(weather.data)

