import geocoder
import ipinfo
import requests


class LocationError(Exception):
    pass


class LocationTrack:

    def __init__(self, track_location=True, **kwargs):
        self.city = None
        self.state = None
        self.country = None
        self.latitude = None
        self.longitude = None
        self.zip_code = None
        self.timezone = None
        self.kwargs = kwargs

        if type(track_location) is bool:
            if track_location:
                self.get_location_info()
            else:
                raise LocationError("track_location is False.")
        else:
            raise TypeError("track_location must be bool.")

    def get_location_info(self):
        try:
            # First, try using the 'requests' library and IP geolocation API
            if 'ipinfo_token' in self.kwargs:
                try:
                    access_token = self.kwargs['ipinfo_token']
                    handler = ipinfo.getHandler(access_token)
                    details = handler.getDetails()
                    self.city = details.city
                    self.state = details.region
                    self.country = details.country
                    self.latitude = details.latitude
                    self.longitude = details.longitude
                    self.zip_code = details.postal
                    self.timezone = details.timezone

                except requests.exceptions.HTTPError:
                    raise "Invalid ipinfo_token, please check it or remove to try another location tracking."

            else:
                response = requests.get('https://ipinfo.io/json')
                loc_data = response.json()
                self.city = loc_data['city']
                self.state = loc_data['region']
                self.country = loc_data['country']
                self.latitude = loc_data['loc'].split(',')[0]
                self.longitude = loc_data['loc'].split(',')[1]
                self.zip_code = loc_data['postal']
                self.timezone = loc_data['timezone']

        except requests.exceptions.RequestException as e:
            try:
                # If the first method fails, try using the 'geocoder' library
                g = geocoder.ip('me')
                loc_data = g.geojson
                self.city = loc_data['features'][0]['properties']['city']
                self.state = loc_data['features'][0]['properties']['state']
                self.country = loc_data['features'][0]['properties']['country']
                self.latitude = loc_data['features'][0]['properties']['lat']
                self.longitude = loc_data['features'][0]['properties']['lng']
                self.zip_code = loc_data['features'][0]['properties']['postal']
                self.timezone = loc_data['features'][0]['properties']['timezone']

            except Exception as e:
                return LocationError(e, "Failed to retrieve location information automatically")

    def loc_info_dict(self):
        loc_dict = {
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'zip_code': self.zip_code,
            'timezone': self.timezone
        }
        return loc_dict
