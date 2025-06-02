from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 搴旂敤閰嶇疆
    APP_NAME: str = "Trip Planner API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 鏁版嵁搴撻厤缃?
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/trip_planner"

    # Redis閰嶇疆
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT閰嶇疆
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30澶?

    # 寰?淇￠厤缃?
    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""

    # 楂樺痉鍦板浘閰嶇疆
    AMAP_API_KEY: str = ""
    AMAP_BASE_URL: str = "https://restapi.amap.com/v3"

    # 澶╂皵API閰嶇疆
    WEATHER_API_KEY: str = ""
    WEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    # 兼容 Flask/测试环境变量
    flask_env: Optional[str] = None
    jwt_secret_key: Optional[str] = None
    amap_key: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

print("DEBUG value:", settings.DEBUG, type(settings.DEBUG))
