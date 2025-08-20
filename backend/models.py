from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class WeatherData(BaseModel):
    value: float
    unit: str
    trend: str
    icon: str

class WindDirectionData(BaseModel):
    value: str
    degrees: int
    unit: str
    trend: str
    icon: str

class WeatherResponse(BaseModel):
    temperature: WeatherData
    windSpeed: WeatherData
    precipitation: WeatherData
    pressure: WeatherData
    windDirection: WindDirectionData
    location: str
    lastUpdate: datetime

class WeatherReading(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    location: str
    temperature: float
    wind_speed: float
    precipitation: float
    pressure: float
    wind_direction: int
    wind_direction_text: str
    humidity: Optional[int] = None
    visibility: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = "openweathermap"

class WeatherReadingCreate(BaseModel):
    location: str
    temperature: float
    wind_speed: float
    precipitation: float
    pressure: float
    wind_direction: int
    wind_direction_text: str
    humidity: Optional[int] = None
    visibility: Optional[float] = None