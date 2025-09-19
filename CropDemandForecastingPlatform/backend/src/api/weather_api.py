import requests
from typing import Dict, Any

class WeatherAPI:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.example.com/weather"  # Replace with actual weather API

    def get_weather_forecast(self, region: str, days: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast for a specific region
        """
        # Simulated weather data for demo purposes
        import random
        
        forecast = []
        for _ in range(days):
            forecast.append({
                "temperature": random.uniform(15, 35),
                "rainfall": random.uniform(0, 100),
                "humidity": random.uniform(30, 90),
                "soil_moisture": random.uniform(20, 60)
            })
        
        return {
            "region": region,
            "forecast": forecast
        }

    def get_historical_weather(self, region: str, days_back: int = 30) -> Dict[str, Any]:
        """
        Get historical weather data for a specific region
        """
        # Simulated historical data for demo purposes
        import random
        
        history = []
        for _ in range(days_back):
            history.append({
                "temperature": random.uniform(15, 35),
                "rainfall": random.uniform(0, 100),
                "humidity": random.uniform(30, 90),
                "soil_moisture": random.uniform(20, 60)
            })
        
        return {
            "region": region,
            "history": history
        }