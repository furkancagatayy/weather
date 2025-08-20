// Mock data for LEGO Spike Weather Station Demo
export const mockWeatherData = {
  temperature: {
    value: 23.5,
    unit: "°C",
    trend: "stable",
    icon: "thermometer"
  },
  windSpeed: {
    value: 8.2,
    unit: "m/s",
    trend: "increasing",
    icon: "wind"
  },
  precipitation: {
    value: 2.3,
    unit: "mm",
    trend: "decreasing",
    icon: "cloud-rain"
  },
  pressure: {
    value: 1013.2,
    unit: "hPa",
    trend: "stable",
    icon: "gauge"
  },
  windDirection: {
    value: "NE",
    degrees: 45,
    unit: "°",
    trend: "stable",
    icon: "compass"
  }
};

export const mockProjectStats = {
  sensorsActive: 5,
  dataPoints: 1247,
  uptime: "99.8%",
  lastUpdate: "2 saniye önce"
};

export const mockFeatures = [
  {
    title: "Gerçek Zamanlı Veri",
    description: "LEGO Spike ile anlık hava durumu verilerini matriks ekranında görüntüleyin",
    icon: "activity"
  },
  {
    title: "5 Farklı Sensör",
    description: "Sıcaklık, rüzgar hızı, yağış, basınç ve rüzgar yönü ölçümü",
    icon: "sensors"
  },
  {
    title: "Görsel Gösterim",
    description: "LED matriks ekran üzerinde renkli ve anlaşılır veri görselleştirme",
    icon: "monitor"
  },
  {
    title: "Eğitici Proje",
    description: "Robotik ve meteoroloji alanlarında öğrenme fırsatı",
    icon: "graduation-cap"
  }
];