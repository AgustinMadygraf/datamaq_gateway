"""
Path: infrastructure/fastapi/dashboard_adapter.py
"""

from typing import Optional
from fastapi import APIRouter, Query, Depends

from application.container import resolve_get_dashboard_data
from interface_adapters.controllers.dashboard_controller import get_dashboard, Periodo

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard.php")
def dashboard_endpoint(
    periodo: Periodo = Query("semana", regex="^(semana|turno|hora)$"),
    conta: Optional[int] = Query(None, description="timestamp de referencia en ms"),
    uc = Depends(resolve_get_dashboard_data),
):
    "Adaptador HTTP para get_dashboard"
    return get_dashboard(periodo, conta, uc)
