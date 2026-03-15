"""
Aplicación principal Yagua.
Contiene la clase principal que inicializa la ventana y componentes.
"""

import os
import sys

import customtkinter as ctk
from PIL import Image, ImageTk

from ui import fonts
from ui.main_window import MainWindow


class YaguaApp(ctk.CTk):
    """Ventana principal de la aplicación Yagua."""
    
    def __init__(self):
        super().__init__()
        fonts.inicializar_fuentes()
        self.title('Yagua - Image Editor')
        self.geometry('1000x500')
        self.minsize(900, 600)
        self._setup_icon()
        self.main_window = MainWindow(self)
        self.main_window.pack(fill='both', expand=True)
    
    def _setup_icon(self):
        """Configura el icono de la ventana según la plataforma."""
        if sys.platform == 'win32':
            self.iconbitmap('assets/icon.ico')
        else:
            img = Image.open('assets/icon.png')
            self.iconphoto(True, ImageTk.PhotoImage(img))
