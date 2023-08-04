import requests


class Weather:
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
        >>> weather1 = Weather(apikey="231432521352512355", city="Tampa, US")

    Example of creating a weather object using latitude and longitude coordinates:
        >>> weather2 = Weather(apikey="1234225325123523532", lat=41.4, lon=-23.4)

    To retrieve complete information regarding the next 12-hour forecast, use the following method:
        >>> weather1.next_12h()

    To get a simplified version of the data for the next 12 hours, you can use:
        >>> weather1.next12h_simplified()
    """
    def __init__(self, apikey, city=None, lat=None, lon=None, units="imperial"):
        """
        Initialize the Weather object.

        :param apikey: Your API key from openweathermap.org
        :type apikey: str
        :param city: Name of the city, default is None
        :type city: str, optional
        :param lat: Latitude coordinate, default is None
        :type lat: float, optional
        :param lon: Longitude coordinate, default is None
        :type lon: float, optional
        """
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},uk&APPID={apikey}&units={units}"
            r = requests.get(url)
            self.data = r.json()

        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={apikey}&units={units}"
            r = requests.get(url)
            self.data = r.json()

        else:
            raise TypeError("Provide either a city or lat and long arguments")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

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
            simple_data.append((dict_weather['dt_txt'], dict_weather['main']['temp'], dict_weather['weather'][0]['description']))
        return simple_data

