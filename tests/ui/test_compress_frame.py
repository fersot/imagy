from app.ui.frames.compress.frame import CompressFrame


def test_compress_frame_build(ui_root):
    frame = CompressFrame(ui_root)
    ui_root.update_idletasks()

    assert hasattr(frame, "_btn_seleccionar")
    assert hasattr(frame, "_lista_frame")
    assert hasattr(frame, "_panel_opciones")
    assert hasattr(frame, "_btn_comprimir")
