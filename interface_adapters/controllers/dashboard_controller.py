"""
Path: interface_adapters/controllers/dashboard_controller.py
"""

from use_cases.get_dashboard_data import GetDashboardData, GetDashboardDataInput, Periodo
from interface_adapters.presenters.dashboard_presenter import present
from interface_adapters.gateway.repositories import DashboardRepository, FormatoRepository

def get_dashboard(
    periodo: Periodo,
    conta: int,
    dash_repo: DashboardRepository,
    formato_repo: FormatoRepository
) -> dict:
    "Ejecutar caso de uso para obtener datos del dashboard"
    uc = GetDashboardData(dash_repo, formato_repo)
    out = uc.execute(GetDashboardDataInput(periodo=periodo, conta_ms=conta))
    return present(out)

# Expongo el tipo Periodo para uso en infraestructura
__all__ = ["get_dashboard", "Periodo"]
