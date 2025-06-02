import httpx
from typing import Optional, Dict, Any
from datetime import date
from app.core.config import settings
from app.core.exceptions import ValidationError
from app.schemas.trip import WeatherInfo


class WeatherService:
    def __init__(self):
        self.base_url = settings.WEATHER_BASE_URL
        self.api_key = settings.WEATHER_API_KEY

    async def get_weather_forecast(self, city: str, target_date: date) -> Optional[WeatherInfo]:
        """Get weather forecast"""
        if not self.api_key:
            return None

        try:
            # Get city coordinates
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {
                "q": city,
                "limit": 1,
                "appid": self.api_key
            }

            async with httpx.AsyncClient() as client:
                geo_response = await client.get(geo_url, params=geo_params)
                geo_data = geo_response.json()

                if not geo_data or not isinstance(geo_data, list) or len(geo_data) == 0:
                    print(f"Could not find geo data for city: {city}")
                    return None
                
                # Add more robust error handling for geo_data structure
                if not isinstance(geo_data[0], dict) or "lat" not in geo_data[0] or "lon" not in geo_data[0]:
                    print(f"Geo data for city {city} is malformed: {geo_data[0]}")
                    return None

                lat = geo_data[0]["lat"]
                lon = geo_data[0]["lon"]

                # Get weather forecast
                weather_url = f"{self.base_url}/forecast"
                weather_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "zh_cn"
                }

                weather_response = await client.get(weather_url, params=weather_params)
                weather_response.raise_for_status()
                weather_data = weather_response.json()

                # Find weather for the target date
                # OpenWeatherMap 5 day / 3 hour forecast returns a list.
                # We need to find the forecast entry closest to midday for the target_date.
                target_dt_str = target_date.strftime("%Y-%m-%d")
                
                best_match_for_date = None

                for forecast_item in weather_data.get("list", []):
                    item_dt_txt = forecast_item.get("dt_txt", "")
                    if target_dt_str in item_dt_txt:
                        # Simple approach: take the first entry for the day, or one around midday
                        # A more complex approach might average or pick the most representative
                        if best_match_for_date is None or "12:00:00" in item_dt_txt :
                             best_match_for_date = forecast_item
                             if "12:00:00" in item_dt_txt: # Prefer midday forecast
                                 break 
                
                if best_match_for_date:
                    weather_details = best_match_for_date.get("weather", [{}])[0]
                    main_details = best_match_for_date.get("main", {})
                    wind_details = best_match_for_date.get("wind", {})
                    
                    # The WeatherInfo schema expects specific string formats.
                    # Note: OpenWeatherMap 'pop' is probability of precipitation.
                    precipitation_percentage = int(best_match_for_date.get("pop", 0) * 100)

                    return WeatherInfo(
                        condition=weather_details.get("description"),
                        temperature=f"{int(main_details.get('temp_min', 0))}°-{int(main_details.get('temp_max', 0))}°",
                        icon=weather_details.get("icon"),
                        humidity=f"{main_details.get('humidity', 0)}%",
                        wind=f"{wind_details.get('speed', 0)}m/s",
                        precipitation=f"{precipitation_percentage}%"
                        # uv_index, sunrise, sunset are not directly available in the 5-day forecast's list items.
                        # These would require a different API call (e.g., One Call API) or be omitted.
                    )
                else:
                    print(f"No forecast data found for {target_date} in city {city}")
                    return None

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred while fetching weather data: {e}")
            return None
        except httpx.RequestError as e:
            print(f"Request error occurred while fetching weather data: {e}")
            return None
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error parsing weather data: {str(e)}. Data: {weather_data if 'weather_data' in locals() else 'N/A'}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching weather information: {str(e)}")
            return None
