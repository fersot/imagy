from app.ui.frames.lqip.frame import LqipFrame


def test_lqip_frame_build(ui_root):
    frame = LqipFrame(ui_root)
    ui_root.update_idletasks()

    assert hasattr(frame, "_btn_seleccionar")
    assert hasattr(frame, "_lista_frame")
    assert hasattr(frame, "_seg_modo")
    assert hasattr(frame, "_btn_procesar")
