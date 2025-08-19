"""
Path: application/container.py
"""

import os

from entities.dashboard_point import DashboardPoint
from entities.formato import Formato
from interface_adapters.gateway.repositories import (
    InMemoryDashboardRepository,
    InMemoryFormatoRepository,
)

from infrastructure.pymsql.pymysql_dashboard import MySQLDashboardRepository
from infrastructure.pymsql.pymysql_formato import MySQLFormatoRepository
from infrastructure.sql_alchemy.sql_alchemy_dashboard import SQLAlchemyDashboardRepository
from infrastructure.sql_alchemy.sql_alchemy_formato import SQLAlchemyFormatoRepository

def get_dashboard_gateways():
    "Retorna los gateways para dashboard y formato según configuración"
    use_db = os.getenv("USE_DB")
    if use_db == "mysql" and MySQLDashboardRepository and MySQLFormatoRepository:
        dash_repo = MySQLDashboardRepository()
        formato_repo = MySQLFormatoRepository()
    elif use_db == "sqlalchemy" and SQLAlchemyDashboardRepository and SQLAlchemyFormatoRepository:
        dash_repo = SQLAlchemyDashboardRepository()
        formato_repo = SQLAlchemyFormatoRepository()
    else:
        dash_repo = InMemoryDashboardRepository(seed=[
            DashboardPoint(unixtime=1723948800, hr_counter1=120),  # ejemplo
            DashboardPoint(unixtime=1723952400, hr_counter1=130),
        ])
        formato_repo = InMemoryFormatoRepository(
            ultimo=Formato(id_formato=123, formato="22x10x30", ancho_bobina_mm=760)
        )
    return dash_repo, formato_repo
