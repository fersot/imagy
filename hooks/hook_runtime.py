"""
Runtime hook para PyInstaller — Imagy.
Asegura que los assets y módulos dinámicos se encuentren correctamente
cuando la app corre desde el ejecutable.
"""

import sys
import os
from pathlib import Path


def resource_base():
    """Retorna el directorio raíz de recursos."""
    if getattr(sys, 'frozen', False):
        # Corriendo como ejecutable PyInstaller
        return Path(sys._MEIPASS)
    else:
        # Corriendo desde código fuente
        return Path(__file__).parent.parent


# Agregar el directorio base al sys.path para imports dinámicos
base = resource_base()
if str(base) not in sys.path:
    sys.path.insert(0, str(base))

# Forzar variable de entorno para que customtkinter encuentre sus assets
os.environ.setdefault('CUSTOMTKINTER_DATA', str(base / 'customtkinter'))
