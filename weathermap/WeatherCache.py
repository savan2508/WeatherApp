import os
import json
from datetime import datetime, timedelta


class CacheCleaningDisabledError(Exception):
    pass


class WeatherCache:
    def __init__(self, cache_system: bool = True, cache_directory: str = 'weather_cache',
                 auto_cache_clean_for_exceed_limit: bool = False,
                 cache_cleaning: bool = True, cache_size_limit_mb: int = 200, **kwargs):
        self.cache_directory = cache_directory
        self.cache_cleaning = cache_cleaning
        self.cache_size_limit_mb = cache_size_limit_mb
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
            raise CacheCleaningDisabledError("Missing attribute to create a cache")

    def create_cache(self, data, **kwargs):
        name_dict = self.validate_name_for_directory_name(kwargs)
        try:
            filename = os.path.join(self.cache_directory, self._get_cache_filename(name_dict))
            with open(filename, 'w') as file:
                json.dump(data, file)
        except OSError:
            raise OSError("Cache System disabled")

    def get_cached_weather(self, timeout: dict, **kwargs):
        cache_filename = self._get_cache_filename(kwargs)

        cache_filename_city, cache_filename_req_type, cache_filename_time_str = cache_filename[:-5].split("_", 2)

        forcast_time_delta = datetime.now() - self.forcast_timedelta(timeout)

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
            raise CacheCleaningDisabledError(f"File not found: {cache_filename}")

    @staticmethod
    def forcast_timedelta(timeout: dict) -> timedelta:
        """

        :param timeout:
        :return:
        """
        if timeout['req_type'] == 'weather':
            placeholder = 'weather_timeout'
        elif timeout['req_type'] == 'forcast':
            placeholder = 'forcast_timeout'
        elif timeout['req_type'] == 'air_pollution':
            placeholder = 'air_pollution_timeout'
        else:
            raise ValueError("Please provide correct req_type")
        forcast_timedelta = timedelta(seconds=timeout[placeholder]['seconds'],
                                      minutes=timeout[placeholder]['minutes'],
                                      hours=timeout[placeholder]['hours'],
                                      days=timeout[placeholder]['days'])
        return forcast_timedelta

    @staticmethod
    def validate_name_for_directory_name(input_dict: dict) -> dict:
        """
        The method takes the keyword arguments for the function to clean them for naming the cache
        :param input_dict: take keyword arguments from method
        :return: cleaned dictionary with valid names
        """
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

    def delete_oldest_and_outdated_file(self, directory, timeout: dict):
        oldest_file = None
        oldest_timestamp = float('inf')

        forcast_time_delta = self.forcast_timedelta(timeout)
        expired_file_time = datetime.now() - forcast_time_delta

        filenames = os.listdir(directory)
        for filename in filenames:
            if filename.endswith(".json"):
                file_city, file_req_type, file_time_str = filename[:-5].split("_", 2)
                file_time = datetime.strptime(file_time_str, '%Y-%m-%d_%H-%M')
                filepath = os.path.join(directory, filename)
                file_timestamp = os.path.getmtime(filepath)

                if file_time > expired_file_time:
                    os.remove(filepath)

                elif file_timestamp < oldest_timestamp:
                    oldest_timestamp = file_timestamp
                    oldest_file = filepath

        if oldest_file:
            os.remove(oldest_file)
            # print(f"Deleted oldest file: {oldest_file}")

    def manage_directory_size(self, timeout, directory: str = None, threshold_size: int = None,
                              cache_cleaning: bool = None):
        if directory is None:
            directory = self.cache_directory
        if threshold_size is None:
            threshold_size = int(self.cache_size_limit_mb) * 1024 * 1024
        if cache_cleaning is None:
            cache_cleaning = self.cache_cleaning

        if cache_cleaning:
            current_size = os.path.getsize(directory)
            if current_size > threshold_size:
                while current_size <= threshold_size / 2:
                    self.delete_oldest_and_outdated_file(directory=directory, timeout=timeout)
            else:
                raise ValueError("Current directory size is not greater than the threshold size.")
        else:
            raise CacheCleaningDisabledError("cache_cleaning is disable. Please enable it use this feature.")
