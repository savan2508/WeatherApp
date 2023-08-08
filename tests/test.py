import os
import pprint

from weathermap import WeatherCache
from weathermap.weathermap import Weather
from dotenv import load_dotenv

# Load the contents of the .env file into the environment variables
load_dotenv()

openweather_api = os.getenv('OPENWEATHER_API')


tampa_weather = Weather(apikey=openweather_api)
# tampa_weather.api_request()

# a = WeatherCache().get_cached_weather(city="Tampa", timeout="hours=1", req_type="weather")
#
# pprint.pprint(a)
pprint.pprint(tampa_weather.api_request())

