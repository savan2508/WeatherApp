import os
import json
from datetime import datetime, timedelta


class CacheCleaningDisabledError(Exception):
    pass


class WeatherCache:
    """
    WeatherCache Class:

    This class provides a caching mechanism to store weather data and manage the cache directory. It supports creating,
    retrieving, and managing cached weather data.

    :param cache_system: Enable or disable a cache system.
    :type cache_system: bool
    :param cache_cleaning: Enable or disable cache cleaning.
    :type cache_cleaning: bool
    :param cache_directory: The directory where cached data will be stored (default is 'weather_cache').
    :type cache_directory: str
    :param auto_cache_clean_for_exceed_limit: Enables or disables automatic cache cleaning when exceeding the cache size
    limit (default is False).
    :type auto_cache_clean_for_exceed_limit: bool
    :param cache_size_limit_mb: The cache size limit in megabytes (default is 200 MB).
    :type cache_size_limit_mb: int
    :keyword timeout: A dictionary containing timeout values for different request types.
    :type timeout: dict

    Methods:
    - create_cache(data, timeout, **kwargs): Create cache for weather data.
    - get_cached_weather(timeout, **kwargs): Retrieve cached weather data.
    - forcast_timedelta(timeout): Calculate the forecast time delta.
    - validate_name_for_directory_name(input_dict): Validate and clean input dictionary for cache directory naming.
    - manage_directory_size(timeout, directory=None, threshold_size=None, cache_cleaning=None): Manage directory size by
      deleting outdated files when the cache size exceeds the threshold.

    """
    def __init__(self, cache_system: bool, cache_cleaning: bool, cache_directory: str = 'weather_cache',
                 auto_cache_clean_for_exceed_limit: bool = False, cache_size_limit_mb: int = 200, **kwargs):
        self.cache_directory = cache_directory
        self.cache_cleaning = cache_cleaning
        self.cache_size_limit_mb = cache_size_limit_mb
        self.auto_cache_clean_for_exceed_limit = auto_cache_clean_for_exceed_limit
        if cache_system:
            self.create_dir(self.cache_directory)

    @staticmethod
    def create_dir(weather_dir):
        """
        Create a directory if it doesn't exist.

        :param weather_dir: The directory to create.
        :type weather_dir: str
        """
        os.makedirs(weather_dir, exist_ok=True)

    def _get_cache_filename(self, names):
        """
        Generate a cache filename based on input data.

        :param names: Input data for naming the cache file.
        :type names: dict
        :return: Generated cache filename.
        :rtype: str
        """
        name_dict = self.validate_name_for_directory_name(names)
        formatted_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
        if name_dict['date_time']:
            formatted_date_time = name_dict['date_time'].strftime('%Y-%m-%d_%H-%M')
        try:
            return (f"{name_dict['city']}{name_dict['state'][0:2].upper()}{name_dict['country']}_"
                    f"{name_dict['req_type'][0:3]}_{formatted_date_time}.json")

        except AttributeError:
            raise CacheCleaningDisabledError("Missing attribute to create a cache")

    def create_cache(self, data, timeout: dict, **kwargs):
        """
        Create a cache for weather data.

        :param data: Weather data to cache.
        :type data: dict
        :param timeout: Timeout values for cache expiration.
        :type timeout: dict
        :param kwargs: Additional data for naming the cache file.
        :type kwargs: dict
        """
        name_dict = self.validate_name_for_directory_name(kwargs)
        try:
            filename = os.path.join(self.cache_directory, self._get_cache_filename(name_dict))
            with open(filename, 'w') as file:
                json.dump(data, file)

            if self.auto_cache_clean_for_exceed_limit:
                self.manage_directory_size(timeout=timeout, directory=self.cache_directory)
        except OSError:
            raise CacheCleaningDisabledError("Cache System disabled")

    def get_cached_weather(self, timeout: dict, **kwargs):
        """
        Retrieve cached weather data.

        :param timeout: Timeout values for cache expiration.
        :type timeout: dict
        :param kwargs: Additional data for identifying the cache file.
        :type kwargs: dict
        :return: Cached weather data.
        :rtype: dict
        """
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

                    elif self.cache_cleaning and file_time > forcast_time_delta:
                        filepath = os.path.join(self.cache_directory, filename)
                        os.remove(filepath)

                    elif self.auto_cache_clean_for_exceed_limit:
                        self.manage_directory_size(timeout=timeout, directory=self.cache_directory)

            # No cached file found for the same city within the past 1 hour
            raise FileNotFoundError(f"File not found: {cache_filename}")
        except OSError:
            raise CacheCleaningDisabledError(f"File not found: {cache_filename}")

    @staticmethod
    def forcast_timedelta(timeout: dict) -> timedelta:
        """
        Calculate the forecast time delta based on the request type.

        :param timeout: Timeout values for different request types.
        :type timeout: dict
        :return: Forecast time delta.
        :rtype: timedelta
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
        Validate and clean input data for naming cache directory.

        :param input_dict: Input data for naming cache directory.
        :type input_dict: dict
        :return: Cleaned dictionary with valid names.
        :rtype: dict
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

    def delete_oldest_and_outdated_file(self, directory, timeout: dict):
        """
        Delete the oldest and outdated cache files from the specified directory.

        This method iterates through the files in the given directory, identifying cache files that have expired
        according to the specified timeout values. It then deletes the cache files that are either outdated or no
        longer needed.

        :param directory: The directory containing cache files.
        :type directory: str
        :param timeout: Timeout values for cache expiration.
        :type timeout: dict
        """
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
        """
        Manage the size of the cache directory by deleting files when exceeding the size limit.

        This method checks the current size of the specified cache directory and compares it with the threshold size.
        If the current size exceeds the threshold, it iteratively deletes the oldest and outdated cache files until
        the directory size drops below half of the threshold size.

        :param timeout: Timeout values for cache expiration.
        :type timeout: dict
        :param directory: The directory to manage (default is the cache directory).
        :type directory: str, optional
        :param threshold_size: The threshold size in bytes (default is cache size limit * 1024 * 1024).
        :type threshold_size: int, optional
        :param cache_cleaning: Enable or disable cache cleaning (default is class's cache_cleaning attribute).
        :type cache_cleaning: bool, optional
        :raises ValueError: When the current directory size is not greater than the threshold size.
        :raises CacheCleaningDisabledError: When cache_cleaning is disabled.
        """
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
