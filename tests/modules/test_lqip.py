from pathlib import Path

from app.modules.lqip import batch_procesar


def test_lqip_batch(tmp_path: Path, fixtures_dir: Path):
    entrada = fixtures_dir / "sample.png"

    res = batch_procesar([str(entrada)], modo="lqip", ancho=16, blur=1.0, calidad_lqip=40)
    assert res["ok"] == 1
    assert res["resultados"]
    assert res["resultados"][0]["data_uri"].startswith("data:image/jpeg;base64,")
