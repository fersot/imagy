from app.ui.frames.metadata.frame import MetadataFrame
from app.translations import t


def test_metadata_frame_build(ui_root):
    frame = MetadataFrame(ui_root)
    ui_root.update_idletasks()

    assert hasattr(frame, "_tab")
    assert hasattr(frame, "_frames")
    # Verificar que se crearon los tabs principales
    assert t("view") in frame._frames
    assert t("edit") in frame._frames
    assert t("clean_batch") in frame._frames
