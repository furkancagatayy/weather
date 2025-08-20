import { useEffect, useState } from "react";
import "./App.css";
import { WeatherCard } from "./components/WeatherCard";
import { FeatureCard } from "./components/FeatureCard";
import { WeatherMatrix } from "./components/WeatherMatrix";
import { Button } from "./components/ui/button";
import { Card, CardContent } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { mockProjectStats, mockFeatures } from "./mock";
import { Cpu, Zap, Clock, Database, AlertCircle } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [weatherData, setWeatherData] = useState(null);
  const [stats, setStats] = useState(mockProjectStats);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const fetchWeatherData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API}/weather/sivas`);
      setWeatherData(response.data);
    } catch (err) {
      console.error('Weather API error:', err);
      setError('Hava durumu verileri alınamadı');
      // Fallback mock data
      setWeatherData({
        temperature: { value: 23.5, unit: "°C", trend: "stable", icon: "thermometer" },
        windSpeed: { value: 8.2, unit: "m/s", trend: "increasing", icon: "wind" },
        precipitation: { value: 2.3, unit: "mm", trend: "decreasing", icon: "cloud-rain" },
        pressure: { value: 1013.2, unit: "hPa", trend: "stable", icon: "gauge" },
        windDirection: { value: "NE", degrees: 45, unit: "°", trend: "stable", icon: "compass" },
        location: "Sivas, Türkiye",
        lastUpdate: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchWeatherData();
    
    // Her 5 dakikada bir güncelle
    const interval = setInterval(fetchWeatherData, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-yellow-500 rounded-lg flex items-center justify-center">
                <Cpu className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">LEGO Spike Hava İstasyonu</h1>
                <p className="text-sm text-gray-500">Gerçek Zamanlı Meteoroloji Projesi</p>
              </div>
            </div>
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
              <Zap className="h-3 w-3 mr-1" />
              Aktif
            </Badge>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-purple-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              LEGO Spike ile
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600"> Sivas Hava Durumu</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              LEGO Spike set kullanarak geliştirdiğimiz bu projede, Sivas'ın gerçek zamanlı hava durumu verileri 8x8 LED matriks ekranda görüntüleniyor. 
              Hissedilen sıcaklık, rüzgar hızı, yağış miktarı, hava basıncı ve rüzgar yönü sürekli izleniyor.
            </p>
            {error && (
              <div className="mt-4 flex items-center justify-center gap-2 text-orange-600 bg-orange-50 px-4 py-2 rounded-lg max-w-md mx-auto">
                <AlertCircle className="h-4 w-4" />
                <span className="text-sm">{error} - Mock veriler gösteriliyor</span>
              </div>
            )}
          </div>
          
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Sivas hava durumu veriler yükleniyor...</p>
                </div>
              ) : weatherData ? (
                <>
                  <div className="grid grid-cols-2 gap-4">
                    <WeatherCard data={weatherData.temperature} title="Hissedilen Sıcaklık" />
                    <WeatherCard data={weatherData.windSpeed} title="Rüzgar Hızı" />
                    <WeatherCard data={weatherData.precipitation} title="Yağış" />
                    <WeatherCard data={weatherData.pressure} title="Basınç" />
                  </div>
                  <WeatherCard data={weatherData.windDirection} title="Rüzgar Yönü" />
                  <div className="text-sm text-gray-500 text-center">
                    <Clock className="h-4 w-4 inline mr-1" />
                    Son güncelleme: {new Date(weatherData.lastUpdate).toLocaleTimeString('tr-TR')}
                    <br />
                    📍 {weatherData.location}
                  </div>
                </>
              ) : (
                <div className="text-center py-8 text-red-600">
                  <AlertCircle className="h-12 w-12 mx-auto mb-4" />
                  <p>Hava durumu verileri yüklenemedi</p>
                </div>
              )}
            </div>
            
            <div className="flex justify-center">
              <WeatherMatrix weatherData={weatherData} />
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <Card className="text-center border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-blue-600 mb-2">{stats.sensorsActive}</div>
                <div className="text-sm text-gray-600">Aktif Sensör</div>
              </CardContent>
            </Card>
            <Card className="text-center border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-green-600 mb-2">{stats.dataPoints.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Veri Noktası</div>
              </CardContent>
            </Card>
            <Card className="text-center border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-purple-600 mb-2">{stats.uptime}</div>
                <div className="text-sm text-gray-600">Çalışma Süresi</div>
              </CardContent>
            </Card>
            <Card className="text-center border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-center gap-1 mb-2">
                  <Clock className="h-4 w-4 text-orange-600" />
                  <span className="text-sm font-medium text-orange-600">{stats.lastUpdate}</span>
                </div>
                <div className="text-sm text-gray-600">Son Güncelleme</div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">Proje Özellikleri</h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              LEGO Spike teknolojisi ile meteoroloji dünyasını keşfedin
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {mockFeatures.map((feature, index) => (
              <FeatureCard key={index} feature={feature} />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-purple-700">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Robotik ve Meteoroloji Birleşiyor
          </h3>
          <p className="text-xl text-blue-100 mb-8 leading-relaxed">
            LEGO Spike ile geliştirdiğimiz bu hava istasyonu, Sivas'ın gerçek zamanlı hava durumu verilerini görüntüleyerek eğitim ve teknoloji arasında köprü kuruyor. 
            Gerçek veriler, görsel gösterim ve interaktif öğrenme deneyimi sunar.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 transition-all transform hover:scale-105">
              <Database className="h-5 w-5 mr-2" />
              Proje Detayları
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600 transition-all transform hover:scale-105">
              <Cpu className="h-5 w-5 mr-2" />
              Teknik Bilgiler
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-red-500 to-yellow-500 rounded-lg flex items-center justify-center">
                <Cpu className="h-5 w-5 text-white" />
              </div>
              <span className="text-lg font-semibold text-white">LEGO Spike Hava İstasyonu</span>
            </div>
            <p className="text-sm text-gray-400">
              © 2025 LEGO Spike Weather Station Project. Robotik meraklıları için geliştirildi.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;