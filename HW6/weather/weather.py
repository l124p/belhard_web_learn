import asyncio
import requests
from aiohttp import ClientSession
import time

apikey = 'dbb4003ac34a3a47a2da0de9e73e2514'


def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': apikey, 'units': 'metric'}
    rez = requests.get(url, params)
    if rez.status_code == 200:
        return {'city': city, 'temp': rez.json()['main']['temp']}
    return 'Error get data'


async def task_get_weather_async(city):
    async with ClientSession() as sesion:
        url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'appid': apikey, 'units': 'metric'}
        async with sesion.get(url=url, params=params) as respons:
            rez = await respons.json()
            return {'city': city, 'temp': rez['main']['temp']}


async def get_weather_async(cities_):
    tasks = []
    result = []
    for city in cities_:
        tasks.append(asyncio.create_task(task_get_weather_async(city)))
    for task in tasks:
        result.append(await task)
    return result



