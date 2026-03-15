"""
Frame para extraer paleta de colores de imágenes.
"""

import customtkinter as ctk

from ui import colors, fonts


class PaletteFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=colors.FRAMES_BG)
        ctk.CTkLabel(
            self,
            text="Palette — proximamente",
            font=fonts.FUENTE_BASE
        ).pack(expand=True)