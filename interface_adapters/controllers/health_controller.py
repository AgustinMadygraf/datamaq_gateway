"""
Path: interface_adapters/controllers/health_controller.py
"""

from interface_adapters.presenters.health_presenter import present_health

def get_health():
    "Obtiene el estado de salud del sistema"
    return present_health()
