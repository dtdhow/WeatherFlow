from anyio import current_effective_deadline
from flask import Flask, render_template, redirect, url_for, request
from markupsafe import escape
import dotenv
import requests
from flask_caching import Cache

PATH_ENV = ".env"

apikey = dotenv.get_key(PATH_ENV, "APIKEY")
BASE_URL = "http://api.weatherapi.com/v1"

app = Flask(__name__)

# Конфигурация кэширования
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 600  # 10 минут

cache = Cache(app)

def parse_weather_data(data):
    if not data:
        return None

    location = data['location']
    current = data['current']
    forecast = data['forecast']

    return {
        'city': location['name'],
        'country': location['country'],
        'temperature': current['temp_c'],
        'condition': current['condition']['text'],
        'condition_icon': current['condition']['icon'],
        'humidity': current['humidity'],
        'wind_speed': current['wind_kph'],
        'wind_dir': current["wind_dir"],
        'vis_km': current["vis_km"],
        "pressure": current["pressure_mb"],
        "precip": current["precip_mm"],
        "uv": current["uv"],
        "gust": current["gust_kph"],

        'feels_like': current['feelslike_c'],

        'forecast': forecast,
    }


def get_weather_data(city):
    url = f"{BASE_URL}/forecast.json"
    params = {
        'key': apikey,
        'q': city,
        'lang': 'ru',
        'day': 7,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

@app.route("/")
def base():
    return redirect(url_for("index"))

@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/weather/")
def weather():
    city = request.args.get("city")

    if not city:
        return "Ошибка: не указан город"

    weather_data = get_weather_data(escape(city))

    if not weather_data:
        return "Ошибка: не удалось получить данные о погоде"

    parsed_data = parse_weather_data(weather_data)

    if not parsed_data:
        return "Ошибка: город не найден"

    return render_template("weather.html", weather=parsed_data)

@app.route("/about/")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
