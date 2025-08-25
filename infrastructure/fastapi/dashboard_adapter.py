"""
Path: infrastructure/fastapi/dashboard_adapter.py
"""

from typing import Optional
from fastapi import APIRouter, Query

from interface_adapters.controllers.dashboard_controller import get_dashboard, Periodo
from application.container import get_dashboard_gateways

router = APIRouter(tags=["dashboard"])

@router.get("/v0/dashboard.php")
def dashboard_endpoint_v0(
    periodo: Periodo = Query("semana", regex="^(semana|turno|hora)$"),
    conta: Optional[str] = Query(None, description="timestamp de referencia en ms"),
):
    "Adaptador HTTP para get_dashboard"
    dash_repo, formato_repo = get_dashboard_gateways()
    conta_int = None
    if conta is not None:
        # Reemplaza comas y puntos, luego convierte a entero
        conta_int = int(conta.replace('.', '').replace(',', ''))
    return get_dashboard(periodo, conta_int, dash_repo, formato_repo)

@router.get("/v1/dashboard.php")
def dashboard_endpoint_v1(
    periodo: Periodo = Query("semana", regex="^(semana|turno|hora)$"),
    conta: Optional[str] = Query(None, description="timestamp de referencia en ms"),
):
    "Adaptador HTTP para get_dashboard"
    dash_repo, formato_repo = get_dashboard_gateways()
    conta_int = None
    if conta is not None:
        # Reemplaza comas y puntos, luego convierte a entero
        conta_int = int(conta.replace('.', '').replace(',', ''))
    return get_dashboard(periodo, conta_int, dash_repo, formato_repo)
