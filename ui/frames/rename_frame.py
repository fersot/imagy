"""
Frame para renombrar imágenes en lote.
"""

import customtkinter as ctk

from ui import colors, fonts


class RenameFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=colors.FRAMES_BG)
        ctk.CTkLabel(
            self,
            text="Rename — proximamente",
            font=fonts.FUENTE_BASE
        ).pack(expand=True)