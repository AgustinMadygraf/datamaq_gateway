"""
Path: infrastructure/fastapi/dashboard_adapter.py
"""

from typing import Optional
from fastapi import APIRouter, Query

from interface_adapters.controllers.dashboard_controller import get_dashboard, Periodo
from interface_adapters.presenters.dashboard_presenter import present, present_legacy
from application.container import get_dashboard_gateways


router = APIRouter(tags=["dashboard"])

@router.get("/v0/dashboard.php")
def dashboard_endpoint_v0(
    periodo: Periodo = Query("semana", regex="^(semana|turno|hora)$"),
    conta: Optional[str] = Query(None, description="timestamp de referencia en ms"),
):
    "Adaptador HTTP para get_dashboard (legacy)"
    dash_repo, formato_repo = get_dashboard_gateways()
    conta_int = None
    if conta is not None:
        conta_int = int(conta.replace('.', '').replace(',', ''))
    # Usar present_legacy para mantener formato legacy
    out = get_dashboard(periodo, conta_int, dash_repo, formato_repo)
    return present_legacy(out) if hasattr(out, 'periodo') else out

@router.get("/v1/dashboard.php")
def dashboard_endpoint_v1(
    periodo: Periodo = Query("semana", regex="^(semana|turno|hora)$"),
    conta: Optional[str] = Query(None, description="timestamp de referencia en ms"),
):
    "Adaptador HTTP para get_dashboard (v1 estandarizado)"
    dash_repo, formato_repo = get_dashboard_gateways()
    conta_int = None
    if conta is not None:
        conta_int = int(conta.replace('.', '').replace(',', ''))
    # Usar present para formato estandarizado
    out = get_dashboard(periodo, conta_int, dash_repo, formato_repo)
    resp = present(out) if hasattr(out, 'periodo') else out
    # Marcar ls_periodos y menos_periodo como deprecados en meta.deprecations
    if isinstance(resp, dict) and "data" in resp and "meta" in resp["data"]:
        resp["data"]["meta"]["deprecations"] = ["ls_periodos", "menos_periodo"]
    return resp

@router.get("/v1/meta/periodos")
def meta_periodos_endpoint():
    "Endpoint para exponer ls_periodos y menos_periodo en formato canónico"
    ls_periodos = {"semana": 604800, "turno": 28800, "hora": 7200}
    menos_periodo = {"semana": "turno", "turno": "hora", "hora": "hora"}
    return {
        "ls_periodos": ls_periodos,
        "menos_periodo": menos_periodo,
        "meta": {
            "schema_version": "1.0",
            "deprecations": []
        }
    }
