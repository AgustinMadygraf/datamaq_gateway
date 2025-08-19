"""
Path: interface_adapters/controllers/db_connection_controller.py
"""

import pymysql
from interface_adapters.presenters.db_connection_presenter import present_db_connection
from shared.config import get_use_db, get_mysql_config

def test_db_connection():
    "Testea el valor de USE_DB y la conexión a la base de datos si corresponde"
    use_db = get_use_db()
    result = {"USE_DB": use_db}
    if use_db == "mysql":
        try:
            conn = pymysql.connect(**get_mysql_config())
            conn.close()
            result["connection"] = "success"
        except pymysql.MySQLError as e:
            result["connection"] = f"error: {str(e)}"
    else:
        result["connection"] = "not required (memory mode)"
    return present_db_connection(result)
