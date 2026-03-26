from app.ui.frames.palette.frame import PaletteFrame


def test_palette_frame_build(ui_root):
    frame = PaletteFrame(ui_root)
    ui_root.update_idletasks()

    assert hasattr(frame, "_btn_seleccionar")
    assert hasattr(frame, "_frame_preview")
