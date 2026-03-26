from app.ui.frames.resize.frame import ResizeFrame


def test_resize_frame_build(ui_root):
    frame = ResizeFrame(ui_root)
    ui_root.update_idletasks()

    assert hasattr(frame, "_btn_seleccionar")
    assert hasattr(frame, "_lista_frame")
    assert hasattr(frame, "_tab")
    assert hasattr(frame, "_frames")
