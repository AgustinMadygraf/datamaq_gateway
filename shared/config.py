"""
Path: shared/config.py
"""

import os
from dotenv import load_dotenv
load_dotenv()

def get_env(var_name, default=None):
    "Obtiene una variable de entorno"
    return os.environ.get(var_name, default)

def get_mysql_config():
    "Obtiene la configuración de MySQL"
    return {
        "host": get_env("MYSQL_HOST"),
        "port": int(get_env("MYSQL_PORT", 3306)),
        "user": get_env("MYSQL_USER"),
        "password": get_env("MYSQL_PASSWORD"),
        "database": get_env("MYSQL_DB"),
        "connect_timeout": 3
    }

def get_use_db():
    "Obtiene el valor de USE_DB"
    return get_env("USE_DB")

def get_static_path():
    "Obtiene la ruta base de archivos estáticos"
    return get_env("STATIC_PATH", "static")
