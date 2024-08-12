import requests

weather_api_key = 'e1b9079f105bdb7e3abaabfe82dcf8a8'
weather_city = 'Almaty'
weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={weather_city}&appid={weather_api_key}&units=metric'

try:
    response_weather = requests.get(weather_url)
    response_weather.raise_for_status()
    weather_data = response_weather.json()
    print(weather_data)
except requests.exceptions.RequestException as e:
    print(f"Weather API error: {e}")
    weather_data = None

