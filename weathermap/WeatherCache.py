import os
import json
from datetime import datetime


class WeatherCache:
    def __init__(self,cache_system=True, cache_directory='weather_cache'):
        self.cache_directory = cache_directory
        if cache_system:
            self.create_dir(self.cache_directory)

    @staticmethod
    def create_dir(weather_dir):
        os.makedirs(weather_dir, exist_ok=True)

    def _get_cache_filename(self, city, date_time):
        try:
            formatted_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
            if date_time:
                formatted_date_time = date_time.strftime('%Y-%m-%d_%H-%M')

            return os.path.join(self.cache_directory, f"{city}_{formatted_date_time}.json")
        except OSError:
            raise OSError("Cache system disabled")

    def create_cache(self, city, data, date_time=None):
        try:
            filename = self._get_cache_filename(city, date_time)
            with open(filename, 'w') as file:
                json.dump(data, file)
        except OSError:
            raise OSError("Cache System disabled")

    def update_cache(self, city, date_time, data):
        try:
            filename = self._get_cache_filename(city, date_time)
            if os.path.exists(filename):
                with open(filename, 'w') as file:
                    json.dump(data, file)
        except OSError:
            raise OSError("Cache System disabled")

    def retrieve_cache(self, city, date_time):
        try:
            filename = self._get_cache_filename(city, date_time)
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    return json.load(file)
            return None
        except OSError:
            raise OSError("Cache System disabled")

    def delete_cache(self, city, date_time):
        try:
            filename = self._get_cache_filename(city, date_time)
            if os.path.exists(filename):
                os.remove(filename)
        except OSError:
            raise OSError("Cache System disabled")
