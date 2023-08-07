import os
import json
from datetime import datetime, timedelta


class WeatherCache:
    def __init__(self,cache_system=True, cache_directory='weather_cache', **kwargs):
        self.cache_directory = cache_directory
        if cache_system:
            self.create_dir(self.cache_directory)

    @staticmethod
    def create_dir(weather_dir):
        os.makedirs(weather_dir, exist_ok=True)

    def _get_cache_filename(self, names):
        name_dict = self.validate_name_for_directory_name(names)
        formatted_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
        if name_dict['date_time']:
            formatted_date_time = name_dict['date_time'].strftime('%Y-%m-%d_%H-%M')
        try:
            return os.path.join(self.cache_directory, f"{name_dict['city']}{name_dict['state'][0:2].upper()}"
                                                      f"{name_dict['country']}_{name_dict['req_type'][0:3]}_"
                                                      f"{formatted_date_time}.json")
        except OSError or AttributeError:
            raise OSError("Cache system disabled")

    def create_cache(self, data, **kwargs):
        name_dict = self.validate_name_for_directory_name(kwargs)
        try:
            filename = self._get_cache_filename(name_dict)
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

    def get_cached_weather(self, city, req_type, timeout=None):
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        try:
            cached_files = os.listdir(self.cache_directory)

            for filename in cached_files:
                if filename.endswith(".json"):
                    file_city, file_req_time, file_time_str = filename[:-5].split("_", 2)
                    file_time = datetime.strptime(file_time_str, '%Y-%m-%d_%H-%M')

                    if file_city == city and file_time >= one_hour_ago and file_req_time == req_type[:3]:
                        # The file exists for the same city and within the past 1 hour
                        try:
                            filepath = os.path.join(self.cache_directory, filename)
                            with open(filepath, 'r') as file:
                                return json.load(file)
                        except FileNotFoundError:
                            raise OSError(f"File not found: {city}")

            # No cached file found for the same city within the past 1 hour
            raise FileNotFoundError(f"File not found: {city}")

        except OSError:
            raise FileNotFoundError(f"File not found: {city}")

    def validate_name_for_directory_name(self, input_dict: dict):
        dicty = {
            "city": "",
            "state": "",
            "country": "",
            "zip_code": "",
            "lat": "",
            "lon": "",
            "req_type": "",
            "date_time": None
        }
        for key in input_dict.keys():
            if key in dicty.keys() and (input_dict[key] is not None):
                dicty[key] = input_dict[key]

        return dicty


