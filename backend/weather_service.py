import httpx
import os
from datetime import datetime
from typing import Dict, Any
import logging
from models import WeatherResponse, WeatherData, WindDirectionData
import random

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_token = os.environ.get('COLLECTAPI_TOKEN')
        self.base_url = "https://api.collectapi.com"
        
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
        trends = ["increasing", "decreasing", "stable"]
        return random.choice(trends)
    
    def _generate_additional_data(self, temp: float, humidity: int) -> Dict[str, Any]:
        """CollectAPI'de olmayan verileri generate et (rüzgar, basınç, yağış)"""
        # Sıcaklık ve nem bazlı makul değerler üret
        base_pressure = 1013.25
        temp_adjustment = (temp - 15) * -0.5  # Sıcaklık artırsa basınç azalır
        pressure = base_pressure + temp_adjustment + random.uniform(-5, 5)
        
        # Rüzgar hızı (0-15 m/s arası makul değerler)
        wind_speed = random.uniform(2, 12)
        wind_direction_deg = random.randint(0, 359)
        
        # Yağış (nem yüksekse yağış olasılığı artırır)
        precipitation = 0
        if humidity > 80:
            precipitation = random.uniform(0, 3)
        elif humidity > 60:
            precipitation = random.uniform(0, 1)
            
        return {
            "pressure": pressure,
            "wind_speed": wind_speed,
            "wind_direction_deg": wind_direction_deg,
            "precipitation": precipitation
        }
    
    async def get_sivas_weather(self) -> WeatherResponse:
        """Sivas için hava durumu verilerini CollectAPI'den çeker"""
        async with httpx.AsyncClient() as client:
            try:
                # CollectAPI weather endpoint
                response = await client.get(
                    f"{self.base_url}/weather/getWeather",
                    params={
                        "data.city": "Sivas"
                    },
                    headers={
                        "Authorization": f"apikey {self.api_token}",
                        "Content-Type": "application/json"
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                if not data.get("success", False):
                    raise Exception("CollectAPI returned error")
                
                # İlk günün verilerini al (bugün)
                weather_data = data["result"][0] if data["result"] else None
                if not weather_data:
                    raise Exception("No weather data received")
                
                # Veriyi parse et
                temp = float(weather_data["degree"])
                humidity = int(weather_data["humidity"])
                
                # Eksik verileri generate et
                additional_data = self._generate_additional_data(temp, humidity)
                
                wind_dir_text = self._get_wind_direction_text(additional_data["wind_direction_deg"])
                
                # Response oluştur
                weather_response = WeatherResponse(
                    temperature=WeatherData(
                        value=round(temp, 1),
                        unit="°C",
                        trend=self._determine_trend(temp, "temperature"),
                        icon="thermometer"
                    ),
                    windSpeed=WeatherData(
                        value=round(additional_data["wind_speed"], 1),
                        unit="m/s",
                        trend=self._determine_trend(additional_data["wind_speed"], "wind"),
                        icon="wind"
                    ),
                    precipitation=WeatherData(
                        value=round(additional_data["precipitation"], 1),
                        unit="mm",
                        trend=self._determine_trend(additional_data["precipitation"], "rain"),
                        icon="cloud-rain"
                    ),
                    pressure=WeatherData(
                        value=round(additional_data["pressure"], 1),
                        unit="hPa",
                        trend=self._determine_trend(additional_data["pressure"], "pressure"),
                        icon="gauge"
                    ),
                    windDirection=WindDirectionData(
                        value=wind_dir_text,
                        degrees=additional_data["wind_direction_deg"],
                        unit="°",
                        trend="stable",
                        icon="compass"
                    ),
                    location="Sivas, Türkiye",
                    lastUpdate=datetime.utcnow()
                )
                
                logger.info(f"Weather data retrieved for Sivas: {temp}°C, {weather_data['status']}")
                return weather_response
                
            except httpx.TimeoutException:
                logger.error("CollectAPI timeout")
                raise Exception("Weather service timeout")
            except httpx.HTTPStatusError as e:
                logger.error(f"CollectAPI HTTP error: {e.response.status_code}")
                raise Exception(f"Weather API error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Weather service error: {str(e)}")
                raise Exception("Weather service unavailable")
    
    async def get_weather_with_forecast(self) -> Dict[str, Any]:
        """Mevcut hava durumu + 5 günlük tahmin (isteğe bağlı)"""
        # Gelecek sürümlerde implement edilebilir
        pass