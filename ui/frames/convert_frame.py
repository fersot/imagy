"""
Frame para convertir imágenes a diferentes formatos.
"""

import customtkinter as ctk

from ui import colors, fonts


class ConvertFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=colors.FRAMES_BG)
        ctk.CTkLabel(
            self,
            text="Convert — proximamente",
            font=fonts.FUENTE_BASE
        ).pack(expand=True)