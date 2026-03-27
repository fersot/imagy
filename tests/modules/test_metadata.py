from pathlib import Path

from app.modules.metadata import leer_metadatos_safe, limpiar_exif, editar_exif


def test_leer_metadatos_safe(fixtures_dir: Path):
    entrada = fixtures_dir / "sample.jpg"
    data, error = leer_metadatos_safe(str(entrada))

    assert error is None
    assert isinstance(data, dict)


def test_limpiar_exif(tmp_path: Path, fixtures_dir: Path):
    entrada = fixtures_dir / "sample.jpg"
    salida = tmp_path / "sample_sin_exif.jpg"

    res = limpiar_exif(str(entrada), str(salida))
    assert Path(res["ruta_salida"]).exists()


def test_editar_exif(tmp_path: Path, fixtures_dir: Path):
    entrada = fixtures_dir / "sample.jpg"
    salida = tmp_path / "sample_edit_exif.jpg"

    ok, warning = editar_exif(
        str(entrada),
        str(salida),
        {"Artist": "Test", "Software": "Imagy"},
    )
    assert ok is True
