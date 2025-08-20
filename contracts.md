# LEGO Spike Hava İstasyonu - API Contracts

## Backend API Endpoints

### 1. GET /api/weather/sivas
**Açıklama:** Sivas için gerçek zamanlı hava durumu verilerini OpenWeatherMap API'sinden çeker

**Response:**
```json
{
  "temperature": {
    "value": 23.5,
    "unit": "°C",
    "trend": "stable",
    "icon": "thermometer"
  },
  "windSpeed": {
    "value": 8.2,
    "unit": "m/s", 
    "trend": "increasing",
    "icon": "wind"
  },
  "precipitation": {
    "value": 2.3,
    "unit": "mm",
    "trend": "decreasing", 
    "icon": "cloud-rain"
  },
  "pressure": {
    "value": 1013.2,
    "unit": "hPa",
    "trend": "stable",
    "icon": "gauge"
  },
  "windDirection": {
    "value": "NE",
    "degrees": 45,
    "unit": "°",
    "trend": "stable",
    "icon": "compass"
  },
  "location": "Sivas, Turkey",
  "lastUpdate": "2025-01-20T15:30:00Z"
}
```

### 2. GET /api/weather/history
**Açıklama:** Son 24 saatlik hava durumu geçmişi (isteğe bağlı)

## Database Models

### WeatherReading
```python
{
  "id": "uuid",
  "location": "Sivas",
  "temperature": 23.5,
  "wind_speed": 8.2,
  "precipitation": 2.3,
  "pressure": 1013.2,
  "wind_direction": 45,
  "wind_direction_text": "NE",
  "timestamp": "datetime",
  "source": "openweathermap"
}
```

## Mock Data Replacement

### Frontend Changes Needed:
1. **App.js:** `mockWeatherData` yerine API'den veri çekme
2. **API integration:** `REACT_APP_BACKEND_URL/api/weather/sivas` endpoint'i kullan
3. **Error handling:** API çağrısı başarısız olursa mock data'ya geri dön
4. **Loading states:** API çağrısı sırasında loading göster

### API Integration Details:
- **OpenWeatherMap API:** Current Weather Data API kullan
- **Sivas Koordinatları:** lat=39.7477, lon=37.0179
- **Units:** metric (Celsius, m/s, hPa)
- **Update Frequency:** 10 dakikada bir cache güncelle
- **Error Handling:** API hatası durumunda mock data göster

## Implementation Plan:
1. Backend .env dosyasına OPENWEATHER_API_KEY ekle
2. httpx dependency ekle
3. Weather service oluştur
4. API endpoint implement et
5. Frontend'te mock.js'i kaldır ve API entegrasyonu yap
6. Error handling ve loading states ekle