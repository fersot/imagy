from app.ui.frames.remove_bg.frame import RemoveBgFrame


def test_remove_bg_frame_build(monkeypatch, ui_root):
    # Evitar checks pesados en background
    monkeypatch.setattr(RemoveBgFrame, "_inicializar_en_background", lambda self: self._build_content_ready(True, True))

    frame = RemoveBgFrame(ui_root)
    ui_root.update_idletasks()

    assert hasattr(frame, "_btn_seleccionar")
    assert hasattr(frame, "_lista_frame")
    assert hasattr(frame, "_btn_procesar")
