import os
import json
from datetime import datetime, timedelta


class WeatherCache:
    def __init__(self, cache_system: bool = True, cache_directory: str = 'weather_cache',
                 auto_cache_clean_for_exceed_limit: bool = False,
                 cache_cleaning: bool = True, cache_size_limit_mb: int = 200, **kwargs):
        self.cache_directory = cache_directory
        self.cache_cleaning = cache_cleaning
        self.cache_size_limit_mb= cache_size_limit_mb
        self.auto_cache_clean_for_exceed_limit = auto_cache_clean_for_exceed_limit
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
            return (f"{name_dict['city']}{name_dict['state'][0:2].upper()}{name_dict['country']}_"
                    f"{name_dict['req_type'][0:3]}_{formatted_date_time}.json")

        except AttributeError:
            raise AttributeError("Missing attribute to create a cache")

    def create_cache(self, data, **kwargs):
        name_dict = self.validate_name_for_directory_name(kwargs)
        try:
            filename = os.path.join(self.cache_directory, self._get_cache_filename(name_dict))
            with open(filename, 'w') as file:
                json.dump(data, file)
        except OSError:
            raise OSError("Cache System disabled")

    def delete_cache(self, city, date_time):
        try:
            filename = self._get_cache_filename(city, date_time)
            if os.path.exists(filename):
                os.remove(filename)
        except OSError:
            raise OSError("Cache System disabled")

    def get_cached_weather(self, timeout: dict, **kwargs):
        cache_filename = self._get_cache_filename(kwargs)

        cache_filename_city, cache_filename_req_type, cache_filename_time_str = cache_filename[:-5].split("_", 2)

        forcast_time_delta = self.forcast_timedelta(timeout)

        try:
            cached_files = os.listdir(self.cache_directory)

            for filename in cached_files:
                if filename.endswith(".json"):
                    file_city, file_req_type, file_time_str = filename[:-5].split("_", 2)
                    file_time = datetime.strptime(file_time_str, '%Y-%m-%d_%H-%M')

                    if (file_city == cache_filename_city and file_time >= forcast_time_delta and
                            file_req_type == cache_filename_req_type):
                        # The file exists for the same city and within the past 1 hour
                        try:
                            filepath = os.path.join(self.cache_directory, filename)
                            with open(filepath, 'r') as file:
                                return json.load(file)
                        except FileNotFoundError:
                            raise OSError(f"File not found: {cache_filename}")

            # No cached file found for the same city within the past 1 hour
            raise FileNotFoundError(f"File not found: {cache_filename}")

        except OSError:
            raise FileNotFoundError(f"File not found: {cache_filename}")

    def forcast_timedelta(self, timeout):
        if timeout['req_type'] == 'weather':
            placeholder = 'weather_timeout'
        elif timeout['req_type'] == 'forcast':
            placeholder = 'forcast_timeout'
        elif timeout['req_type'] == 'air_pollution':
            placeholder = 'air_pollution_timeout'
        else:
            raise ValueError("Please provide correct req_type")
        now = datetime.now()
        forcast_time_delta = now - timedelta(seconds=timeout[placeholder]['seconds'],
                                             minutes=timeout[placeholder]['minutes'],
                                             hours=timeout[placeholder]['hours'],
                                             days=timeout[placeholder]['days'])
        return forcast_time_delta

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

    def delete_directory_cache(self, directory):
        pass

    def get_directory_size(self, directory):
        pass

    def delete_oldest_and_outdated_file(self, directory, timeout: dict, req_type):
        oldest_file = None
        oldest_timestamp = float('inf')

        forcast_time_delta = self.forcast_timedelta(timeout)

        filenames = os.listdir(directory)
        for filename in filenames:
            if filename.endswith(".json"):
                file_city, file_req_type, file_time_str = filename[:-5].split("_", 2)
                file_time = datetime.strptime(file_time_str, '%Y-%m-%d_%H-%M')
                filepath = os.path.join(directory, filename)
                file_timestamp = os.path.getmtime(filepath)

                if

                if file_timestamp < oldest_timestamp:
                    oldest_timestamp = file_timestamp
                    oldest_file = filepath

        if oldest_file:
            os.remove(oldest_file)
            # print(f"Deleted oldest file: {oldest_file}")

    def manage_directory_size(self, directory: str=None, threshold_size : int = None):
        if directory is None:
            directory = self.cache_directory
        if threshold_size is None:
            threshold_size = int(self.cache_size_limit_mb) * 1024 * 1024

        current_size = os.path.getsize(directory)
        while current_size <= threshold_size:
            self.delete_oldest_and_outdated_file(directory)

