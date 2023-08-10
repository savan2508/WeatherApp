import unittest
from weathermap import Weather
import os
from dotenv import load_dotenv

# Load the contents of the .env file into the environment variables
load_dotenv()

API_key = os.getenv('OPENWEATHER_API')


class TestExample(unittest.TestCase):

    def test_location_tracking(self):
        # uses IP address coordinates
        try:
            weather_info = Weather(apikey=API_key)
            weather_info.get_current_weather()
            weather_info.get_forecast()
        except ValueError:
            self.fail("Unexpected ValueError raised")
        except AssertionError:
            self.fail("Unexpected AssertionError raised")

    def test_city(self):
        # uses coordinates for Tampa, Florida
        try:
            weather_info = Weather(apikey=API_key, city="Tampa")
            weather_info.get_current_weather()
            weather_info.get_forecast()
        except ValueError:
            self.fail("Unexpected ValueError raised")
        except AssertionError:
            self.fail("Unexpected AssertionError raised")

    def test_lat_lon(self):
        # uses coordinates for Tampa, Florida
        try:
            weather_info = Weather(apikey=API_key, lat=27.964157, lon=-82.452606)
            weather_info.get_current_weather()
            weather_info.get_forecast()
        except ValueError:
            self.fail("Unexpected ValueError raised")
        except AssertionError:
            self.fail("Unexpected AssertionError raised")

    def test_zip_country(self):
        # uses coordinates for Tampa, Florida -> Hillsborough County
        try:
            weather_info = Weather(apikey=API_key, zip_code=33592, country="US")
            weather_info.get_current_weather()
            weather_info.get_forecast()
        except ValueError:
            self.fail("Unexpected ValueError raised")
        except AssertionError:
            self.fail("Unexpected AssertionError raised")


if __name__ == '__main__':
    unittest.main()
