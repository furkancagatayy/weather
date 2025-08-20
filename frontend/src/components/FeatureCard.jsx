import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Activity, Zap, Monitor, GraduationCap } from "lucide-react";

const iconMap = {
  activity: Activity,
  sensors: Zap,
  monitor: Monitor,
  "graduation-cap": GraduationCap
};

export const FeatureCard = ({ feature }) => {
  const Icon = iconMap[feature.icon];
  
  return (
    <Card className="group hover:shadow-xl transition-all duration-500 hover:-translate-y-2 bg-white border-0 shadow-md hover:shadow-2xl">
      <CardHeader className="text-center pb-4">
        <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
          <Icon className="h-8 w-8 text-white" />
        </div>
        <CardTitle className="text-lg font-semibold text-gray-800 group-hover:text-blue-600 transition-colors">
          {feature.title}
        </CardTitle>
      </CardHeader>
      <CardContent className="text-center">
        <p className="text-gray-600 leading-relaxed">
          {feature.description}
        </p>
      </CardContent>
    </Card>
  );
};