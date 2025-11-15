from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "f46995d31e6bf8086bc5f8338d39bd68"  # Replace with your actual API key

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing city parameter"}), 400
    
    try:
        # Get current weather directly
        current_url = "https://api.openweathermap.org/data/2.5/weather"
        current_params = {"q": city, "appid": API_KEY, "units": "metric"}
        current_resp = requests.get(current_url, params=current_params)
        
        if current_resp.status_code != 200:
            if current_resp.status_code == 404:
                return jsonify({"error": f"City '{city}' not found"}), 400
            elif current_resp.status_code == 401:
                return jsonify({"error": "Invalid API key. Please check your API key."}), 400
            else:
                return jsonify({"error": f"API error: {current_resp.status_code}"}), 400
        
        current_data = current_resp.json()
        
        # Extract coordinates for forecast
        lat, lon = current_data['coord']['lat'], current_data['coord']['lon']
        city_name = current_data['name']  # Use the name returned by API
        
        # Get forecast data
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        forecast_params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
        forecast_resp = requests.get(forecast_url, params=forecast_params)
        
        forecast_data = []
        if forecast_resp.status_code == 200:
            forecast_json = forecast_resp.json()
            # Group by day and get daily min/max temperatures
            daily_data = {}
            for item in forecast_json['list']:
                date_str = item['dt_txt'].split(' ')[0]  # Get date part (YYYY-MM-DD)
                temp = item['main']['temp']
                
                if date_str not in daily_data:
                    daily_data[date_str] = {
                        'date': item['dt'],
                        'temp_max': temp,
                        'temp_min': temp,
                        'condition': item['weather'][0]['description'].capitalize(),
                        'icon': item['weather'][0]['icon'],
                        'temps': [temp]
                    }
                else:
                    daily_data[date_str]['temps'].append(temp)
                    if temp > daily_data[date_str]['temp_max']:
                        daily_data[date_str]['temp_max'] = temp
                    if temp < daily_data[date_str]['temp_min']:
                        daily_data[date_str]['temp_min'] = temp
            
            # Convert to list and clean up (limit to 5 days as free API provides)
            for date_str in sorted(daily_data.keys())[:10]:  # Limit to 5 days
                day_data = daily_data[date_str]
                # Calculate average temp for the day
                day_data['temp'] = sum(day_data['temps']) / len(day_data['temps'])
                del day_data['temps']  # Remove the temps array
                forecast_data.append(day_data)
        
        result = {
            "current": {
                "city_name": city_name,
                "temp": current_data["main"]["temp"],
                "feels_like": current_data["main"]["feels_like"],
                "humidity": current_data["main"]["humidity"],
                "condition": current_data["weather"][0]["description"].capitalize(),
                "icon": current_data["weather"][0]["icon"]
            },
            "forecast": forecast_data
        }
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/')
def serve_index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)