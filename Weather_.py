import json
import requests
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

def get_weather_data(api_key, city_name):
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error: {response.status_code}")
        return None

def insert_weather_data_into_mysql(data, city_name, db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO weather_data (data, city_name) VALUES (%s, %s)"
            data_to_insert = (json.dumps(data), city_name)
            cursor.execute(insert_query, data_to_insert)

        connection.commit()
        logging.info("Weather data inserted into MySQL database")

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()

def save_to_database(data, db_config,city_name):
    try:
        connection = mysql.connector.connect(**db_config)
        with connection.cursor() as cursor:
            for entry in data['list']:
                # Extract data from the JSON response
                dt = entry['dt']
                temp = entry['main']['temp']
                feels_like = entry['main']['feels_like']
                humidity = entry['main']['humidity']
                weather_description = entry['weather'][0]['description']
                wind_speed = entry['wind']['speed']
                dt_txt = entry['dt_txt']



                # Parameterized SQL query
                sql = """
                    INSERT INTO weather_data (dt, temp, feels_like, humidity, weather_description, wind_speed, dt_txt,city)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
                """

                values = (dt, temp, feels_like, humidity, weather_description, wind_speed, dt_txt,city_name)
                cursor.execute(sql, values)

        connection.commit()
        logging.info("Weather data saved to MySQL database")

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()

def main():
    api_key = '1264bc21f1c4df8b83fc1febd5d727b5'  # Replace with your actual API key
    city_name = input("Enter a city name: ")

    weather_data = get_weather_data(api_key, city_name)

    if weather_data:
        print(json.dumps(weather_data, indent=2))  # Pretty-print JSON data
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'tabs1234',
            'database': 'ETL'
        }
        save_to_database(weather_data, db_config,city_name)

if __name__ == "__main__":
    main()
