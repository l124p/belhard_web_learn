from flask import Flask, request
from weather import get_weather
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    with open('index.html', 'rb') as f:
        return f.read()


@app.route('/weather')
def weather():
    city = 'minsk'
    temp = get_weather(city)
    cur_date = datetime.now().strftime('%d.%m.%y')
    print(cur_date)
    return f'<h1>City: {city}</h1> <p>Temp: {temp}</p>'


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
