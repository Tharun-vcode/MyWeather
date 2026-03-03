from flask import Flask, request, jsonify, render_template
from services.weather_service import fetch_weather
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/weather')
def weather():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Missing city parameter"}), 400

    data, status = fetch_weather(city)

    if status != 200:
        if status == 404:
            return jsonify({"error": f"City '{city}' not found"}), 400
        elif status == 401:
            return jsonify({"error": "Invalid API key"}), 400
        else:
            return jsonify({"error": "External API error"}), 500

    return jsonify(data)


@app.route('/')
def serve_index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
