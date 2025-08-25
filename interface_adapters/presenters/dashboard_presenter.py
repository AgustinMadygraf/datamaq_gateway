"""
Path: interfaces_adapters/presenters/dashcboard_presenters.py
"""

from datetime import datetime, timezone
from typing import Optional, List, Any, Dict
import re
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
    series = []
    for p in output.rawdata:
        series.append({
            "t": datetime.fromtimestamp(p.unixtime, tz=timezone.utc).isoformat().replace('+00:00', 'Z'),
            "hr_counter1": p.hr_counter1 if p.hr_counter1 is not None else 0,
            "hr_counter2": p.hr_counter2 if p.hr_counter2 is not None else 0
        })
    if output.formato:
        # Ajusta el nombre del campo si es necesario (ancho_bobina_mm o ancho_bobina)
        ancho = getattr(output.formato, "ancho_bobina_mm", None)
        if ancho is None:
            ancho = getattr(output.formato, "ancho_bobina", None)

    raw_models = [
        DashboardPointLegacyModel(
            unixtime=p.unixtime,
            HR_COUNTER1=str(p.hr_counter1 if p.hr_counter1 is not None else 0),
            HR_COUNTER2=str(p.hr_counter2 if p.hr_counter2 is not None else 0),
        ) for p in output.rawdata
    ]

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

    def ms_to_iso(ms):
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat().replace('+00:00', 'Z')

    inicio_iso = ms_to_iso(ui_data["preConta"])
    fin_iso = ms_to_iso(ui_data["postConta"])

    # Añadir campo t ISO-8601 y espejos numéricos en cada rawdata
    rawdata_with_t = []
    for i, m in enumerate(raw_models):
        d = m.dict()
        d["t"] = datetime.fromtimestamp(d["unixtime"], tz=timezone.utc).isoformat().replace('+00:00', 'Z')
        # Espejos numéricos
        # Usamos output.rawdata[i] para obtener el valor original como int
        d["hr_counter1_num"] = output.rawdata[i].hr_counter1 if output.rawdata[i].hr_counter1 is not None else 0
        d["hr_counter2_num"] = output.rawdata[i].hr_counter2 if output.rawdata[i].hr_counter2 is not None else 0
        rawdata_with_t.append(d)

    # Construir producto.formato y producto.web_width_mm
    producto = None
    if output.formato:
        # Intentar extraer medidas del string formato si existe
        formato_str = output.formato.formato or ""
        width_mm = gusset_mm = height_mm = None
        # Ejemplo: "12 X 08 X 26" => width=12, gusset=8, height=26
        match = re.match(r"(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+)", formato_str)
        if match:
            width_mm = int(match.group(1))
            gusset_mm = int(match.group(2))
            height_mm = int(match.group(3))
        producto = {
            "formato": {
                "width_mm": width_mm,
                "gusset_mm": gusset_mm,
                "height_mm": height_mm
            },
            "web_width_mm": float(output.formato.ancho_bobina_mm) if output.formato.ancho_bobina_mm is not None else None
        }

    data = {
        "meta": {
            "schema_version": "1.0",  # Actualiza según versión
            "timezone": "America/Argentina/Buenos_Aires",
            "inicio": inicio_iso,
            "fin": fin_iso
        },
        "periodo": output.periodo,
        "series": series,
        "features": {
            "velocidad_ultima_bpm": output.vel_ult
        },
        "producto": producto
    }

    return data

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
