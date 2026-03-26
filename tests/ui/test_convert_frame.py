from app.ui.frames.convert.frame import ConvertFrame


def test_convert_frame_build(ui_root):
    frame = ConvertFrame(ui_root)
    ui_root.update_idletasks()

    assert hasattr(frame, "_btn_seleccionar")
    assert hasattr(frame, "_lista_frame")
    assert hasattr(frame, "_panel_opciones")
    assert hasattr(frame, "_seg_formato")
    assert hasattr(frame, "_btn_convertir")
