"""
Frame del módulo Redimensionar / Recortar / Canvas.
"""

import threading
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image

from modules.resize import (
    redimensionar, recortar, agregar_canvas,
    PRESETS_LISTA, RATIOS
)
from modules.compress import formatear_bytes
from ui import colors, fonts
from utils import tintar_icono


class ResizeFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=colors.FRAMES_BG)
        self._imagenes: list[str] = []
        self._thumbs: list[ctk.CTkImage] = []
        self._filas_lista: list[ctk.CTkLabel] = []
        self._modo_resize: ctk.StringVar = ctk.StringVar(value='Porcentaje')
        self._mantener_ratio: ctk.BooleanVar = ctk.BooleanVar(value=True)
        self._pct_var: ctk.IntVar = ctk.IntVar(value=50)
        self._ratio_var: ctk.StringVar = ctk.StringVar(value='1:1')
        self._color_fondo: ctk.StringVar = ctk.StringVar(value='Blanco')
        self._preset_var: ctk.StringVar = ctk.StringVar(value=PRESETS_LISTA[0])
        self._build()

    # ─── BUILD ────────────────────────────────────────────────────────────────

    def _build(self):
        self.grid_columnconfigure(0, weight=1)

        # Título + limpiar
        fila_titulo = ctk.CTkFrame(self, fg_color='transparent')
        fila_titulo.grid(row=0, column=0, padx=28, pady=(26, 8), sticky='ew')
        fila_titulo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            fila_titulo, text='Redimensionar',
            font=fonts.FUENTE_TITULO,
            text_color=colors.TEXT_COLOR, anchor='w'
        ).grid(row=0, column=0, sticky='w')

        ctk.CTkButton(
            fila_titulo, text='Limpiar',
            width=80, height=30, corner_radius=8,
            font=fonts.FUENTE_CHICA,
            fg_color='#FFFFFF', text_color='#1A1A1A',
            hover_color='#EEEEEE', border_width=0,
            command=self._limpiar
        ).grid(row=0, column=1, sticky='e')

        # Tabs
        self._tab = ctk.CTkSegmentedButton(
            self,
            values=['Redimensionar', 'Recortar', 'Canvas'],
            font=fonts.FUENTE_BASE,
            selected_color="#949494",
            selected_hover_color="#949494",
            unselected_color=colors.PANEL_BG,
            unselected_hover_color=colors.SIDEBAR_HOVER,
            text_color=colors.TEXT_COLOR,
            command=self._cambiar_tab
        )
        self._tab.set('Redimensionar')
        self._tab.grid(row=1, column=0, padx=28, pady=(0, 8), sticky='ew')

        # Botón seleccionar imágenes
        ctk.CTkButton(
            self,
            text='Seleccionar imágenes',
            height=40,
            corner_radius=8,
            font=fonts.FUENTE_BASE,
            fg_color=colors.PANEL_BG,
            border_width=1,
            border_color=colors.SIDEBAR_SEPARATOR,
            text_color=colors.TEXT_COLOR,
            hover_color=colors.SIDEBAR_HOVER,
            image=tintar_icono('assets/icons/upload.png', colors.ICON_COLOR),
            compound='left',
            command=self._explorar
        ).grid(row=2, column=0, padx=28, pady=(0, 8), sticky='ew')

        # Lista de archivos
        self._lista = ctk.CTkScrollableFrame(
            self, corner_radius=10,
            fg_color=colors.PANEL_BG,
            border_width=0,
            scrollbar_button_color=colors.SIDEBAR_SEPARATOR,
            scrollbar_button_hover_color=colors.ACENTO_DIMMED,
            height=120
        )
        self._lista.grid(row=3, column=0, padx=28, pady=(0, 8), sticky='ew')
        self._lista.grid_columnconfigure(0, weight=1)

        self._lbl_lista_vacia = ctk.CTkLabel(
            self._lista,
            text='Sin imágenes cargadas',
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY
        )
        self._lbl_lista_vacia.pack(pady=12)

        # Contenedor de tabs
        self._contenedor = ctk.CTkFrame(self, fg_color='transparent')
        self._contenedor.grid(row=4, column=0, padx=28, sticky='ew')
        self._contenedor.grid_columnconfigure(0, weight=1)

        self._frames: dict[str, ctk.CTkFrame] = {
            'Redimensionar': self._build_tab_resize(),
            'Recortar':      self._build_tab_crop(),
            'Canvas':        self._build_tab_canvas(),
        }
        for f in self._frames.values():
            f.grid(row=0, column=0, sticky='ew')

        self._lbl_info = ctk.CTkLabel(
            self, text='',
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY
        )
        self._lbl_info.grid(row=5, column=0, pady=(0, 4))

        self._cambiar_tab('Redimensionar')

    # ─── TAB REDIMENSIONAR ────────────────────────────────────────────────────

    def _build_tab_resize(self) -> ctk.CTkFrame:
        f = ctk.CTkFrame(self._contenedor, fg_color='transparent')
        f.grid_columnconfigure(0, weight=1)

        panel = ctk.CTkFrame(
            f, corner_radius=12, fg_color=colors.PANEL_BG,
            border_width=1, border_color=colors.SIDEBAR_SEPARATOR
        )
        panel.grid(row=0, column=0, sticky='ew')
        panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel, text='Modo', font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY, anchor='w'
        ).grid(row=0, column=0, padx=(16, 12), pady=(16, 8), sticky='w')

        ctk.CTkSegmentedButton(
            panel,
            values=['Porcentaje', 'Píxeles', 'Preset'],
            variable=self._modo_resize,
            font=fonts.FUENTE_CHICA,
            selected_color="#949494",
            selected_hover_color="#949494",
            unselected_color=colors.SIDEBAR_BG,
            unselected_hover_color=colors.SIDEBAR_HOVER,
            text_color=colors.TEXT_COLOR,
            command=self._actualizar_modo_resize
        ).grid(row=0, column=1, padx=(0, 16), pady=(16, 8), sticky='w')

        self._frame_controles_resize = ctk.CTkFrame(panel, fg_color='transparent')
        self._frame_controles_resize.grid(
            row=1, column=0, columnspan=2, padx=16, pady=(0, 8), sticky='ew'
        )
        self._frame_controles_resize.grid_columnconfigure(1, weight=1)

        self._frame_ratio = ctk.CTkFrame(panel, fg_color='transparent')
        self._frame_ratio.grid(
            row=2, column=0, columnspan=2, padx=16, pady=(0, 8), sticky='ew'
        )
        ctk.CTkCheckBox(
            self._frame_ratio,
            text='Mantener relación de aspecto',
            variable=self._mantener_ratio,
            font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY,
            fg_color=colors.ACENTO,
            hover_color=colors.ACENTO_HOVER,
            border_color=colors.SIDEBAR_SEPARATOR,
            checkmark_color=colors.TEXT_ACTIVE,
        ).pack(anchor='w')

        self._btn_resize = ctk.CTkButton(
            panel, text='Redimensionar', height=40, corner_radius=8,
            font=fonts.FUENTE_BASE, fg_color=colors.ACENTO,
            text_color=colors.TEXT_ACTIVE, hover_color=colors.ACENTO_HOVER,
            command=self._ejecutar_resize
        )
        self._btn_resize.grid(
            row=3, column=0, columnspan=2, padx=16, pady=(0, 16), sticky='ew'
        )

        self._actualizar_modo_resize('Porcentaje')
        return f

    def _actualizar_modo_resize(self, modo: str):
        for w in self._frame_controles_resize.winfo_children():
            w.destroy()

        fc = self._frame_controles_resize

        if modo == 'Píxeles':
            self._frame_ratio.grid()
        else:
            self._frame_ratio.grid_remove()

        if modo == 'Porcentaje':
            fc.grid_columnconfigure(0, weight=0)
            fc.grid_columnconfigure(1, weight=1)
            fc.grid_columnconfigure(2, weight=0)

            self._lbl_pct = ctk.CTkLabel(
                fc, text='50%', font=fonts.FUENTE_BASE,
                text_color=colors.ACENTO, fg_color='transparent', width=36
            )

            ctk.CTkSlider(
                fc, from_=1, to=200, variable=self._pct_var,
                button_color=colors.ACENTO,
                button_hover_color=colors.ACENTO_HOVER,
                progress_color=colors.ACENTO,
                fg_color=colors.SIDEBAR_SEPARATOR,
                command=lambda v: self._lbl_pct.configure(text=f'{int(v)}%')
            ).grid(row=0, column=0, columnspan=2, sticky='ew', padx=(0, 8))

            self._lbl_pct.grid(row=0, column=2)

        elif modo == 'Píxeles':
            fc.grid_columnconfigure(0, weight=0)
            fc.grid_columnconfigure(1, weight=0)
            fc.grid_columnconfigure(2, weight=0)
            fc.grid_columnconfigure(3, weight=0)

            ctk.CTkLabel(
                fc, text='Ancho', font=fonts.FUENTE_CHICA,
                text_color=colors.TEXT_GRAY
            ).grid(row=0, column=0, padx=(0, 4), sticky='w')

            self._entry_ancho = ctk.CTkEntry(
                fc, width=90, font=fonts.FUENTE_BASE,
                fg_color=colors.FRAMES_BG,
                border_color=colors.SIDEBAR_SEPARATOR,
                text_color=colors.TEXT_COLOR,
                placeholder_text='1920',
                placeholder_text_color=colors.TEXT_GRAY
            )
            self._entry_ancho.grid(row=0, column=1, padx=(0, 16))

            ctk.CTkLabel(
                fc, text='Alto', font=fonts.FUENTE_CHICA,
                text_color=colors.TEXT_GRAY
            ).grid(row=0, column=2, padx=(0, 4), sticky='w')

            self._entry_alto = ctk.CTkEntry(
                fc, width=90, font=fonts.FUENTE_BASE,
                fg_color=colors.FRAMES_BG,
                border_color=colors.SIDEBAR_SEPARATOR,
                text_color=colors.TEXT_COLOR,
                placeholder_text='1080',
                placeholder_text_color=colors.TEXT_GRAY
            )
            self._entry_alto.grid(row=0, column=3)

        elif modo == 'Preset':
            fc.grid_columnconfigure(0, weight=1)

            ctk.CTkOptionMenu(
                fc,
                values=PRESETS_LISTA,
                variable=self._preset_var,
                font=fonts.FUENTE_BASE,
                fg_color=colors.SIDEBAR_BG,
                button_color=colors.ACENTO,
                button_hover_color=colors.ACENTO_HOVER,
                text_color=colors.TEXT_COLOR,
                dropdown_fg_color=colors.PANEL_BG,
                dropdown_text_color=colors.TEXT_COLOR,
                dropdown_hover_color=colors.SIDEBAR_HOVER,
            ).grid(row=0, column=0, sticky='ew')

    # ─── TAB RECORTAR ─────────────────────────────────────────────────────────
    def _build_tab_crop(self) -> ctk.CTkFrame:
        f = ctk.CTkFrame(self._contenedor, fg_color='transparent')
        f.grid_columnconfigure(0, weight=1)

        panel = ctk.CTkFrame(
            f, corner_radius=12, fg_color=colors.PANEL_BG,
            border_width=1, border_color=colors.SIDEBAR_SEPARATOR
        )
        panel.grid(row=0, column=0, sticky='ew')
        panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel, text='Ratio', font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY, anchor='w'
        ).grid(row=0, column=0, padx=(16, 12), pady=(16, 8), sticky='w')

        ctk.CTkOptionMenu(
            panel,
            values=list(RATIOS.keys()),
            variable=self._ratio_var,
            font=fonts.FUENTE_BASE,
            fg_color=colors.SIDEBAR_BG,
            button_color=colors.ACENTO,
            button_hover_color=colors.ACENTO_HOVER,
            text_color=colors.TEXT_COLOR,
            dropdown_fg_color=colors.PANEL_BG,
            dropdown_text_color=colors.TEXT_COLOR,
            dropdown_hover_color=colors.SIDEBAR_HOVER,
        ).grid(row=0, column=1, padx=(0, 16), pady=(16, 8), sticky='w')

        ctk.CTkLabel(
            panel,
            text='Recorte centrado — la imagen se recorta desde el centro.',
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY, anchor='w'
        ).grid(row=1, column=0, columnspan=2, padx=16, pady=(0, 8), sticky='w')

        self._btn_crop = ctk.CTkButton(
            panel, text='Recortar', height=40, corner_radius=8,
            font=fonts.FUENTE_BASE, fg_color=colors.ACENTO,
            text_color=colors.TEXT_ACTIVE, hover_color=colors.ACENTO_HOVER,
            command=self._ejecutar_crop
        )
        self._btn_crop.grid(
            row=2, column=0, columnspan=2, padx=16, pady=(0, 16), sticky='ew'
        )
        return f

    # ─── TAB CANVAS ───────────────────────────────────────────────────────────
    def _build_tab_canvas(self) -> ctk.CTkFrame:
        f = ctk.CTkFrame(self._contenedor, fg_color='transparent')
        f.grid_columnconfigure(0, weight=1)

        panel = ctk.CTkFrame(
            f, corner_radius=12, fg_color=colors.PANEL_BG,
            border_width=1, border_color=colors.SIDEBAR_SEPARATOR
        )
        panel.grid(row=0, column=0, sticky='ew')
        panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel, text='Tamaño', font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY, anchor='w'
        ).grid(row=0, column=0, padx=(16, 12), pady=(16, 8), sticky='w')

        fila_dim = ctk.CTkFrame(panel, fg_color='transparent')
        fila_dim.grid(row=0, column=1, padx=(0, 16), pady=(16, 8), sticky='w')

        self._canvas_ancho = ctk.CTkEntry(
            fila_dim, width=80, font=fonts.FUENTE_BASE,
            fg_color=colors.FRAMES_BG,
            border_color=colors.SIDEBAR_SEPARATOR,
            text_color=colors.TEXT_COLOR,
            placeholder_text='1080',
            placeholder_text_color=colors.TEXT_GRAY
        )
        self._canvas_ancho.pack(side='left', padx=(0, 8))

        ctk.CTkLabel(
            fila_dim, text='×', font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY
        ).pack(side='left', padx=(0, 8))

        self._canvas_alto = ctk.CTkEntry(
            fila_dim, width=80, font=fonts.FUENTE_BASE,
            fg_color=colors.FRAMES_BG,
            border_color=colors.SIDEBAR_SEPARATOR,
            text_color=colors.TEXT_COLOR,
            placeholder_text='1080',
            placeholder_text_color=colors.TEXT_GRAY
        )
        self._canvas_alto.pack(side='left')

        ctk.CTkLabel(
            panel, text='Fondo', font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY, anchor='w'
        ).grid(row=1, column=0, padx=(16, 12), pady=8, sticky='w')

        ctk.CTkSegmentedButton(
            panel,
            values=['Blanco', 'Negro', 'Transparente'],
            variable=self._color_fondo,
            font=fonts.FUENTE_CHICA,
            selected_color="#949494",
            selected_hover_color="#949494",
            unselected_color=colors.SIDEBAR_BG,
            unselected_hover_color=colors.SIDEBAR_HOVER,
            text_color=colors.TEXT_COLOR,
            command=self._actualizar_fondo_opciones
        ).grid(row=1, column=1, padx=(0, 16), pady=8, sticky='w')

        self._lbl_aviso_fondo = ctk.CTkLabel(
            panel, text='',
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY, anchor='w'
        )
        self._lbl_aviso_fondo.grid(
            row=2, column=0, columnspan=2, padx=16, pady=(0, 4), sticky='w'
        )

        self._btn_canvas = ctk.CTkButton(
            panel, text='Aplicar canvas', height=40, corner_radius=8,
            font=fonts.FUENTE_BASE, fg_color=colors.ACENTO,
            text_color=colors.TEXT_ACTIVE, hover_color=colors.ACENTO_HOVER,
            command=self._ejecutar_canvas
        )
        self._btn_canvas.grid(
            row=2, column=0, columnspan=2, padx=16, pady=(0, 16), sticky='ew'
        )
        return f

    # ─── LÓGICA ───────────────────────────────────────────────────────────────

    def _explorar(self):
        archivos = filedialog.askopenfilenames(
            title='Seleccioná imágenes',
            filetypes=[('Imágenes', '*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.avif')]
        )
        if not archivos:
            return

        self._imagenes = list(archivos)
        self._thumbs.clear()
        self._filas_lista.clear()

        for w in self._lista.winfo_children():
            w.destroy()

        for ruta in self._imagenes:
            p = Path(ruta)
            fila = ctk.CTkFrame(
                self._lista, fg_color=colors.SIDEBAR_BG, corner_radius=8
            )
            fila.pack(fill='x', pady=3, padx=2)
            fila.grid_columnconfigure(1, weight=1)

            lbl_thumb = ctk.CTkLabel(
                fila, text='', width=44, height=44, fg_color='transparent'
            )
            lbl_thumb.grid(row=0, column=0, padx=(8, 0), pady=6)
            self._filas_lista.append(lbl_thumb)

            info = ctk.CTkFrame(fila, fg_color='transparent')
            info.grid(row=0, column=1, padx=(10, 8), pady=6, sticky='w')

            nombre = p.name if len(p.name) <= 32 else p.name[:29] + '...'
            ctk.CTkLabel(
                info, text=nombre, font=fonts.FUENTE_BASE,
                text_color=colors.TEXT_COLOR, anchor='w'
            ).pack(anchor='w')
            ctk.CTkLabel(
                info,
                text=f'{formatear_bytes(p.stat().st_size)}  ·  {p.suffix.upper().lstrip(".")}',
                font=fonts.FUENTE_CHICA,
                text_color=colors.TEXT_GRAY, anchor='w'
            ).pack(anchor='w')

        threading.Thread(
            target=self._generar_thumbs, args=(self._imagenes,), daemon=True
        ).start()

        n = len(self._imagenes)
        self._lbl_info.configure(
            text=f'{n} imagen{"es" if n > 1 else ""} cargadas'
        )

    def _generar_thumbs(self, rutas: list[str]):
        thumbs = []
        for ruta in rutas:
            try:
                img = Image.open(ruta)
                img.thumbnail((44, 44), Image.Resampling.LANCZOS)
                thumb = ctk.CTkImage(light_image=img, dark_image=img, size=(44, 44))
            except Exception:
                thumb = None
            thumbs.append(thumb)
        self.after(0, lambda: self._aplicar_thumbs(thumbs))

    def _aplicar_thumbs(self, thumbs: list):
        self._thumbs = [t for t in thumbs if t]
        for i, thumb in enumerate(thumbs):
            if thumb and i < len(self._filas_lista):
                self._filas_lista[i].configure(image=thumb)

    def _cambiar_tab(self, tab: str):
        for nombre, frame in self._frames.items():
            if nombre == tab:
                frame.grid()
                frame.tkraise()
            else:
                frame.grid_remove()

    def _ejecutar_resize(self):
        if not self._imagenes:
            self._lbl_info.configure(text='Primero cargá imágenes.')
            return
        carpeta = filedialog.askdirectory(title='Elegí carpeta de salida')
        if not carpeta:
            return

        modo = self._modo_resize.get()
        self._btn_resize.configure(state='disabled', text='Procesando...')

        def _proc():
            errores = 0
            for ruta in self._imagenes:
                try:
                    p = Path(ruta)
                    salida = str(Path(carpeta) / (p.stem + '_redim' + p.suffix))
                    if modo == 'Porcentaje':
                        redimensionar(ruta, salida, porcentaje=self._pct_var.get())
                    elif modo == 'Píxeles':
                        ancho = int(self._entry_ancho.get() or 0) or None
                        alto  = int(self._entry_alto.get() or 0) or None
                        redimensionar(ruta, salida, ancho=ancho, alto=alto,
                                      mantener_ratio=self._mantener_ratio.get())
                    elif modo == 'Preset':
                        redimensionar(ruta, salida, preset_key=self._preset_var.get())
                except Exception:
                    errores += 1
            ok = len(self._imagenes) - errores
            self.after(0, lambda: self._finalizar(
                self._btn_resize, 'Redimensionar', ok, errores
            ))

        threading.Thread(target=_proc, daemon=True).start()

    def _ejecutar_crop(self):
        if not self._imagenes:
            self._lbl_info.configure(text='Primero cargá imágenes.')
            return
        carpeta = filedialog.askdirectory(title='Elegí carpeta de salida')
        if not carpeta:
            return

        self._btn_crop.configure(state='disabled', text='Procesando...')
        ratio = self._ratio_var.get()

        def _proc():
            errores = 0
            for ruta in self._imagenes:
                try:
                    p = Path(ruta)
                    salida = str(Path(carpeta) / (p.stem + '_crop' + p.suffix))
                    recortar(ruta, salida, ratio=ratio)
                except Exception:
                    errores += 1
            ok = len(self._imagenes) - errores
            self.after(0, lambda: self._finalizar(
                self._btn_crop, 'Recortar', ok, errores
            ))

        threading.Thread(target=_proc, daemon=True).start()

    def _ejecutar_canvas(self):
        if not self._imagenes:
            self._lbl_info.configure(text='Primero cargá imágenes.')
            return
        try:
            ancho = int(self._canvas_ancho.get())
            alto  = int(self._canvas_alto.get())
        except ValueError:
            self._lbl_info.configure(text='Ingresá ancho y alto válidos.')
            return
        carpeta = filedialog.askdirectory(title='Elegí carpeta de salida')
        if not carpeta:
            return

        fondo_elegido = self._color_fondo.get()
        self._btn_canvas.configure(state='disabled', text='Procesando...')

        def _proc():
            errores = 0
            for ruta in self._imagenes:
                try:
                    p = Path(ruta)
                    ext = p.suffix.lower()
                    soporta_transparencia = ext in ('.png', '.webp', '.gif', '.tiff')

                    # Determinar color de fondo real
                    if fondo_elegido == 'Transparente' and soporta_transparencia:
                        color = None  # señal para usar fondo transparente real
                    elif fondo_elegido == 'Negro' or (
                        fondo_elegido == 'Transparente' and not soporta_transparencia
                    ):
                        color = (0, 0, 0)
                    else:
                        color = (255, 255, 255)

                    salida = str(Path(carpeta) / (p.stem + '_canvas' + p.suffix))
                    agregar_canvas(ruta, salida, ancho, alto, color_fondo=color) # type: ignore
                except Exception:
                    errores += 1

            ok = len(self._imagenes) - errores
            self.after(0, lambda: self._finalizar(
                self._btn_canvas, 'Aplicar canvas', ok, errores
            ))

        threading.Thread(target=_proc, daemon=True).start()

    def _finalizar(self, btn: ctk.CTkButton, texto: str, ok: int, errores: int):
        btn.configure(state='normal', text=texto)
        msg = f'{ok} imagen{"es" if ok != 1 else ""} procesadas'
        if errores:
            msg += f'  ·  {errores} con error'
        self._lbl_info.configure(text=msg)

    def _limpiar(self):
        self._imagenes = []
        self._thumbs.clear()
        self._filas_lista.clear()
        for w in self._lista.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self._lista,
            text='Sin imágenes cargadas',
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY
        ).pack(pady=12)
        self._lbl_info.configure(text='')

    def _actualizar_fondo_opciones(self, valor: str):
        """Muestra aviso si se elige Transparente con imágenes que no lo soportan."""
        if valor == 'Transparente' and self._imagenes:
            no_soportan = [
                Path(r).suffix.lower()
                for r in self._imagenes
                if Path(r).suffix.lower() not in ('.png', '.webp', '.gif', '.tiff')
            ]
            if no_soportan:
                self._lbl_aviso_fondo.configure(
                    text='Advertencia: JPG/BMP no soportan transparencia — se usará negro.'
                )
                return
        self._lbl_aviso_fondo.configure(text='')