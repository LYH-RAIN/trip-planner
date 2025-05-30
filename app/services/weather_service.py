import httpx
from typing import Optional, Dict, Any
from datetime import date
from app.core.config import settings
from app.core.exceptions import ValidationError


class WeatherService:
    def __init__(self):
        self.base_url = settings.WEATHER_BASE_URL
        self.api_key = settings.WEATHER_API_KEY

    async def get_weather_forecast(self, city: str, target_date: date) -> Optional[Dict[str, Any]]:
        """获取天气预报"""
        if not self.api_key:
            return None

        try:
            # 获取城市坐标
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {
                "q": city,
                "limit": 1,
                "appid": self.api_key
            }

            async with httpx.AsyncClient() as client:
                geo_response = await client.get(geo_url, params=geo_params)
                geo_data = geo_response.json()

                if not geo_data:
                    return None

                lat = geo_data[0]["lat"]
                lon = geo_data[0]["lon"]

                # 获取天气预报
                weather_url = f"{self.base_url}/forecast"
                weather_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "zh_cn"
                }

                weather_response = await client.get(weather_url, params=weather_params)
                weather_data = weather_response.json()

                # 查找目标日期的天气
                target_timestamp = target_date.strftime("%Y-%m-%d")

                for item in weather_data.get("list", []):
                    item_date = item["dt_txt"][:10]
                    if item_date == target_timestamp:
                        weather = item["weather"][0]
                        main = item["main"]

                        return {
                            "condition": weather["description"],
                            "temperature": f"{int(main['temp_min'])}°-{int(main['temp_max'])}°",
                            "icon": weather["icon"],
                            "humidity": f"{main['humidity']}%",
                            "wind": f"{item['wind']['speed']}m/s",
                            "precipitation": f"{int(item.get('pop', 0) * 100)}%"
                        }

                return None

        except Exception as e:
            print(f"获取天气信息失败: {str(e)}")
            return None
