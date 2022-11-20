import sqlite3


def create_database() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users_meteo_data(
       cityname TEXT PRIMARY KEY,
       weather_ru TEXT,
       coord_ru_1 TEXT,
       coord_ru_2 TEXT,
       date TEXT,
       sunrise TEXT,
       sunset TEXT,
       tz TEXT,
       temp_now TEXT,
       feels_like TEXT);
    """)
    conn.commit()

    return conn
