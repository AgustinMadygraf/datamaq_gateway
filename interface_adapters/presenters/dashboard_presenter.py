"""
Path: interfaces_adapters/presenters/dashcboard_presenters.py
"""

from typing import Optional, List, Any, Dict
from pydantic import BaseModel

from use_cases.get_dashboard_data import GetDashboardDataOutput

class DashboardPointModel(BaseModel):
    "Modelo para un punto del dashboard"
    unixtime: int
    hr_counter1: int
    hr_counter2: Optional[int] = None

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

class DashboardPointLegacyModel(BaseModel):
    "Modelo para un punto del dashboard en formato legacy"
    unixtime: int
    HR_COUNTER1: str
    HR_COUNTER2: str

class FormatoLegacyModel(BaseModel):
    "Modelo para el formato del dashboard en formato legacy"
    formato: Optional[str] = None
    ancho_bobina: Optional[str] = None

def present(output: GetDashboardDataOutput) -> DashboardResponse:
    "Presentar los datos del dashboard en formato legacy"
    ls_periodos = {"semana": 604800, "turno": 28800, "hora": 7200}
    menos_periodo = {"semana": "turno", "turno": "hora", "hora": "hora"}
    gradient = [350, 340, 330, 320]
    ui_data = {
        "class": [1, 0, 0],
        "refClass": ["presado", "presione", "presione"],
        "preConta": 1708010400000,
        "postConta": 1709220000000,
        "estiloFondo": (
            "background: linear-gradient(195deg, "
            "rgba(107,170,34,0.9) 320%, "
            "rgba(255,164,1,0.9) 330%, "
            "rgba(234,53,34,0.9) 340%, "
            "rgba(100,10,5,0.9) 350%);"
        )
    }

    raw_models = [
        DashboardPointLegacyModel(
            unixtime=p.unixtime,
            HR_COUNTER1=str(p.hr_counter1 if p.hr_counter1 is not None else 0),
            HR_COUNTER2=str(p.hr_counter2 if p.hr_counter2 is not None else 0),
        ) for p in output.rawdata
    ]

    formato = None
    if output.formato:
        formato = FormatoLegacyModel(
            formato=output.formato.formato,
            ancho_bobina=(
                f"{output.formato.ancho_bobina_mm:.2f} mm"
                if output.formato.ancho_bobina_mm
                else None
            ),
        )

    data = {
        "periodo": output.periodo,
        "ls_periodos": ls_periodos,
        "menos_periodo": menos_periodo,
        "rawdata": [m.dict() for m in raw_models],
        "conta": output.unixtime * 1000,  # ejemplo, ajusta según tu lógica
        "vel_ult_calculada": str(output.vel_ult),
        "unixtime": output.unixtime,
        "gradient": gradient,
        "formatoData": formato.dict() if formato else None,
        "uiData": ui_data,
    }

    return {
        "status": "success",
        "data": data
    }

def present_legacy(output: GetDashboardDataOutput) -> Dict[str, Any]:
    "Presentar los datos del dashboard en formato legacy"
    # Ejemplo de campos adicionales, puedes ajustar según tu lógica
    ls_periodos = {"semana": 604800, "turno": 28800, "hora": 7200}
    menos_periodo = {"semana": "turno", "turno": "hora", "hora": "hora"}
    gradient = [350, 340, 330, 320]
    ui_data = {
        "class": [1, 0, 0],
        "refClass": ["presado", "presione", "presione"],
        "preConta": 1708010400000,
        "postConta": 1709220000000,
        "estiloFondo": (
            "background: linear-gradient(195deg, "
            "rgba(107,170,34,0.9) 320%, "
            "rgba(255,164,1,0.9) 330%, "
            "rgba(234,53,34,0.9) 340%, "
            "rgba(100,10,5,0.9) 350%);"
        )
    }

    raw_models = [
        DashboardPointLegacyModel(
            unixtime=p.unixtime,
            HR_COUNTER1=str(p.hr_counter1 if p.hr_counter1 is not None else 0),
            HR_COUNTER2=str(p.hr_counter2 if p.hr_counter2 is not None else 0),
        ) for p in output.rawdata
    ]

    formato = None
    if output.formato:
        formato = FormatoLegacyModel(
            formato=output.formato.formato,
            ancho_bobina=(
            f"{output.formato.ancho_bobina_mm:.2f} mm"
            if output.formato.ancho_bobina_mm is not None
            else None
            ),
        )

    data = {
        "periodo": output.periodo,
        "ls_periodos": ls_periodos,
        "menos_periodo": menos_periodo,
        "rawdata": [m.dict() for m in raw_models],
        "conta": output.unixtime * 1000,  # ejemplo, ajusta según tu lógica
        "vel_ult_calculada": str(output.vel_ult),
        "unixtime": output.unixtime,
        "gradient": gradient,
        "formatoData": formato.dict() if formato else None,
        "uiData": ui_data,
    }

    return {
        "status": "success",
        "data": data
    }
