"""
Path: interface_adapters/controllers/db_connection_controller.py
"""

import os
import pymysql
from interface_adapters.presenters.db_connection_presenter import present_db_connection

def test_db_connection():
    "Testea el valor de USE_DB y la conexión a la base de datos si corresponde"
    use_db = os.environ.get("USE_DB")
    result = {"USE_DB": use_db}
    if use_db == "mysql":
        try:
            conn = pymysql.connect(
                host=os.environ.get("MYSQL_HOST"),
                port=int(os.environ.get("MYSQL_PORT")),
                user=os.environ.get("MYSQL_USER"),
                password=os.environ.get("MYSQL_PASSWORD"),
                database=os.environ.get("MYSQL_DB"),
                connect_timeout=3
            )
            conn.close()
            result["connection"] = "success"
        except pymysql.MySQLError as e:
            result["connection"] = f"error: {str(e)}"
    else:
        result["connection"] = "not required (memory mode)"
    return present_db_connection(result)
