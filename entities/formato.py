"""
Path: entities/formato.py
"""

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Formato:
    "Formato de bobina"
    id_formato: int
    formato: Optional[str] = None
    ancho_bobina_mm: Optional[int] = None
