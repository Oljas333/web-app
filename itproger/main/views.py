from django.shortcuts import render


def index(request):
    weather_api_key = 'e1b9079f105bdb7e3abaabfe82dcf8a8'
    weather_city = 'Almaty'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={weather_city}&appid={weather_api_key}&units=metric'

    try:
        response_weather = requests.get(weather_url)
        response_weather.raise_for_status()
        weather_data = response_weather.json()
        logger.info(f"Weather API response: {weather_data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API error: {e}")
        weather_data = None

    currency_url = 'https://api.exchangerate-api.com/v4/latest/USD'
    try:
        response_currency = requests.get(currency_url)
        response_currency.raise_for_status()
        currency_data = response_currency.json()
        logger.info(f"Currency API response: {currency_data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Currency API error: {e}")
        currency_data = None

    context = {
        'weather': weather_data,
        'currency': currency_data,
    }
    return render(request, 'main/index.html', context)


def about(request):
    print(request.GET)
    if request.method == "post":
        print(request.POST)

    return render(request, 'main/about.html')


def contacs(request):
    data = {
        'title': 'Контакты',
    }
    return render(request, 'main/contacs.html', data)

import logging
import requests

logger = logging.getLogger(__name__)


def weather(request):
    weather_api_key = 'e1b9079f105bdb7e3abaabfe82dcf8a8'
    city = request.GET.get('city', 'Almaty')
    weather_data = {}
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'

    try:
        response_weather = requests.get(weather_url)
        response_weather.raise_for_status()
        weather_data = response_weather.json()
    except requests.exceptions.RequestException as e:
        weather_data['error'] = 'Error fetching weather data'

    return render(request, 'main/index.html', {'weather_data': weather_data})


def currency(request):
    base_currency = request.GET.get('base', 'USD')
    currencies_to_display = request.GET.get('currencies', '').split(',')
    currencies_to_display = [currency.strip() for currency in currencies_to_display]
    currency_url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
    try:
        response_currency = requests.get(currency_url)
        response_currency.raise_for_status()
        currency_data = response_currency.json()
        logger.info(f"Ответ от API валют: {currency_data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API валют: {e}")
        currency_data = None

    if currency_data:
        all_rates = currency_data.get('rates', {})
        filtered_rates = {currency: all_rates[currency] for currency in currencies_to_display if currency in all_rates}

        context = {
            'base_currency': base_currency,
            'rates': filtered_rates,
            'currencies_to_display': currencies_to_display
        }
    else:
        context = {
            'error': 'Не удалось получить данные о валюте.'
        }
    return render(request, 'main/index.html', context)