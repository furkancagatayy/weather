from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime
from models import WeatherReading, WeatherReadingCreate, WeatherResponse
from weather_service import WeatherService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="LEGO Spike Weather Station API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Weather service instance
weather_service = WeatherService()

# Weather endpoints
@api_router.get("/weather/sivas", response_model=WeatherResponse)
async def get_sivas_weather():
    """Sivas için gerçek zamanlı hava durumu verilerini döndürür"""
    try:
        weather_data = await weather_service.get_sivas_weather()
        
        # Veritabanına kaydet
        weather_reading = WeatherReadingCreate(
            location="Sivas",
            temperature=weather_data.temperature.value,
            wind_speed=weather_data.windSpeed.value,
            precipitation=weather_data.precipitation.value,
            pressure=weather_data.pressure.value,
            wind_direction=weather_data.windDirection.degrees,
            wind_direction_text=weather_data.windDirection.value
        )
        
        reading_dict = weather_reading.dict()
        weather_obj = WeatherReading(**reading_dict)
        await db.weather_readings.insert_one(weather_obj.dict())
        
        return weather_data
        
    except Exception as e:
        logger.error(f"Weather endpoint error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Weather service error: {str(e)}")

@api_router.get("/weather/history", response_model=List[WeatherReading])
async def get_weather_history(limit: int = 24):
    """Son hava durumu kayıtlarını döndürür"""
    try:
        readings = await db.weather_readings.find().sort("timestamp", -1).limit(limit).to_list(limit)
        return [WeatherReading(**reading) for reading in readings]
    except Exception as e:
        logger.error(f"Weather history error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

# Basic endpoints
@api_router.get("/")
async def root():
    return {"message": "LEGO Spike Weather Station API", "status": "active"}

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "connected",
            "weather_api": "available"
        }
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("LEGO Spike Weather Station API starting up...")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("Database connection closed")