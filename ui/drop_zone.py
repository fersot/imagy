"""
Zona de arrastre para subir imágenes.
Permite arrastrar archivos o buscarlos mediante diálogo.
"""

from tkinter import filedialog

import customtkinter as ctk
from tkinterdnd2 import DND_FILES

from ui import colors, fonts


class DropZone(ctk.CTkFrame):
    """Zona interactiva para soltar archivos de imagen."""
    
    def __init__(self, parent, on_drop, text='Arrastra imagenes aqui'):
        super().__init__(
            parent,
            height=160,
            border_width=2,
            border_color=colors.DROPOZONE_BORDER,
            fg_color=colors.DROPOZONE_BG,
            corner_radius=12
        )

        self.on_drop = on_drop

        ctk.CTkLabel(
            self,
            text=text,
            font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY
        ).pack(expand=True)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self._handle_drop)
        self.bind('<Button-1>', self._browse)

    def _handle_drop(self, event):
        """Procesa los archivos soltados en la zona."""
        paths = self.tk.splitlist(event.data)
        self.on_drop(list(paths))

    def _browse(self, event):
        """Abre el diálogo para seleccionar archivos."""
        files = filedialog.askopenfilenames(
            filetypes=[
                ('Imagenes', '*.jpg *.jpeg *.png *.webp *.gif *.bmp *.tiff *.avif *.ico')
            ]
        )

        if files:
            self.on_drop(list(files))