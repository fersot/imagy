import pytest

from app.modules.remove_bg import rembg_disponible


def test_rembg_disponible():
    if not rembg_disponible():
        pytest.skip("rembg no disponible en el entorno de test")
