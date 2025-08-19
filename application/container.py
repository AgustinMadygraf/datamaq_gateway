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
from infrastructure.pymsql import (
    MySQLDashboardRepository, MySQLFormatoRepository
)

def get_dashboard_gateways():
    "Retorna los gateways para dashboard y formato según configuración"
    if os.getenv("USE_DB") == "mysql" and MySQLDashboardRepository and MySQLFormatoRepository:
        dash_repo = MySQLDashboardRepository()
        formato_repo = MySQLFormatoRepository()
    else:
        dash_repo = InMemoryDashboardRepository(seed=[
            DashboardPoint(unixtime=1723948800, hr_counter1=120),  # ejemplo
            DashboardPoint(unixtime=1723952400, hr_counter1=130),
        ])
        formato_repo = InMemoryFormatoRepository(
            ultimo=Formato(id_formato=123, formato="22x10x30", ancho_bobina_mm=760)
        )
    return dash_repo, formato_repo
