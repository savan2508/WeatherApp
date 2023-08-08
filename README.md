# weathermap

The weathermap package aims to aid users in getting necessary weather information in a simplified way, making it easy to integrate into various development projects where weather data is needed. The project can be accessed on PyPI [here](https://pypi.org/project/weathermap/), and the GitHub repository is available [here](https://github.com/savan2508/WeatherApp).

Now the weathermap Library provides functionality for tracking geographical location based on user IP address and caching weather data to reduce API calls.

## Project Overview

The weathermap package version 1.0.7 is stable version, and its primary goal is to provide users with easy access to weather data as long as they have an API key from openweathermap.org. Acquiring the API key is straightforward and should be ready to use within two hours, after which this library becomes accessible for use.

## Acquiring the API Key

To use the Weather package, you'll need an API key from openweathermap.org. Follow these steps to obtain a free API key:

1. Go to [openweathermap.org](https://openweathermap.org/api) and create an account.
2. After successfully creating the account, log in to your account.
3. Once logged in, navigate to the API keys section.
4. Generate a new API key by following the provided instructions.
5. Make sure to copy the generated API key, as it will be required to create a Weather object.

## Installation

You can install the package using pip:

```bash
pip install weathermap
```

## Key Features

- Simplified Weather Data: Instead of overwhelming users with excessive data, the Weather package provides only the necessary weather information that users require.
- Flexible Use Cases: This library can be utilized in various scenarios, especially when users are developing programs that rely on different weather information for cities or specific latitude and longitude coordinates.
- Easy Data Access: The primary objective of the project is to allow users to create instances for different cities, and then easily access various weather information using different methods.
- Location tracking based on the user's IP address.
- Caching weather data to minimize API calls and improve performance.
- Support for various API endpoints, such as weather, forecast, and air pollution.
- Easily configurable timeout intervals for cached data.
- Compatibility with both IP geolocation services and the 'geocoder' library.
- Planned support for future features, including more information extraction from the API and compatibility with the One Call API version 3.0.

## Contributing
We welcome contributions to the Weather Information Library! Feel free to submit issues, feature requests, or pull requests on the GitHub repository.

## Usage
Here's an example of how to use the Weather Information Library:
```python
from weathermap import Weather

# Initialize Weather with location information
weather_info = Weather(apikey='YOUR_API_KEY', city="Tampa", state="Florida", country="US")

# Initialize Weather without location to enable location tracking
weather_info_for_current_ip = Weather(apikey='YOUR_API_KEY')

# Retrieve weather information
current_weather = weather_info.get_current_weather()
forecast = weather_info.get_forecast()

print("Current Weather:", current_weather)
print("Forecast:", forecast)
```

## Use Cases

The Weather Information Library offers versatile functionality that can be integrated into various applications and platforms to provide real-time weather data and enhance user experiences. Some potential use cases include:

### Weather Updates on Websites

By integrating the Weather Information Library into your website, you can easily provide visitors with up-to-date weather conditions based on their geographical location. This is particularly useful for travel, tourism, and outdoor event websites. Users can quickly access weather information relevant to their location, enabling them to plan their activities more effectively.

### Event Ticket Booking Platforms

Event ticket booking platforms can benefit from the Weather Information Library by offering forecast weather data for the dates of scheduled events. This helps attendees and travelers make informed decisions about attending outdoor events, concerts, festivals, or sports games, considering the weather conditions.

### Travel Planning Applications

Travel planning applications can use the library to display weather forecasts for the chosen travel destination. Travelers can prepare for their trips by knowing the expected weather conditions during their stay, ensuring they pack appropriately and plan outdoor activities accordingly.

### Location-Based Recommendations

Applications that provide location-based recommendations, such as local restaurants, attractions, and activities, can leverage the Weather Information Library to offer more tailored suggestions. By considering the weather conditions, these apps can suggest indoor or outdoor options that align with the user's preferences and the current weather.

### IoT and Smart Home Integration

Internet of Things (IoT) devices and smart home systems can use the Weather Information Library to enhance their capabilities. For example, a smart sprinkler system can adjust watering schedules based on upcoming rainfall predictions, optimizing water usage and promoting eco-friendly practices.

### Outdoor Event Management

Organizers of outdoor events, such as music festivals, markets, or fairs, can utilize the library to monitor weather forecasts and make real-time decisions regarding event logistics. By staying informed about weather changes, event planners can ensure the safety and comfort of attendees.

### Digital Signage and Displays

Digital signage solutions in public spaces, transportation hubs, and retail environments can provide localized weather updates using the Weather Information Library. This information can be valuable to commuters, shoppers, and tourists passing through these areas.

These are just a few examples of how the Weather Information Library can enhance applications and platforms by providing accurate and relevant weather data. As the library continues to evolve, more opportunities for integration and innovation will emerge.


## Release Notes

### Version 1.0.7

- Added location tracking based on user IP address using IP geolocation services and the 'geocoder' library.
- Implemented caching system to reduce API calls and improve performance.
- Support for various API endpoints, including weather, forecast, and air pollution.
- Added timeout interval configuration for cached data.
- Improved error handling and robustness.
- Compatibility with both IP geolocation services and the 'geocoder' library.
- Bug fixes. 

### Version 1.0.6

- Initial release of the Weather Information Library.
- Basic functionality for retrieving weather data using OpenWeatherMap API.
- Support for forecast data.
- Minimal error handling and configurability.

## Planned Features for Future Versions

In future versions of the Weather Information Library, we plan to introduce the following enhancements:

- More comprehensive information extraction from API responses.
- Compatibility with the One Call API version 3.0 for a consolidated weather data solution.
- Enhanced error handling and error messages.
- Additional API endpoints and weather-related functionalities.
- Integration with popular Python libraries for data visualization.
- Improved documentation and usage examples.

Stay tuned for updates and new releases as we continue to enhance the Weather Information Library!
With this package, developers can effortlessly integrate weather data into their projects, making it a valuable tool for a wide range of applications.

## License
This project is licensed under the MIT License.

---
For more information and updates, visit the project on [PyPI](https://pypi.org/project/weathermap/) or check out the [GitHub repository](https://github.com/savan2508/WeatherApp).
