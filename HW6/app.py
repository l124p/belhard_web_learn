from flask import Flask, request, render_template
from datetime import datetime
import asyncio
import os
import random
import string
from weather.weather import get_weather, get_weather_async

BASE_DIR = os.getcwd()

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"),
            template_folder=os.path.join(BASE_DIR, "templates")
            )
sec_key = "".join(random.sample(string.ascii_letters,20))
print(sec_key)
app.config['SECRET_KEY'] = sec_key

@app.route('/')
def index():
    with open('static/index.html', 'rb') as f:
        data = f.read()  
    return data


@app.route('/weather')
def weather():
    cities = ['Minsk', 'Brest', 'Grodno', 'Vitebsk', 'Gomel']
    city = request.args.get('city')
    if city == 'all' or city == None:
        data = {}
        response = asyncio.run(get_weather_async(cities))
        for item in response:
            print(item)
            data[item['city']] = {'temperatura': item['temp']}
            data[item['city']] = {'humidity': item['humidity']}
        print(data)    
        return render_template('weather.html  ', cities=cities, data=data)
    elif city.title() in cities:
        response = get_weather(city)
        cur_date = datetime.now().strftime('%d.%m.%y')
        print(cur_date)
        print(response)
        return render_template('weather.html', city=city, temperatura=response["temp"], humidity=response["humidity"], wind_speed=response["wind_speed"])
    else:
        with open('static/weather.html', 'rb') as f:
            data =f.read()
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

@app.route('/homework')
def homework():
    with open('static/homework/index.html', 'rb') as f:
        data =f.read()
    return data



if __name__ == '__main__':
    app.run(debug=True, port=5000)
