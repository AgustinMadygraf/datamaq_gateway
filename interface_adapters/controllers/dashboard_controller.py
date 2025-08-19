"""
Path: interface_adapters/controllers/dashboard_controller.py
"""

from typing import Optional
from fastapi import APIRouter, Query, Depends
from use_cases.get_dashboard_data import GetDashboardDataInput, Periodo
from application.container import resolve_get_dashboard_data
from interface_adapters.presenters.dashboard_presenter import DashboardResponse, present

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    periodo: Periodo = Query("semana", regex="^(semana|turno|hora)$"),
    conta: Optional[int] = Query(None, description="timestamp de referencia en ms"),
    uc = Depends(resolve_get_dashboard_data),
):
    "Ejecutar caso de uso para obtener datos del dashboard"
    out = uc.execute(GetDashboardDataInput(periodo=periodo, conta_ms=conta))
    return present(out)
