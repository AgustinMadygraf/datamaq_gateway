"""
Path: infrastructure/pymsql/
"""

import os
from typing import Optional
import pymysql

from entities.formato import Formato
from interface_adapters.gateway.repositories import FormatoRepository


class MySQLFormatoRepository(FormatoRepository):
    "Repositorio MySQL para Formatos"
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            db=os.getenv("MYSQL_DB", "datamaq"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        def _get_ultimo_formato(self) -> Optional[Formato]:
            "Obtiene el último formato"
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id_formato, formato, ancho_bobina_mm "
                    "FROM tabla_1 "
                    "ORDER BY id_formato DESC "
                    "LIMIT 1"
                )
                row = cursor.fetchone()
                if row:
                    return Formato(**row)
                return None
