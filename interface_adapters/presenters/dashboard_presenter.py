"""
Path: interfaces_adapters/presenters/dashcboard_presenters.py
"""

from typing import Optional, List
from pydantic import BaseModel

from use_cases.get_dashboard_data import GetDashboardDataOutput

class DashboardPointModel(BaseModel):
    "Modelo para un punto del dashboard"
    unixtime: int
    HR_COUNTER1: int
    HR_COUNTER2: Optional[int] = None

class FormatoModel(BaseModel):
    "Modelo para el formato del dashboard"
    id_formato: int
    formato: Optional[str] = None
    ancho_bobina_mm: Optional[int] = None

class DashboardResponse(BaseModel):
    "Modelo para la respuesta del dashboard"
    periodo: str
    vel_ult: int
    unixtime: int
    rawdata: List[DashboardPointModel]
    formato: Optional[FormatoModel] = None

def present(output: GetDashboardDataOutput) -> DashboardResponse:
    "Presentar los datos del dashboard"
    raw_models = [
        DashboardPointModel(
            unixtime=p.unixtime,
            HR_COUNTER1=p.hr_counter1,
            HR_COUNTER2=p.hr_counter2,
        ) for p in output.rawdata
    ]
    fmt = None
    if output.formato:
        fmt = FormatoModel(
            id_formato=output.formato.id_formato,
            formato=output.formato.formato,
            ancho_bobina_mm=output.formato.ancho_bobina_mm,
        )
    return DashboardResponse(
        periodo=output.periodo,
        vel_ult=output.vel_ult,
        unixtime=output.unixtime,
        rawdata=raw_models,
        formato=fmt,
    )
