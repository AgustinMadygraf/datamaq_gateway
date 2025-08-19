"""
Path: interface_adapters/controllers/get_dashboard_data.py
"""

from dataclasses import dataclass
from typing import List, Optional, Literal
from entities.dashboard_point import DashboardPoint
from entities.formato import Formato
from interface_adapters.gateway.repositories import DashboardRepository, FormatoRepository

Periodo = Literal["semana", "turno", "hora"]
PERIODOS = {"semana": 604800, "turno": 28800, "hora": 7200}  # segundos

@dataclass
class GetDashboardDataInput:
    "Entrada para obtener datos del dashboard"
    periodo: Periodo = "semana"
    conta_ms: Optional[int] = None  # timestamp (ms) de referencia (opcional)

@dataclass
class GetDashboardDataOutput:
    "Salida para obtener datos del dashboard"
    periodo: Periodo
    vel_ult: int
    unixtime: int
    rawdata: List[DashboardPoint]
    formato: Optional[Formato]

class GetDashboardData:
    "Caso de uso para obtener datos del dashboard"
    def __init__(self, dash_repo: DashboardRepository, formato_repo: FormatoRepository):
        self._dash = dash_repo
        self._formato = formato_repo

    def execute(self, inp: GetDashboardDataInput) -> GetDashboardDataOutput:
        "Ejecutar caso de uso para obtener datos del dashboard"
        last = self._dash.get_last_point()
        unixtime = last.unixtime if last else 0
        vel_ult = last.hr_counter1 if last else 0

        if inp.conta_ms and inp.conta_ms <= unixtime * 1000:
            conta_ms = inp.conta_ms
        else:
            conta_ms = unixtime * 1000

        ventana = PERIODOS[inp.periodo]
        t1 = int(conta_ms / 1000) - ventana
        t2 = int(conta_ms / 1000)

        raw = list(self._dash.get_points_between(t1, t2))
        formato = self._formato.get_ultimo_formato()

        return GetDashboardDataOutput(
            periodo=inp.periodo,
            vel_ult=vel_ult,
            unixtime=unixtime,
            rawdata=raw,
            formato=formato,
        )
