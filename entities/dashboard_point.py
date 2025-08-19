"""
Path: entities/dashboard_point.py
"""

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DashboardPoint:
    "Punto de datos del dashboard"
    unixtime: int
    hr_counter1: int
    hr_counter2: Optional[int] = None
