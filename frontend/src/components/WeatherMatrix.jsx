import { useEffect, useState } from "react";

export const WeatherMatrix = ({ weatherData }) => {
  const [activePixels, setActivePixels] = useState([]);
  
  useEffect(() => {
    // Simulate matrix display animation
    const interval = setInterval(() => {
      const newPixels = Array.from({ length: 64 }, (_, i) => ({
        id: i,
        active: Math.random() > 0.7,
        color: getPixelColor(i, weatherData)
      }));
      setActivePixels(newPixels);
    }, 1000);
    
    return () => clearInterval(interval);
  }, [weatherData]);
  
  const getPixelColor = (index, data) => {
    const row = Math.floor(index / 8);
    if (row < 2) return "bg-blue-400"; // Temperature
    if (row < 4) return "bg-green-400"; // Wind
    if (row < 6) return "bg-yellow-400"; // Precipitation  
    return "bg-red-400"; // Pressure
  };
  
  return (
    <div className="bg-black p-6 rounded-xl shadow-2xl">
      <div className="grid grid-cols-8 gap-1">
        {Array.from({ length: 64 }, (_, i) => {
          const pixel = activePixels.find(p => p.id === i);
          return (
            <div
              key={i}
              className={`w-4 h-4 rounded-sm transition-all duration-300 ${
                pixel?.active 
                  ? `${pixel.color} shadow-lg animate-pulse` 
                  : "bg-gray-800"
              }`}
            />
          );
        })}
      </div>
      <div className="mt-4 text-center">
        <div className="text-green-400 text-xs font-mono">
          LEGO SPIKE MATRIX DISPLAY
        </div>
        <div className="text-gray-400 text-xs mt-1">
          8x8 LED Matrix Simulation
        </div>
      </div>
    </div>
  );
};