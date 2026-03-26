from pathlib import Path

from app.modules.rename import generar_nombres_preview, renombrar_archivos


def test_preview_y_renombrar(tmp_path: Path, fixtures_dir: Path):
    origen = fixtures_dir / "sample.jpg"
    copia = tmp_path / "sample.jpg"
    copia.write_bytes(origen.read_bytes())

    opciones = {
        "numeracion_activa": True,
        "prefijo": "img",
        "inicio": 1,
        "fecha_activa": False,
        "caso": "sin_cambio",
    }

    preview = generar_nombres_preview([str(copia)], opciones)
    assert preview
    assert preview[0][1].startswith("img_")

    res = renombrar_archivos([str(copia)], opciones)
    assert res["ok"] == 1

    renombrado = tmp_path / f"{preview[0][1]}"
    assert renombrado.exists()
