from flask import Flask, render_template, request
import requests
app = Flask(__name__)
history = []  # In-memory list for demonstration purposes, replace with a database in production

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = 'd95d44fdc016cdf1ad21eb5bf2760280'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(weather_url)
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        icon_code = weather_data['weather'][0]['icon']

        # Add the city to the history
        history.append(city)

        return render_template('weather.html', city=city, temperature=temperature, description=description,
                                humidity=humidity, wind_speed=wind_speed, icon_code=icon_code)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/history')
def view_history():
    return render_template('history.html', history=history)

@app.route('/delete/<int:index>')
def delete_history(index):
    if 0 <= index < len(history):
        deleted_city = history.pop(index)
        return f'Deleted entry: {deleted_city}'
    else:
        return 'Invalid index'

if __name__ == '__main__':
    app.run(debug=True)
