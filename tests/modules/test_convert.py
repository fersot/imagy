from pathlib import Path

from app.modules.convert import batch_convertir_safe


def test_convertir_a_png(tmp_path: Path, fixtures_dir: Path):
    entrada = fixtures_dir / "sample.jpg"

    res = batch_convertir_safe([str(entrada)], "PNG", str(tmp_path), calidad=90)

    salida = tmp_path / "sample.png"
    assert salida.exists()
    assert res["ok"] == 1
