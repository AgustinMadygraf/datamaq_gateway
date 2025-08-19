"""
Path: interface_adapters/controllers/dashboard_controller.py
"""

from use_cases.get_dashboard_data import GetDashboardDataInput, Periodo
from interface_adapters.presenters.dashboard_presenter import present

def get_dashboard(periodo: Periodo, conta: int, uc) -> dict:
    "Ejecutar caso de uso para obtener datos del dashboard"
    out = uc.execute(GetDashboardDataInput(periodo=periodo, conta_ms=conta))
    return present(out)

# Expongo el tipo Periodo para uso en infraestructura
__all__ = ["get_dashboard", "Periodo"]
