import requests


def get_weather(url, params):
    res = requests.get(url, params)
    if res.status_code == 200:
        return res.json()
    return 'Error get data'


if __name__ == '__main__':

    url = 'https://api.openweathermap.org/data/2.5/weather?units=metric&q=London&appid=dbb4003ac34a3a47a2da0de9e73e2514'
    result = get_weather(url)
    print(result['main'])