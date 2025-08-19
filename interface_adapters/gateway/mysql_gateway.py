"""
Path: interface_adapters/gateway/mysql_gateway.py
"""

import os
from typing import Optional, Sequence
import pymysql
from entities.dashboard_point import DashboardPoint
from entities.formato import Formato
from interface_adapters.gateway.repositories import DashboardRepository, FormatoRepository

class MySQLDashboardRepository(DashboardRepository):
    "Repositorio MySQL para Dashboard"
    def __init__(self):
        self.conn = pymysql.connect(
			host=os.getenv("MYSQL_HOST", "localhost"),
			user=os.getenv("MYSQL_USER", "root"),
			password=os.getenv("MYSQL_PASSWORD", ""),
			db=os.getenv("MYSQL_DB", "datamaq"),
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor
		)

    def get_last_point(self) -> Optional[DashboardPoint]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT unixtime, hr_counter1, hr_counter2 "
                "FROM intervalproduction "
                "ORDER BY unixtime DESC "
                "LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                return DashboardPoint(**row)
            return None

    def get_points_between(self, t1: int, t2: int) -> Sequence[DashboardPoint]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT unixtime, hr_counter1, hr_counter2 "
                "FROM intervalproduction "
                "WHERE unixtime > %s "
                "AND unixtime <= %s "
                "ORDER BY unixtime ASC",
                (t1, t2)
            )
            rows = cursor.fetchall()
            return [DashboardPoint(**row) for row in rows]

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

        def get_ultimo_formato(self) -> Optional[Formato]:
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
