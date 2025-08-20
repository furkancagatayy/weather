#!/usr/bin/env python3
"""
LEGO Spike Weather Station Backend Tests
Tests the weather API endpoints for Sivas, Turkey
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from typing import Dict, Any
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Test configuration
BACKEND_URL = "https://lego-weather-station.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class WeatherStationTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
        
    async def close(self):
        await self.client.aclose()
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
        print(f"{status} - {test_name}")
        if details:
            print(f"    Details: {details}")
        print()
    
    async def test_health_endpoint(self):
        """Test the health check endpoint"""
        try:
            response = await self.client.get(f"{API_BASE}/health")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["status", "timestamp", "services"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Health Endpoint", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check services status
                services = data.get("services", {})
                if "database" not in services or "weather_api" not in services:
                    self.log_test("Health Endpoint", False, "Missing service status information")
                    return False
                
                self.log_test("Health Endpoint", True, f"Status: {data['status']}, Services: {services}")
                return True
            else:
                self.log_test("Health Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Health Endpoint", False, f"Exception: {str(e)}")
            return False
    
    async def test_sivas_weather_endpoint(self):
        """Test the main Sivas weather endpoint"""
        try:
            response = await self.client.get(f"{API_BASE}/weather/sivas")
            
            if response.status_code != 200:
                self.log_test("Sivas Weather Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            
            # Check required top-level fields
            required_fields = ["temperature", "windSpeed", "precipitation", "pressure", "windDirection", "location", "lastUpdate"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test("Sivas Weather Endpoint", False, f"Missing top-level fields: {missing_fields}")
                return False
            
            # Check location is correct
            if data["location"] != "Sivas, Türkiye":
                self.log_test("Sivas Weather Endpoint", False, f"Incorrect location: {data['location']}, expected 'Sivas, Türkiye'")
                return False
            
            # Check weather parameter structure
            weather_params = ["temperature", "windSpeed", "precipitation", "pressure"]
            for param in weather_params:
                param_data = data[param]
                required_param_fields = ["value", "unit", "trend", "icon"]
                missing_param_fields = [field for field in required_param_fields if field not in param_data]
                
                if missing_param_fields:
                    self.log_test("Sivas Weather Endpoint", False, f"Missing fields in {param}: {missing_param_fields}")
                    return False
                
                # Check value is numeric
                if not isinstance(param_data["value"], (int, float)):
                    self.log_test("Sivas Weather Endpoint", False, f"{param} value is not numeric: {param_data['value']}")
                    return False
            
            # Check wind direction structure
            wind_dir = data["windDirection"]
            required_wind_fields = ["value", "degrees", "unit", "trend", "icon"]
            missing_wind_fields = [field for field in required_wind_fields if field not in wind_dir]
            
            if missing_wind_fields:
                self.log_test("Sivas Weather Endpoint", False, f"Missing fields in windDirection: {missing_wind_fields}")
                return False
            
            # Check wind direction degrees is valid
            if not isinstance(wind_dir["degrees"], int) or not (0 <= wind_dir["degrees"] <= 359):
                self.log_test("Sivas Weather Endpoint", False, f"Invalid wind direction degrees: {wind_dir['degrees']}")
                return False
            
            # Check data validity ranges
            temp_value = data["temperature"]["value"]
            if not (-50 <= temp_value <= 60):  # Reasonable temperature range
                self.log_test("Sivas Weather Endpoint", False, f"Temperature out of reasonable range: {temp_value}°C")
                return False
            
            wind_speed = data["windSpeed"]["value"]
            if not (0 <= wind_speed <= 50):  # Reasonable wind speed range
                self.log_test("Sivas Weather Endpoint", False, f"Wind speed out of reasonable range: {wind_speed} m/s")
                return False
            
            pressure = data["pressure"]["value"]
            if not (950 <= pressure <= 1050):  # Reasonable pressure range
                self.log_test("Sivas Weather Endpoint", False, f"Pressure out of reasonable range: {pressure} hPa")
                return False
            
            precipitation = data["precipitation"]["value"]
            if not (0 <= precipitation <= 100):  # Reasonable precipitation range
                self.log_test("Sivas Weather Endpoint", False, f"Precipitation out of reasonable range: {precipitation} mm")
                return False
            
            # Log successful test with sample data
            sample_data = {
                "temperature": f"{temp_value}°C",
                "windSpeed": f"{wind_speed} m/s",
                "precipitation": f"{precipitation} mm",
                "pressure": f"{pressure} hPa",
                "windDirection": f"{wind_dir['value']} ({wind_dir['degrees']}°)",
                "location": data["location"]
            }
            
            self.log_test("Sivas Weather Endpoint", True, f"All 5 weather parameters valid: {json.dumps(sample_data, indent=2)}")
            return True
            
        except Exception as e:
            self.log_test("Sivas Weather Endpoint", False, f"Exception: {str(e)}")
            return False
    
    async def test_weather_history_endpoint(self):
        """Test the weather history endpoint"""
        try:
            response = await self.client.get(f"{API_BASE}/weather/history")
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Weather History Endpoint", False, "Response is not a list")
                    return False
                
                # If there are records, check structure
                if len(data) > 0:
                    first_record = data[0]
                    required_fields = ["id", "location", "temperature", "wind_speed", "precipitation", "pressure", "wind_direction", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in first_record]
                    
                    if missing_fields:
                        self.log_test("Weather History Endpoint", False, f"Missing fields in history record: {missing_fields}")
                        return False
                    
                    self.log_test("Weather History Endpoint", True, f"Retrieved {len(data)} weather records with correct structure")
                else:
                    self.log_test("Weather History Endpoint", True, "Endpoint accessible, no historical records yet")
                
                return True
            else:
                self.log_test("Weather History Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Weather History Endpoint", False, f"Exception: {str(e)}")
            return False
    
    async def test_data_storage(self):
        """Test that weather data is being stored by making multiple requests"""
        try:
            # Get initial history count
            initial_response = await self.client.get(f"{API_BASE}/weather/history")
            if initial_response.status_code != 200:
                self.log_test("Data Storage Test", False, "Cannot access weather history for storage test")
                return False
            
            initial_count = len(initial_response.json())
            
            # Make a weather request to trigger storage
            weather_response = await self.client.get(f"{API_BASE}/weather/sivas")
            if weather_response.status_code != 200:
                self.log_test("Data Storage Test", False, "Weather endpoint failed during storage test")
                return False
            
            # Wait a moment for database write
            await asyncio.sleep(2)
            
            # Check if new record was added
            final_response = await self.client.get(f"{API_BASE}/weather/history")
            if final_response.status_code != 200:
                self.log_test("Data Storage Test", False, "Cannot access weather history after storage test")
                return False
            
            final_count = len(final_response.json())
            
            if final_count > initial_count:
                self.log_test("Data Storage Test", True, f"Weather data stored successfully (records: {initial_count} → {final_count})")
                return True
            else:
                # Check if the latest record matches our request
                history = final_response.json()
                if history and len(history) > 0:
                    latest_record = history[0]  # Should be sorted by timestamp desc
                    weather_data = weather_response.json()
                    
                    # Check if the stored data matches the API response
                    if (latest_record["location"] == "Sivas" and 
                        abs(latest_record["temperature"] - weather_data["temperature"]["value"]) < 0.1):
                        self.log_test("Data Storage Test", True, "Weather data storage verified (existing record matches)")
                        return True
                
                self.log_test("Data Storage Test", False, f"No new records added (count remained {final_count})")
                return False
                
        except Exception as e:
            self.log_test("Data Storage Test", False, f"Exception: {str(e)}")
            return False
    
    async def test_error_handling(self):
        """Test error handling for invalid endpoints"""
        try:
            # Test invalid weather location
            response = await self.client.get(f"{API_BASE}/weather/invalid-city")
            
            # Should return 404 for invalid endpoint
            if response.status_code == 404:
                self.log_test("Error Handling", True, "Correctly returns 404 for invalid weather location")
                return True
            else:
                self.log_test("Error Handling", False, f"Expected 404 for invalid location, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")
            return False
    
    async def test_turkish_localization(self):
        """Test Turkish localization in responses"""
        try:
            response = await self.client.get(f"{API_BASE}/weather/sivas")
            
            if response.status_code == 200:
                data = response.json()
                location = data.get("location", "")
                
                # Check for Turkish characters and proper location format
                if "Türkiye" in location and "Sivas" in location:
                    self.log_test("Turkish Localization", True, f"Correct Turkish location: {location}")
                    return True
                else:
                    self.log_test("Turkish Localization", False, f"Location not properly localized: {location}")
                    return False
            else:
                self.log_test("Turkish Localization", False, f"Cannot test localization, endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Turkish Localization", False, f"Exception: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all backend tests"""
        print("🧪 Starting LEGO Spike Weather Station Backend Tests")
        print(f"🌐 Testing against: {BACKEND_URL}")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health_endpoint),
            ("Sivas Weather API", self.test_sivas_weather_endpoint),
            ("Weather History", self.test_weather_history_endpoint),
            ("Data Storage", self.test_data_storage),
            ("Error Handling", self.test_error_handling),
            ("Turkish Localization", self.test_turkish_localization),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"🔍 Running: {test_name}")
            try:
                result = await test_func()
                if result:
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution failed: {str(e)}")
        
        print("=" * 60)
        print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Backend is working correctly.")
        else:
            print("⚠️  Some tests failed. Check details above.")
        
        return passed_tests, total_tests, self.test_results

async def main():
    """Main test execution"""
    tester = WeatherStationTester()
    try:
        passed, total, results = await tester.run_all_tests()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📋 DETAILED TEST SUMMARY")
        print("=" * 60)
        
        for result in results:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['test']}")
            if result["details"]:
                print(f"   {result['details']}")
        
        return passed == total
        
    finally:
        await tester.close()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)