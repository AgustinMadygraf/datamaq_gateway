"""
Path: uses_cases/get_dashboard_data.py
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
        # Validación de periodo
        if inp.periodo not in PERIODOS:
            raise ValueError(f"Periodo inválido: {inp.periodo}. Debe ser uno de {list(PERIODOS.keys())}")

        last = self._dash.get_last_point()
        unixtime = last.unixtime if last else 0
        vel_ult = last.hr_counter1 if last else 0

        # Validación de timestamp
        if inp.conta_ms is not None:
            if inp.conta_ms < 0:
                raise ValueError("El timestamp (conta_ms) no puede ser negativo.")
            if inp.conta_ms > unixtime * 1000:
                # Si el timestamp es mayor al último dato, lo ajustamos
                conta_ms = unixtime * 1000
            else:
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
            unixtime=unixtime,  # podés ajustar UTC-3 en el presenter si querés
            rawdata=raw,
            formato=formato,
        )
