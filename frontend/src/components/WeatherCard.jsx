import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Thermometer, Wind, CloudRain, Gauge, Compass, TrendingUp, TrendingDown, Minus } from "lucide-react";

const iconMap = {
  thermometer: Thermometer,
  wind: Wind,
  "cloud-rain": CloudRain,
  gauge: Gauge,
  compass: Compass
};

const trendIconMap = {
  increasing: TrendingUp,
  decreasing: TrendingDown,
  stable: Minus
};

const trendColorMap = {
  increasing: "text-green-500",
  decreasing: "text-red-500",
  stable: "text-gray-500"
};

export const WeatherCard = ({ data, title }) => {
  const Icon = iconMap[data.icon];
  const TrendIcon = trendIconMap[data.trend];
  
  return (
    <Card className="group hover:shadow-lg transition-all duration-300 hover:-translate-y-1 bg-gradient-to-br from-white to-gray-50 border-2 hover:border-blue-200">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center justify-between text-sm font-medium text-gray-600">
          <span className="flex items-center gap-2">
            <Icon className="h-4 w-4 text-blue-600" />
            {title}
          </span>
          <TrendIcon className={`h-4 w-4 ${trendColorMap[data.trend]}`} />
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-gray-900">
            {data.value}
          </span>
          <span className="text-sm text-gray-500">{data.unit}</span>
        </div>
        {data.degrees && (
          <div className="mt-1 text-xs text-gray-400">
            {data.degrees}°
          </div>
        )}
        <Badge 
          variant="secondary" 
          className="mt-2 text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors"
        >
          {data.trend === "increasing" ? "Artıyor" : 
           data.trend === "decreasing" ? "Azalıyor" : "Sabit"}
        </Badge>
      </CardContent>
    </Card>
  );
};