"""
Path: interface_adapters/gateways/repositories.py
"""

from typing import Protocol, Sequence, Optional, List

from entities.dashboard_point import DashboardPoint
from entities.formato import Formato

class DashboardRepository(Protocol):
    "Interfaz para el acceso a datos del dashboard."
    def get_last_point(self) -> Optional[DashboardPoint]:
        "Obtiene el último punto del dashboard."

    def get_points_between(self, t1: int, t2: int) -> Sequence[DashboardPoint]:
        "Método para obtener puntos entre dos timestamps."

class FormatoRepository(Protocol):
    "Clase para el acceso a datos de formato."
    def get_ultimo_formato(self) -> Optional[Formato]:
        "Método para obtener el último formato."

class InMemoryDashboardRepository(DashboardRepository):
    "Implementación en memoria de DashboardRepository"
    def __init__(self, seed: Optional[List[DashboardPoint]] = None):
        self._data = seed or []

    def get_last_point(self) -> Optional[DashboardPoint]:
        return self._data[-1] if self._data else None

    def get_points_between(self, t1: int, t2: int) -> Sequence[DashboardPoint]:
        return [p for p in self._data if t1 < p.unixtime <= t2]

class InMemoryFormatoRepository(FormatoRepository):
    "implementación en memoria de FormatoRepository"
    def __init__(self, ultimo: Optional[Formato] = None):
        self._ultimo = ultimo

    def get_ultimo_formato(self) -> Optional[Formato]:
        return self._ultimo
