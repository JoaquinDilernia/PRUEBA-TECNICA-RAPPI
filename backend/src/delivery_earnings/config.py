import os

from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
WEATHER_API_BASE_URL = "https://api.weatherapi.com/v1"
