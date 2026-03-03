# 🌤️ MyWeather – Full-Stack Weather Forecasting Application

MyWeather is a production-style Flask web application that provides real-time weather data using the OpenWeather API.  
It is designed with clean backend architecture, service-layer separation, structured error handling, environment-based configuration, caching, and cloud deployment.

This project demonstrates practical backend engineering principles used in real-world applications.

---

# 🚀 Live Demo

Deployed on Render  
https://myweather-gc2b.onrender.com/

---

# Screen Shots 

<img width="1897" height="1003" alt="image" src="https://github.com/user-attachments/assets/003f4e6a-9fff-4eaf-9277-0bf8d034e561" />
<img width="1894" height="995" alt="image" src="https://github.com/user-attachments/assets/9b0f4fd2-34ab-49ac-9742-30974c4f9ea1" />

---

# 📌 Project Overview

MyWeather allows users to:

- Search for any city worldwide
- Retrieve real-time weather data
- View extended atmospheric metrics
- Handle invalid inputs gracefully
- Experience reliable API-backed responses with fallback handling

The system integrates with an external REST API and processes structured JSON responses before presenting them in a clean frontend interface.

---

##  Flask Layer (Flask App)

`app.py` acts as the controller layer.

Responsibilities:
- Accept HTTP requests
- Validate user input
- Call the service layer
- Return JSON responses
- Handle exceptions gracefully
- Log runtime issues

This layer does NOT directly interact with the external API.
Instead, it delegates that responsibility to a separate service module.

This separation improves:
- Maintainability
- Testability
- Code readability
- Scalability

---

##  Service Layer (weather_service.py)

This is the core logic layer.

Responsibilities:

- Communicate with OpenWeather REST API
- Construct API request URLs
- Parse JSON responses
- Extract relevant metrics
- Format structured response
- Handle API failures
- Implement caching logic
- Raise structured errors for invalid cities

By separating this logic from the Flask routes, the application follows a clean architecture principle commonly used in production systems.

---

## 🌐 REST API Integration

The application integrates with:

OpenWeather REST API

Workflow:

1. User enters city name
2. Flask route receives request
3. Service layer constructs API call
4. External API returns JSON response
5. Service layer extracts:
   - Temperature
   - Feels like
   - Humidity
   - Pressure
   - Wind speed
   - Visibility
   - Weather condition
   - Icon
   - Sunrise timestamp
   - Sunset timestamp
6. Data returned to frontend as structured JSON
7. Frontend renders formatted weather dashboard

This demonstrates proper REST API consumption and JSON parsing.

---

# ⚡ Caching (Performance Optimization)

To reduce repeated API calls:

- The service layer implements in-memory caching
- If the same city is requested within a short time window,
  the cached response is returned instead of calling the API again

Benefits:
- Reduced API usage
- Faster response time
- Improved efficiency
- Awareness of rate limiting concerns

This reflects performance optimization practices used in real-world backend systems.

---

# 🛡️ Error Handling Strategy

The application handles:

- Invalid city names
- API key issues
- Network failures
- Missing API response fields
- Unexpected server errors

Errors are:

- Logged for debugging
- Returned in structured JSON format
- Displayed clearly to users

This prevents application crashes and improves reliability.

---

# 🔐 Environment-Based Configuration

Sensitive data (API keys) are NOT hardcoded.

The application uses:

os.getenv("OPENWEATHER_API_KEY")

API keys are stored in environment variables.

Benefits:

- Prevents secret leakage
- Enables secure deployment
- Follows 12-factor app principles
- Production-ready configuration management

`.env` is excluded via `.gitignore`.

---

# 📊 Weather Data Displayed

The application shows:

- Temperature (°C)
- Feels Like
- Humidity (%)
- Atmospheric Pressure (hPa)
- Wind Speed (m/s)
- Visibility (km)
- Weather Condition
- Weather Icon
- Sunrise Time
- Sunset Time

Sunrise and sunset timestamps are converted from UNIX format to readable local time in the frontend.

---

# 🛠️ Tech Stack

Backend:
- Python
- Flask
- Requests
- Gunicorn

Frontend:
- HTML
- CSS

API:
- OpenWeather REST API

Deployment:
- Render (Cloud hosting)

---

# ⚙️ Local Setup Instructions

## 1️⃣ Clone Repository


git clone https://github.com/Tharun-vcode/MyWeather.git

cd MyWeather


## 2️⃣ Create Virtual Environment


python -m venv venv
source venv/bin/activate


(Windows: `venv\Scripts\activate`)

## 3️⃣ Install Dependencies


pip install -r requirements.txt


## 4️⃣ Set Environment Variable

Create a `.env` file:


OPENWEATHER_API_KEY=your_api_key_here


## 5️⃣ Run Application


python app.py


Visit:


http://127.0.0.1:5000/

---
