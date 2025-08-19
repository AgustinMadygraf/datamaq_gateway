"""
Path: application/container.py
"""

import os

from use_cases.get_dashboard_data import GetDashboardData
from entities.dashboard_point import DashboardPoint
from entities.formato import Formato
from interface_adapters.gateway.repositories import (
    InMemoryDashboardRepository,
    InMemoryFormatoRepository,
)


# Wire in-memory por defecto (arranca sin DB)
def _build_inmemory_uc() -> GetDashboardData:
    dash_repo = InMemoryDashboardRepository(seed=[
        DashboardPoint(unixtime=1723948800, hr_counter1=120),  # ejemplo
        DashboardPoint(unixtime=1723952400, hr_counter1=130),
    ])
    formato_repo = InMemoryFormatoRepository(
        ultimo=Formato(id_formato=123, formato="22x10x30", ancho_bobina_mm=760)
    )
    return GetDashboardData(dash_repo, formato_repo)

# Si querés pasar a MySQL, podés detectar una env var y construir repos reales
def resolve_get_dashboard_data() -> GetDashboardData:
    "Resolver para obtener datos del dashboard"
    if os.getenv("USE_DB") == "mysql":
        return _build_inmemory_uc()
    return _build_inmemory_uc()
