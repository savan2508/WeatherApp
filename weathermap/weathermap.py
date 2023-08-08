import re

import requests
from .WeatherCache import WeatherCache
from .locationtrack import LocationTrack, LocationError


class Weather(WeatherCache, LocationTrack):
    """
    Weather Class:

    This class allows you to create a weather object by providing an API key along with either a city name or
    latitude and longitude coordinates.
    Weather class can only be run by providing the api key only. It will track the location of the computer based on
    the IP address.

    The Weather class has an additional functionality that supports the cache system. It is enabled by default, and it
    helps reduce the similar API calls to help decrease the cost.

    To use the class, you'll need an API key from openweathermap.org.

    Follow the steps below to obtain a free API key:

    1. Go to openweathermap.org and create an account.
    2. After successfully creating the account, log in to your account.
    3. Once logged in, navigate to the API keys section.
    4. Generate a new API key by following the provided instructions.
    5. Make sure to copy the generated API key, as it will be required to create a Weather object.

    Example of creating a weather object using a city name and API key:
        weather1 = Weather(apikey="231432521352512355", city="Tampa, US")

    Example of creating a weather object using latitude and longitude coordinates:
        weather2 = Weather(apikey="1234225325123523532", lat=41.4, lon=-23.4)

    To retrieve complete information regarding the next 12-hour forecast, use the following method:
        weather1.next_12h()

    To get a simplified version of the data for the next 12 hours, you can use:
        weather1.next12h_simplified()
    """

    def __init__(self, apikey: str, city: str = None, lat: float = None, lon: float = None,
                 req_type: str = "weather", **kwargs):
        """
        Initialize the Weather object.

        :param apikey: Your API key from openweathermap.org
        :type apikey: str
        :param city: Name of the city, default is None
        :type city: str
        :param lat: Latitude coordinate, default is None
        :type lat: float
        :param lon: Longitude coordinate, default is None
        :type lon: float
        :param req_type: "weather" for current weather, "forcast" for forcast, "air_pollution" for air pollution,
        default is weather
        :type lon: str (weather or forcast)
        must provide either city or latitude and longitude or zipcode and country code.

        Weather instance inherits LocationTrack module which can detect the location of the user based on the user IP.
        If value for the city, zip_code or lat and long is provided, it will disable the location tracking. It can be
        re-enabled by providing the argument track_location=True. (IMPORTANT - by enabling the location tracking, it
        will overwrite the provided inputs of the city, state, country, zip_code, latitude and longitude values. The
        LocationTrack function tracks the location of the user by IP address which may not be accurate location. Please
        consider that the incorrect location may provide you inaccurate weather data.)

        By default, the cache system is turned on which helps reduce the API calls to save cost. It can be disabled by
        providing the kwargs cache_system=False. It is recommended to use a cache system. The timeout inputs can be
        modified to control the frequency and longevity of the cache.
        :keyword forcast_timeout, default is "1D" which is 1 day.
        :keyword weather_timeout, default is "1H" which is 1 hour.
        type: str which must be inputted as value of the unit as integer + first letter of units such as M for minutes,
        H for hours, D for days. for example, 1D for 1 day, 5M for 5 minutes, 3H for 3 hours, etc.

        """
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.city = city.strip() if city is not None else None
        self.apikey = apikey
        self.lat = str(lat) if lat is not None else None
        self.lon = str(lon) if lon is not None else None
        self.zip_code = None
        self.country = None
        self.data = None
        self.state = None
        self.units = "Imperial"
        self.cache_system = True
        self.forcast_timeout = "1D"
        self.weather_timeout = "1H"
        self.air_pollution_timeout = "1D"
        self.track_location = True
        self.kwargs = kwargs
        self.enable_cache = True
        self.req_type = req_type

        if 'zip_code' in kwargs:
            self.zip_code = str(kwargs['zip_code']).strip()
            del kwargs['zip_code']
        if 'country' in kwargs:
            self.country = kwargs['country'].strip()
            del kwargs['country']
        if 'units' in kwargs:
            self.units = kwargs['units'].strip()
            del kwargs['units']
        if 'state' in kwargs:
            self.state = kwargs['state'].strip()
            del kwargs['state']
        if 'cache_system' in kwargs:
            self.cache_system = kwargs['cache_system']
            del kwargs['cache_system']

        if self.city or self.zip_code or self.lon or self.lat:
            self.track_location = False

        if 'track_location' in kwargs:
            self.track_location = kwargs['track_location']

        if self.cache_system:
            WeatherCache.__init__(self, cache_system=self.cache_system, cache_directory='weather_cache', **kwargs)
        if self.track_location:
            LocationTrack.__init__(self, track_location=self.track_location, **kwargs)

        self._validate_input()

    def _validate_input(self):
        if not self.apikey:
            raise ValueError("API key is required.")

        if self.req_type not in ["weather", "forcast", "air_pollution"]:
            raise ValueError("req_type must be weather or forcast")

        try:
            if type(self.track_location) == bool:
                if self.track_location:
                    location = LocationTrack()
                    self.city = location.city.strip()
                    self.state = location.state.strip()
                    self.country = location.country.strip()
            else:
                raise ValueError("track_location must be bool")

        except LocationError or ValueError:
            if not any([self.city, (self.lat and self.lon), (self.zip_code and self.country)]):
                if ((self.lat or self.lon) and self.zip_code is None and self.country is None
                        and self.city is None):
                    raise ValueError("Please provide valid latitude and longitude values")
                elif (self.zip_code or self.country) and (self.lat and self.lon and self.city) is None:
                    raise ValueError("Please provide valid zip_code and county code values")
                else:
                    raise ValueError("Must provide either city or latitude and longitude or zipcode and country "
                                     "code.")

    def api_request(self, req_type=None):
        if req_type:
            self.req_type = req_type

        try:
            if self.req_type == "weather":
                timeout_param = self.timeout_time_clean(timeout=self.weather_timeout)
                self.data = self.get_cached_weather(timeout=timeout_param, req_type=self.req_type, city=self.city,
                                                    state=self.state, country=self.country, lat=self.lat, lon=self.lon)
                if self.data["cod"] != "200":
                    raise FileNotFoundError(self.data["message"])
                else:
                    return self.data
            elif self.req_type == "forcast":
                timeout_param = self.timeout_time_clean(timeout=self.forcast_timeout)
                self.data = self.get_cached_weather(timeout=timeout_param, req_type=self.req_type, city=self.city,
                                                    state=self.state, country=self.country, lat=self.lat, lon=self.lon)
                if self.data["cod"] != "200":
                    raise FileNotFoundError(self.data["message"])
                else:
                    return self.data
            elif self.req_type == "air_pollution":
                timeout_param = self.timeout_time_clean(timeout=self.forcast_timeout)
                self.data = self.get_cached_weather(timeout=timeout_param, req_type=self.req_type, city=self.city,
                                                    state=self.state, country=self.country, lat=self.lat, lon=self.lon)
                if self.data["cod"] != "200":
                    raise FileNotFoundError(self.data["message"])
                else:
                    return self.data
            else:
                raise ValueError("Provide valid req_type. ['weather', 'forcast', 'air_pollution']")

        except OSError or FileNotFoundError:
            if self.city:
                if self.city and self.state and self.country:
                    url = (f"{self.base_url}forecast?q={self.city},{self.state},{self.country}&APPID="
                           f"{self.apikey}&units={self.units}")
                    r = requests.get(url.strip())
                    self.data = r.json()
                    if self.data["cod"] == "200":
                        try:
                            self.create_cache(data=r.json(), city=self.city, state=self.state, country=self.country,
                                              req_type=self.req_type)
                        except OSError:
                            self.data = r.json()

                elif self.city and self.country:
                    url = f"{self.base_url}forecast?q={self.city},{self.country}&APPID={self.apikey}&units={self.units}"
                    r = requests.get(url.strip())
                    self.data = r.json()
                    if self.data["cod"] == "200":
                        try:
                            self.create_cache(data=r.json(), city=self.city, state=self.state, country=self.country,
                                              req_type=self.req_type)
                        except OSError:
                            self.data = r.json()
                else:
                    url = f"{self.base_url}forecast?q={self.city}&APPID={self.apikey}&units={self.units}"
                    r = requests.get(url.strip())
                    self.data = r.json()
                    if self.data["cod"] == "200":
                        try:
                            self.create_cache(data=r.json(), city=self.city, state=self.state, country=self.country,
                                              req_type=self.req_type)
                        except OSError:

                            self.data = r.json()

                    if self.data["cod"] != "200":
                        raise ValueError(self.data["message"], "Check spelling or provide state and country code, "
                                                               "or try zipcode and country.")

            elif self.lat and self.lon:

                url = f"{self.base_url}forecast?lat={self.lat}&lon={self.lon}&APPID={self.apikey}&units={self.units}"
                r = requests.get(url.strip())
                self.data = r.json()

                if self.data["cod"] != "200":
                    raise ValueError(self.data["message"], "Please provide valid latitude and longitude value")

            elif self.zip_code and self.country:

                url = (f"{self.base_url}forecast?zip_code={self.zip_code},{self.country}&"
                       f"APPID={self.apikey}&units={self.units}")
                r = requests.get(url.strip())
                self.data = r.json()

                if self.data["cod"] != "200":
                    raise ValueError(self.data["message"], "Please provide valid zipcode and country code.")

            else:
                raise AttributeError("Not enough arguments provided to provide weather information.")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])
        else:
            return self.data

    def next_12h(self):
        """
        Get complete information regarding the next 12-hour forecast.
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """
        Get a simplified version of the data for the next 12 hours.
        """
        simple_data = []
        for dict_weather in self.data['list'][:4]:
            simple_data.append((dict_weather['dt_txt'], dict_weather['main']['temp'],
                                dict_weather['weather'][0]['description']))
        return simple_data

    def timeout_time_clean(self, timeout):
        output = {
            'req_type': self.req_type,
            'forcast_timeout': {
                'seconds': 0,
                "minutes": 0,
                "hours": 0,
                "days": 0
            },
            'weather_timeout': {
                'seconds': 0,
                "minutes": 0,
                "hours": 0,
                "days": 0
            },
            'air_pollution_timeout': {
                'seconds': 0,
                "minutes": 0,
                "hours": 0,
                "days": 0
            }
        }
        placeholder = ''
        if output['req_type'] == 'weather':
            placeholder = 'weather_timeout'
        elif output['req_type'] == 'forcast':
            placeholder = 'forcast_timeout'
        elif output['req_type'] == 'air_pollution':
            placeholder = 'air_pollution_timeout'
        else:
            raise ValueError("Please provide correct req_type")

        match = re.match(r'^\d+\s*[a-zA-Z]+$', timeout)
        if match:
            match = re.search(r'\d+', timeout)
            if match:
                # Extract the number part
                number = int(match.group())
                # Extract the character part (if any)
                characters = timeout[match.end():].strip()
                if characters[0].upper() == 'S':
                    output[placeholder]["seconds"] = number
                elif characters[0].upper() == 'M':
                    output[placeholder]["minutes"] = number
                elif characters[0].upper() == 'H':
                    output[placeholder]["hours"] = number
                elif characters[0].upper() == 'D':
                    output[placeholder]["days"] = number
                else:
                    raise ValueError("Please provide a valid timeout interval")

                return output
            else:
                raise ValueError("Please provide valid time interval")

        else:
            raise ValueError("Please provide a valid timeout interval")
