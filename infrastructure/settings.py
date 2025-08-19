"""
Path: infrastructure/settings.py
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    "Configuración de la base de datos MySQL"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "ESP32"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    USE_DB: str = "memory"

    class Config:
        "Configuración de Pydantic"
        env_file = ".env"

settings = Settings()
