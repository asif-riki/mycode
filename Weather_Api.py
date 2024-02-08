import json
import requests

def get_weather_data(api_key, city_name):
    base_url='http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    api_key = '1264bc21f1c4df8b83fc1febd5d727b5'  # Replace with your actual API key
    city_name = input("Enter a city name: ")

    weather_data = get_weather_data(api_key, city_name)

    if weather_data:
        print(json.dumps(weather_data, indent=2))  # Pretty-print JSON data

if __name__ == "__main__":
    main()
