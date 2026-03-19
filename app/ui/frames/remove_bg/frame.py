"""
UI para el modulo de eliminacion de fondo de imagenes.
Permite quitar el fondo de una o varias imagenes usando IA.

Relacionado con:
    - app/ui/frames/base.py: Clase base de la que hereda.
    - app/ui/frames/remove_bg/state.py: Estado de la interfaz.
    - app/ui/frames/remove_bg/services.py: Servicios de logica.
    - app/translations/__init__.py: Traducciones de la UI.
"""

from __future__ import annotations

import threading
from tkinter import filedialog

import customtkinter as ctk

from app.ui import colors, fonts
from app.translations import t
from app.ui.frames.base import BaseFrame
from app.ui.frames.remove_bg.services import (
    batch_quitar_fondo,
    rembg_disponible,
    modelo_descargado,
)
from app.ui.frames.remove_bg.state import RemoveBgState


class RemoveBgFrame(BaseFrame):
    """
    Frame del modulo de eliminacion de fondo.

    Permite seleccionar imagenes, elegir el tipo de fondo
    resultante y procesar en lote usando IA (rembg/U2Net).
    """

    def __init__(self, parent):
        """
        Inicializa el frame de eliminacion de fondo.

        Args:
            parent: Widget padre.
        """
        self._state = RemoveBgState()
        super().__init__(parent, t('remove_bg_title'))

    def _build_content(self):
        """
        Construye el contenido especifico del modulo.

        Incluye aviso de dependencia, boton de seleccion,
        lista de archivos, panel de opciones de fondo
        y boton de procesar.
        """
        # Aviso si rembg no esta instalado
        if not rembg_disponible():
            self._construir_aviso_dependencia()
            return

        # Aviso de descarga del modelo (primera vez)
        if not modelo_descargado():
            self._construir_aviso_modelo()

        # Boton para seleccionar imagenes
        self._btn_seleccionar = self._crear_boton_seleccionar(self)
        self._btn_seleccionar.grid(row=1, column=0, padx=28, pady=8, sticky='ew')

        # Lista de archivos seleccionados
        self._lista_frame = self._crear_lista_archivos(self, height=200)
        self._lista_frame.grid(row=2, column=0, padx=28, pady=8, sticky='ew')
        self._lista_frame.grid_columnconfigure(0, weight=1)

        # Label de lista vacia
        self._lbl_lista_vacia = self._crear_lista_vacia(self._lista_frame)
        self._lbl_lista_vacia.pack(pady=12)

        # Panel de opciones de fondo
        self._panel_opciones = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=colors.PANEL_BG,
            border_width=1,
            border_color=colors.SIDEBAR_SEPARATOR
        )
        self._panel_opciones.grid(row=3, column=0, padx=28, pady=8, sticky='ew')
        self._panel_opciones.grid_columnconfigure(1, weight=1)
        self._construir_opciones()

    def _construir_aviso_dependencia(self):
        """
        Muestra un panel de aviso cuando rembg no esta instalado.
        """
        panel = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=colors.PANEL_BG,
            border_width=1,
            border_color=colors.SIDEBAR_SEPARATOR
        )
        panel.grid(row=1, column=0, padx=28, pady=8, sticky='ew')
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text=t('rembg_not_installed'), # type: ignore
            font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_COLOR,
            justify='center'
        ).grid(row=0, column=0, padx=16, pady=(16, 8))

        ctk.CTkLabel(
            panel,
            text='pip install rembg onnxruntime',
            font=ctk.CTkFont(family='Courier New', size=13),
            text_color=colors.ACENTO,
            fg_color=colors.SIDEBAR_BG,
            corner_radius=6,
        ).grid(row=1, column=0, padx=16, pady=(0, 16), ipadx=12, ipady=6)

    def _construir_aviso_modelo(self):
        """
        Muestra un aviso sobre la descarga del modelo en el primer uso.
        """
        aviso = ctk.CTkFrame(
            self,
            corner_radius=8,
            fg_color=colors.SIDEBAR_BG,
            border_width=1,
            border_color=colors.ACENTO_DIMMED
        )
        aviso.grid(row=0, column=0, padx=28, pady=(0, 0), sticky='ew')
        aviso.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            aviso,
            text=t('model_first_download'), # type: ignore
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY,
            justify='center',
            wraplength=500
        ).grid(row=0, column=0, padx=16, pady=10)

    def _construir_opciones(self):
        """
        Construye los controles del panel de opciones.

        Incluye selector de fondo resultante, input de color
        custom y boton de procesar.
        """
        p = self._panel_opciones

        # Label de tipo de fondo
        ctk.CTkLabel(
            p, text=t('background_type'), # type: ignore
            font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY, anchor='w'
        ).grid(row=0, column=0, padx=(16, 12), pady=(16, 8), sticky='w')

        # Selector de modo de fondo
        self._seg_fondo = ctk.CTkSegmentedButton(
            p,
            values=[
                t('bg_transparent'),
                t('bg_white'),
                t('bg_black'),
            ],
            variable=self._state.modo_fondo,
            font=fonts.FUENTE_CHICA,
            selected_color=colors.ACENTO,
            selected_hover_color=colors.ACENTO_HOVER,
            unselected_color=colors.SIDEBAR_BG,
            unselected_hover_color=colors.SIDEBAR_HOVER,
            text_color=colors.TEXT_COLOR,
            command=self._actualizar_modo_fondo
        )
        self._seg_fondo.grid(row=0, column=1, padx=(0, 16), pady=(16, 8), sticky='w')

        # Aviso de transparencia (solo PNG)
        self._lbl_aviso_transparencia = ctk.CTkLabel(
            p,
            text=t('transparency_png_only'), # type: ignore
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY,
            anchor='w'
        )
        self._lbl_aviso_transparencia.grid(
            row=1, column=0, columnspan=2, padx=16, pady=(0, 8), sticky='w'
        )

        # Boton de procesar
        self._btn_procesar = ctk.CTkButton(
            p,
            text=t('remove_bg_btn'), # type: ignore
            height=40,
            corner_radius=8,
            font=fonts.FUENTE_BASE,
            fg_color=colors.ACENTO,
            text_color=colors.TEXT_ACTIVE,
            hover_color=colors.ACENTO_HOVER,
            command=self._procesar
        )
        self._btn_procesar.grid(
            row=2, column=0, columnspan=2,
            padx=16, pady=(0, 16), sticky='ew'
        )

    def _actualizar_modo_fondo(self, modo):
        """
        Actualiza el aviso segun el modo de fondo seleccionado.

        Args:
            modo: Modo de fondo seleccionado.
        """
        if modo == t('bg_transparent'):
            self._lbl_aviso_transparencia.configure(
                text=t('transparency_png_only')
            )
        else:
            self._lbl_aviso_transparencia.configure(text='')

    def _cargar_imagenes(self, rutas):
        """
        Carga las imagenes seleccionadas.

        Sobrescribe el metodo de BaseFrame para guardar
        las rutas en el estado del modulo.

        Args:
            rutas: Lista de rutas de archivos a cargar.
        """
        super()._cargar_imagenes(rutas)
        self._state.imagenes = list(rutas)
        n = len(rutas)
        suffix = t('images_loaded') if n > 1 else t('image_loaded')
        self._lbl_info.configure(text=f'{n} {suffix}')

    def _procesar(self):
        """
        Inicia el proceso de eliminacion de fondo en segundo plano.
        """
        if not self._imagenes:
            self._lbl_info.configure(text=t('load_images_first'))
            return

        carpeta = filedialog.askdirectory(title=t('select_output_folder'))
        if not carpeta:
            return

        self._btn_procesar.configure(state='disabled', text=t('processing'))
        threading.Thread(target=self._proceso, args=(carpeta,), daemon=True).start()

    def _proceso(self, carpeta):
        """
        Ejecuta la eliminacion de fondo en segundo plano.

        Args:
            carpeta: Ruta de la carpeta de salida.
        """
        color_fondo = self._state.obtener_color_fondo()

        res = batch_quitar_fondo(
            self._imagenes,
            carpeta,
            color_fondo=color_fondo,
        )
        self.after(0, lambda: self._finalizar(res['ok'], res['errores']))

    def _finalizar(self, ok, errores):
        """
        Muestra el resultado final del procesamiento.

        Args:
            ok: Cantidad de imagenes procesadas correctamente.
            errores: Cantidad de errores ocurridos.
        """
        self._btn_procesar.configure(state='normal', text=t('remove_bg_btn'))
        suffix = t('images_loaded') if ok > 1 else t('image_loaded')
        msg = f'{ok} {suffix} {t("processed")}'
        if errores:
            msg += f'  -  {errores} {t("error_occurred")}'
        self._lbl_info.configure(text=msg)