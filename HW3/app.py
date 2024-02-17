from flask import Flask, request
from test import get_weather
from datetime import datetime

apikey = 'dbb4003ac34a3a47a2da0de9e73e2514'

app = Flask(__name__)


@app.route('/')
def index():
    city = 'minsk'
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': apikey, 'units': 'metric'}
    data = get_weather(url, params)
    cur_date = datetime.now().strftime('%d.%m.%y')
    print(cur_date)
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
