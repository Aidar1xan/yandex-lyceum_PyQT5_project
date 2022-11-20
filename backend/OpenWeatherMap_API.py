import config
import requests

from datetime import datetime as dt
from datetime import timezone, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_weather_data(city_name: str) -> list:
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?&lang=RU&q={city_name}&appid={config.API_KEY}", verify=False).json()

    weather_ru = 'Погода: ' + str(data['weather'][0]['description'])
    wind_ru = "Cкорость ветра в м/с: " + str(data['wind']['speed'])
    coord_ru_1 = "Долгота: " + str(data['coord']['lon'])
    coord_ru_2 = "Широта: " + str(data['coord']['lat'])
    date = "Дата: " + str(dt.utcfromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d'))
    sunrise = "Время рассвета: " + str(dt.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'))
    sunset = "Время заката: " + str(dt.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'))
    tz = "Часовой пояс: " + str(timezone(timedelta(seconds=data['timezone'])))
    temp_now = "Температура: " + str(int(data['main']['temp'] - 273.15))
    feels_like = "Ощущается как: " + str(int(data['main']['feels_like'] - 273.15))

    return [weather_ru,
            wind_ru,
            coord_ru_1,
            coord_ru_2,
            date,
            sunrise,
            sunset,
            tz,
            temp_now,
            feels_like]
