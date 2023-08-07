import os
import pprint
from weathermap.weathermap import Weather
from dotenv import load_dotenv
from weathermap import Weather

# Load the contents of the .env file into the environment variables
load_dotenv()

openweather_api = os.getenv('OPENWEATHER_API')


tampa_weather = Weather(apikey="openweather_api", city="Tampa,US")
tampa_weather.forcast()
#
# pprint.pprint(tampa_weather.data)

