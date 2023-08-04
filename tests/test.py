import os
import pprint
import weathermap.weathermap
from dotenv import load_dotenv

# Load the contents of the .env file into the environment variables
load_dotenv()

openweather_api = os.getenv('OPENWEATHER_API')
