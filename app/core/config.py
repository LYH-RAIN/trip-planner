from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "Trip Planner API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/trip_planner"

    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30天

    # 微信配置
    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""

    # 高德地图配置
    AMAP_API_KEY: str = ""
    AMAP_BASE_URL: str = "https://restapi.amap.com/v3"

    # 天气API配置
    WEATHER_API_KEY: str = ""
    WEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    class Config:
        env_file = ".env"

settings = Settings()
