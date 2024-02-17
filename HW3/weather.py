import requests

apikey = 'dbb4003ac34a3a47a2da0de9e73e2514'


def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': apikey, 'units': 'metric'}
    res = requests.get(url, params)
    if res.status_code == 200:
        return res.json()['main']['temp']
    return 'Error get data'
