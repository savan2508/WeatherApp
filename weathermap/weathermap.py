import requests
from .WeatherCache import WeatherCache
from .locationtrack import LocationTrack


class Weather(WeatherCache, LocationTrack):
    """
    Weather Class:

    This class allows you to create a weather object by providing an API key along with either a city name or
    latitude and longitude coordinates.
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

    def __init__(self, apikey: str, city: str = None, lat: float = None, lon: float = None, **kwargs):
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
        must provide either city or latitude and longitude or zipcode and country code
        """
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast?"
        self.city = city.strip() if city is not None else None
        self.apikey = apikey
        self.lat = str(lat) if lat is not None else None
        self.lon = str(lon) if lon is not None else None
        self.zip = None
        self.country = None
        self.data = None
        self.state = None
        self.units = "Imperial"
        self.cache_system = True
        self.forcast_timeout = "1D"
        self.weather_timeout = "1H"
        self.track_location = True
        self.kwargs = kwargs

        if 'zip' in kwargs:
            self.zip = str(kwargs['zip']).strip()
            del kwargs['zip']
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
        if 'track_location' in kwargs:
            self.track_location = kwargs['track_location']

        super().__init__(self.cache_system, **kwargs)
        super(LocationTrack, self).__init__(tracking=self.track_location)
        self._validate_input()

    def _validate_input(self):
        if not self.apikey:
            raise ValueError("API key is required.")

        if type(self.track_location) == bool:
            if self.track_location:
                self.get_location_info()
        else:
            raise ValueError ("track_location must be bool")

        if not any([self.city, (self.lat and self.lon), (self.zip and self.country)]):
            if ((self.lat or self.lon) and self.zip is None and self.country is None
                    and self.city is None):
                raise ValueError("Please provide valid latitude and longitude values")
            elif (self.zip or self.country) and (self.lat and self.lon and self.city) is None:
                raise ValueError("Please provide valid zip and county code values")
            else:
                raise ValueError("You must provide either city or latitude and longitude or zipcode and country code.")



    def forcast(self):
        # if self.city:
        #     if self.city and self.state and self.country:
        #         url = f"{self.base_url}q={self.city},{self.state},{self.country}&APPID={self.apikey}&units={self.units}"
        #         r = requests.get(url.strip())
        #         self.data = r.json()
        #
        #     elif self.city and self.country:
        #         url = f"{self.base_url}q={self.city},{self.country}&APPID={self.apikey}&units={self.units}"
        #         r = requests.get(url.strip())
        #         self.data = r.json()
        #
        #     else:
        #         url = f"{self.base_url}q={self.city}&APPID={self.apikey}&units={self.units}"
        #         r = requests.get(url.strip())
        #         self.data = r.json()
        #
        #         if self.data["cod"] != "200":
        #             raise ValueError(self.data["message"], "Check spelling or provide state and country code, "
        #                                                    "or try zipcode and country.")
        #
        # elif self.lat and self.lon:
        #
        #     url = f"{self.base_url}lat={self.lat}&lon={self.lon}&APPID={self.apikey}&units={self.units}"
        #     r = requests.get(url.strip())
        #     self.data = r.json()
        #
        #     if self.data["cod"] != "200":
        #         raise ValueError(self.data["message"], "Please provide valid latitude and longitude value")
        #
        # elif self.zip and self.country:
        #
        #     url = f"{self.base_url}zip={self.zip},{self.country}&APPID={self.apikey}&units={self.units}"
        #     r = requests.get(url.strip())
        #     self.data = r.json()
        #
        #     if self.data["cod"] != "200":
        #         raise ValueError(self.data["message"], "Please provide valid zipcode and country code.")
        # #
        # #     except AttributeError:
        # #         raise TypeError("Provide either a city or lat and long arguments")
        #
        # if self.data["cod"] != "200":
        #     raise ValueError(self.data["message"])
        testdata = {"app": 1, "man": 2}
        self.data = testdata
        self.create_cache(city="Tampa", data=testdata)

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
