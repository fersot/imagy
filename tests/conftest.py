import sys
from pathlib import Path

# Asegurar que el root del proyecto esté en sys.path para importar app.*
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pathlib import Path  # noqa: E402

import pytest  # noqa: E402
from PIL import Image  # noqa: E402
import customtkinter as ctk  # noqa: E402
import tkinter  # noqa: E402


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def fixtures_dir() -> Path:
    return FIXTURES_DIR


def assert_image_size(path: Path, expected_size: tuple[int, int]):
    with Image.open(path) as img:
        assert img.size == expected_size


@pytest.fixture()
def ui_root():
    try:
        root = ctk.CTk()
    except tkinter.TclError:
        pytest.skip("Tk no disponible en el entorno de test")
    root.withdraw()
    yield root
    root.destroy()
