from flask import Flask, request, render_template, redirect
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
count_like = 0


@app.route('/')
def index():
    with open('static/index.html', 'rb') as f:
        data = f.read()  
    return data


@app.route('/weather')
def weather():
    cities = ['Minsk', 'Brest', 'Grodno', 'Vitebsk', 'Gomel']
    city = request.args.get('city')
    if not city:
        print("not city")
        data = {}
        response = asyncio.run(get_weather_async(cities))
        for item in response:
            print(item)
            data[item['city']] = {'temperatura': item['temp']}
            data[item['city']]['humidity'] = item['humidity']
            data[item['city']]["wind_speed"] = item['wind_speed']
        print(data)    
        return render_template('weather.html', cities=cities, data=data)
    elif city == 'all' or city.title() not in cities:
        print("all city")
        data = {}
        response = asyncio.run(get_weather_async(cities))
        for item in response:
            print(item)
            data[item['city']] = {'temperatura': item['temp']}
            data[item['city']]['humidity'] = item['humidity']
            data[item['city']]["wind_speed"] = item['wind_speed']
        print(data)    
        return render_template('weather.html', cities=cities, data=data)
    elif city.title() in cities:
        response = get_weather(city)
        cur_date = datetime.now().strftime('%d.%m.%y')
        print(cur_date)
        print(response)
        return render_template('weather.html', city=city, temperatura=response["temp"], humidity=response["humidity"], wind_speed=response["wind_speed"])

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


@app.route('/like', methods = ['GET', 'POST'])
def like_sum():
    print(request.method)
    global count_like
    if request.method == 'POST':
        print('количество:', request.form['count_like'])
        count_like += int(request.form['count_like']) 
    # if request.method == 'POST' and request.form['image.x']:
    #     print(request.form)
    #     count_like += 1
    return render_template('HW2/hw3.html', count_like=count_like)

@app.route('/form_zoo/', methods = ['GET', 'POST'])
def get_zoo():   
    return f'Данные отправлены'

@app.route('/form_date/', methods = ['GET', 'POST'])
def get_date():   
    return f'Данные отправлены'

@app.route('/modal/', methods = ['POST'])
def get_modal():
    print("Данные сохранены")   
    return redirect('/static/homework/HW3/hw3.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
