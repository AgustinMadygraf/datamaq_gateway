"""
Path: infrastructure/pymsql/my_sql_formato_repository.py
"""

from typing import Optional
import pymysql

from entities.formato import Formato
from interface_adapters.gateway.repositories import FormatoRepository
from shared.config import get_mysql_config

class MySQLFormatoRepository(FormatoRepository):
    "Repositorio MySQL para Formatos"
    def __init__(self):
        mysql_cfg = get_mysql_config()
        self.conn = pymysql.connect(
            host=mysql_cfg["host"],
            user=mysql_cfg["user"],
            password=mysql_cfg["password"],
            db=mysql_cfg["database"],
            port=mysql_cfg.get("port", 3306),
            connect_timeout=mysql_cfg.get("connect_timeout", 3),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_ultimo_formato(self) -> Optional[Formato]:
        "Obtiene el último formato"
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT ID_formato as id_formato, formato, ancho as ancho_bobina_mm "
                "FROM tabla_1 "
                "ORDER BY ID_formato DESC "
                "LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                return Formato(**row)
            return None
