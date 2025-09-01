"""
Presentador moderno para dashboard
"""
from datetime import datetime, timezone
from typing import Optional
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

def present(output: GetDashboardDataOutput) -> dict:
    "Presentar los datos del dashboard en formato moderno"
    series = []
    for p in output.rawdata:
        series.append({
            "t": datetime.fromtimestamp(p.unixtime, tz=timezone.utc).isoformat().replace('+00:00', 'Z'),
            "hr_counter1": p.hr_counter1 if p.hr_counter1 is not None else 0,
            "hr_counter2": p.hr_counter2 if p.hr_counter2 is not None else 0
        })
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
    producto = None
    if output.formato:
        formato_str = output.formato.formato or ""
        width_mm = gusset_mm = height_mm = None
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
            "schema_version": "1.0",
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
