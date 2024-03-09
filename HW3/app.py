from flask import Flask, request
from datetime import datetime
import asyncio
<<<<<<< HEAD
from HW3.weather.weather import get_weather, get_weather_async
=======
from weather.weather import get_weather, get_weather_async
>>>>>>> 3e061176c53b5ea080bef49e101d52f7329faa95

app = Flask(__name__)


@app.route('/')
def index():
    with open('index.html', 'rb') as f:
        return f.read()


@app.route('/weather')
def weather():
    cities = ['minsk', 'brest', 'grodno', 'vitebsk', 'gomel']
    city = request.args.get('city', 'minsk')
    out = ''.encode('utf-8')
    if city == 'Все города':
        response = asyncio.run(get_weather_async(cities))
        for item in response:
<<<<<<< HEAD
            out += f'<p>В городе <b>{item['city']}</b> температура воздуха составляет <b>{item['temp']}</b> градусов</p>'.encode('utf-8')
=======
            out += f'<p>В городе <b>{item["city"]}</b> температура воздуха составляет <b>{item["temp"]}</b> градусов</p>'.encode('utf-8')
>>>>>>> 3e061176c53b5ea080bef49e101d52f7329faa95
        #for city in cities:
            #response = asyncio.run(get_weather_async(city))
            #print(response)
            #out += f'<p>В городе <b>{response['city']}</b> температура воздуха составляет <b>{response['temp']}</b> градусов</p>'.encode('utf-8')
<<<<<<< HEAD
        with open('weather/index.html', 'rb') as f:
            data = f.read()
=======
        with open('weather/index.html', 'rb') as file:
            data = file.read()
>>>>>>> 3e061176c53b5ea080bef49e101d52f7329faa95
            data += bytes(out)
        return data
    else:
        response = get_weather(city)
        cur_date = datetime.now().strftime('%d.%m.%y')
        print(cur_date)
        print(response)
        with open('weather/index.html', 'rb') as f:
            data = f.read()
<<<<<<< HEAD
            out = f'<p>В городе <b>{response['city']}</b> температура воздуха составляет <b>{response['temp']}</b> градусов</p>'.encode('utf-8')
=======
            out = f'<p>В городе <b>{response["city"]}</b> температура воздуха составляет <b>{response["temp"]}</b> градусов</p>'.encode('utf-8')
>>>>>>> 3e061176c53b5ea080bef49e101d52f7329faa95
            data += bytes(out)
        return data


@app.route('/news')
def news():
    colors = ['blue', 'green', 'red', 'black']
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = 10

    color = request.args.get('color') if request.args.get('color') in colors else 'black'
    return f'<h1 style="color: {color}"> News: {limit}<h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
