"""
Servicios UI-agnosticos para el modulo LQIP / Base64.

Relacionado con:
    - app/modules/lqip.py: Logica de negocio original.
    - app/ui/frames/lqip/frame.py: Usa estas funciones.
"""

from app.modules.lqip import (
    batch_procesar,
    exportar_txt,
    exportar_json,
)

__all__ = ['batch_procesar', 'exportar_txt', 'exportar_json']