from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # åº”ç”¨é…ç½®
    APP_NAME: str = "Trip Planner API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # æ•°æ®åº“é…ç½?
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/trip_planner"

    # Redisé…ç½®
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWTé…ç½®
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30å¤?

    # å¾?ä¿¡é…ç½?
    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""

    # é«˜å¾·åœ°å›¾é…ç½®
    AMAP_API_KEY: str = ""
    AMAP_BASE_URL: str = "https://restapi.amap.com/v3"

    # å¤©æ°”APIé…ç½®
    WEATHER_API_KEY: str = ""
    WEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    # ¼æÈİ Flask/²âÊÔ»·¾³±äÁ¿
    flask_env: Optional[str] = None
    jwt_secret_key: Optional[str] = None
    amap_key: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
