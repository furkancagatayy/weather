import httpx
import os
from datetime import datetime
from typing import Dict, Any
import logging
from models import WeatherResponse, WeatherData, WindDirectionData

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Sivas koordinatları
        self.sivas_coords = {
            "lat": 39.7477,
            "lon": 37.0179
        }
    
    def _get_wind_direction_text(self, degrees: int) -> str:
        """Rüzgar yönünü derece cinsinden metne çevirir"""
        directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        ]
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def _determine_trend(self, current_value: float, parameter: str) -> str:
        """Basit trend belirleme (gerçek uygulamada geçmiş verilerle karşılaştırılır)"""
        # Şimdilik mock trend döndürüyoruz
        import random
        trends = ["increasing", "decreasing", "stable"]
        return random.choice(trends)
    
    async def get_sivas_weather(self) -> WeatherResponse:
        """Sivas için hava durumu verilerini OpenWeatherMap'ten çeker"""
        async with httpx.AsyncClient() as client:
            try:
                # Current weather data
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "lat": self.sivas_coords["lat"],
                        "lon": self.sivas_coords["lon"],
                        "appid": self.api_key,
                        "units": "metric",
                        "lang": "tr"
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Veriyi parse et
                temp = data["main"]["temp"]
                pressure = data["main"]["pressure"]
                humidity = data["main"]["humidity"]
                wind_speed = data.get("wind", {}).get("speed", 0)
                wind_deg = data.get("wind", {}).get("deg", 0)
                
                # Yağış verisi (son 1 saat)
                precipitation = 0
                if "rain" in data:
                    precipitation = data["rain"].get("1h", 0)
                elif "snow" in data:
                    precipitation = data["snow"].get("1h", 0)
                
                # Wind direction text
                wind_dir_text = self._get_wind_direction_text(wind_deg)
                
                # Response oluştur
                weather_response = WeatherResponse(
                    temperature=WeatherData(
                        value=round(temp, 1),
                        unit="°C",
                        trend=self._determine_trend(temp, "temperature"),
                        icon="thermometer"
                    ),
                    windSpeed=WeatherData(
                        value=round(wind_speed, 1),
                        unit="m/s",
                        trend=self._determine_trend(wind_speed, "wind"),
                        icon="wind"
                    ),
                    precipitation=WeatherData(
                        value=round(precipitation, 1),
                        unit="mm",
                        trend=self._determine_trend(precipitation, "rain"),
                        icon="cloud-rain"
                    ),
                    pressure=WeatherData(
                        value=round(pressure, 1),
                        unit="hPa",
                        trend=self._determine_trend(pressure, "pressure"),
                        icon="gauge"
                    ),
                    windDirection=WindDirectionData(
                        value=wind_dir_text,
                        degrees=wind_deg,
                        unit="°",
                        trend="stable",
                        icon="compass"
                    ),
                    location="Sivas, Türkiye",
                    lastUpdate=datetime.utcnow()
                )
                
                logger.info(f"Weather data retrieved for Sivas: {temp}°C, {wind_speed}m/s")
                return weather_response
                
            except httpx.TimeoutException:
                logger.error("OpenWeatherMap API timeout")
                raise Exception("Weather service timeout")
            except httpx.HTTPStatusError as e:
                logger.error(f"OpenWeatherMap API error: {e.response.status_code}")
                raise Exception(f"Weather API error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Weather service error: {str(e)}")
                raise Exception("Weather service unavailable")
    
    async def get_weather_with_forecast(self) -> Dict[str, Any]:
        """Mevcut hava durumu + 5 günlük tahmin (isteğe bağlı)"""
        # Gelecek sürümlerde implement edilebilir
        pass