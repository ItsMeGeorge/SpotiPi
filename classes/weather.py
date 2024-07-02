import requests
import time
from datetime import datetime

def get_location():
    """Fetch the current location using IP-based geolocation."""
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        latitude, longitude = map(float, data['loc'].split(','))
        return latitude, longitude
    except requests.RequestException as e:
        return {"error": str(e)}

def get_weather_data(url, params, retries=5, backoff_factor=0.2):
    """Fetch weather data from the API with retries."""
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
            else:
                return {"error": str(e)}

def main():
    location = get_location()
    if "error" in location:
        print(location["error"])
        return

    latitude, longitude = location

    # Format the date as "YYYY-MM-DD"
    formatted_date = datetime.now().date().strftime("%Y-%m-%d")

    # Set up the Open-Meteo API parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "start_date": formatted_date,
        "end_date": formatted_date
    }

    # Fetch the weather data
    data = get_weather_data(url, params)

    if "error" in data:
        print(data["error"])
        return

    # Process the response
    hourly = data.get("hourly", {})

    print(f"Coordinates {latitude}°N {longitude}°E")

    # Process hourly data
    time_values = hourly.get("time", [])
    temperature_2m_values = hourly.get("temperature_2m", [])

    if time_values and temperature_2m_values:
        return f"{temperature_2m_values[0]}°C"

if __name__ == "__main__":
    main()
