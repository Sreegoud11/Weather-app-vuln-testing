# app.py

from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    city = None
    weather_data = None
    image_url = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather_data(city)
            image_url = get_city_image(city)
    
    # If no city is provided or the form is not submitted, get the user's current location
    if not city:
        city = get_current_location()
        weather_data = get_weather_data(city)
        image_url = get_city_image(city)

    return render_template('index.html', weather_data=weather_data, city=city, image_url=image_url)

WEATHER_API = 'bad2dec2a15877bec3740a408fd10ea5'
PEXELS_API_KEY = 'W1TPkTujn9nx6LkDnKZ5c7DgZcHu6DpyP9I7rvJURSYSXZZMllq0lGki'  

def get_weather_data(city):
    api_key = WEATHER_API  
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['description'],
        }
        return weather_data
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        print(f"Response content: {response.content}")
        print(f"Status code: {response.status_code}")
        return None

def get_current_location():
    # Dummy default location (if geolocation is not supported or fails)
    default_location = 'New York'
    
    try:
        # Attempt to get the user's current location using browser's geolocation API
        if request.headers.get('host', '').startswith('localhost'):
            # Use a dummy location when running locally (geolocation is not supported in localhost)
            return default_location

        user_location_response = requests.get('https://ipinfo.io/json')
        user_location_data = user_location_response.json()

        # Extract city name from location data
        city = user_location_data.get('city', default_location)

        return city
    except requests.RequestException as e:
        print(f"Error getting user's location: {e}")
        return default_location

def get_city_image(city):
    try:
        # Use Pexels API to search for images related to the city
        pexels_url = f'https://api.pexels.com/v1/search?query={city}&per_page=1'
        headers = {'Authorization': PEXELS_API_KEY}
        response = requests.get(pexels_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract image URL from Pexels response
        if 'photos' in data and data['photos']:
            image_url = data['photos'][0]['src']['original']
            return image_url

        return None
    except requests.RequestException as e:
        print(f"Error fetching city image: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
