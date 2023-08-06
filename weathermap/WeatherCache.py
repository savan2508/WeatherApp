import os
import json
from datetime import datetime


class WeatherCache:
    def __init__(self, cache_directory='weather_cache'):
        self.cache_directory = cache_directory
        self.create_dir(self.cache_directory)

    @staticmethod
    def create_dir(weat_dir):
        os.makedirs(weat_dir, exist_ok=True)

    def _get_cache_filename(self, city, date_time):
        formatted_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
        if date_time:
            formatted_date_time = date_time.strftime('%Y-%m-%d_%H-%M')

        return os.path.join(self.cache_directory, f"{city}_{formatted_date_time}.json")

    def create_cache(self, city, data, date_time=None):
        filename = self._get_cache_filename(city, date_time)
        with open(filename, 'w') as file:
            json.dump(data, file)

    def update_cache(self, city, date_time, data):
        filename = self._get_cache_filename(city, date_time)
        if os.path.exists(filename):
            with open(filename, 'w') as file:
                json.dump(data, file)

    def retrieve_cache(self, city, date_time):
        filename = self._get_cache_filename(city, date_time)
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return None

    def delete_cache(self, city, date_time):
        filename = self._get_cache_filename(city, date_time)
        if os.path.exists(filename):
            os.remove(filename)
