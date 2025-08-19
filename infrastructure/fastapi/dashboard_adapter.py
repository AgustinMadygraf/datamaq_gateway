"""
Path: infrastructure/fastapi/dashboard_adapter.py
"""

from typing import Optional
from fastapi import APIRouter, Query

from interface_adapters.controllers.dashboard_controller import get_dashboard, Periodo
from application.container import get_dashboard_gateways

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard.php")
@router.get("/dashboard.php")
def dashboard_endpoint(
    periodo: Periodo = Query("semana", regex="^(semana|turno|hora)$"),
    conta: Optional[int] = Query(None, description="timestamp de referencia en ms"),
):
    "Adaptador HTTP para get_dashboard"
    dash_repo, formato_repo = get_dashboard_gateways()
    return get_dashboard(periodo, conta, dash_repo, formato_repo)
