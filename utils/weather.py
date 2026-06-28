import requests

CITY_COORDINATES = {

    "Hyderabad": (17.3850, 78.4867),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Visakhapatnam": (17.6868, 83.2185),
    "Vijayawada": (16.5062, 80.6480),
    "Guntur": (16.3067, 80.4365),
    "Warangal": (17.9689, 79.5941),
    "Tirupati": (13.6288, 79.4192)

}


def get_weather(latitude, longitude):

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,"
        f"wind_speed_10m,weather_code"
    )

    response = requests.get(url)

    if response.status_code != 200:

        return None

    data = response.json()["current"]

    return {
        "temperature": data["temperature_2m"],
        "humidity": data["relative_humidity_2m"],
        "wind": data["wind_speed_10m"],
        "weather_code": data["weather_code"]
    }


def weather_advice(humidity, disease):

    advice = []

    if humidity >= 80:

        advice.append(
            "⚠ High humidity increases the risk of fungal diseases."
        )

    elif humidity >= 60:

        advice.append(
            "🌿 Moderate humidity. Continue monitoring your crop."
        )

    else:

        advice.append(
            "☀ Low humidity. Fungal disease risk is lower."
        )

    disease = disease.lower()

    if "blight" in disease:

        advice.append(
            "🍅 Blight spreads rapidly in cool and humid weather."
        )

    elif "rust" in disease:

        advice.append(
            "🌽 Rust thrives in humid conditions. Inspect nearby leaves."
        )

    elif "healthy" in disease:

        advice.append(
            "✅ Continue regular watering and periodic inspection."
        )

    return advice