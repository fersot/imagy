"""
Frame del módulo de Ajustes / Settings.
Permite cambiar el idioma y otras configuraciones.
"""

import sys
import customtkinter as ctk
from ui import colors, fonts
from translations import t, AVAILABLE_LANGUAGES, set_language, get_language


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=colors.FRAMES_BG)
        self._parent = parent
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)

        # Título
        fila_titulo = ctk.CTkFrame(self, fg_color='transparent')
        fila_titulo.grid(row=0, column=0, padx=28, pady=(26, 8), sticky='ew')
        fila_titulo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            fila_titulo,
            text=t('settings_title'),
            font=fonts.FUENTE_TITULO,
            text_color=colors.TEXT_COLOR,
            anchor='w'
        ).grid(row=0, column=0, sticky='w')

        # Panel de idioma
        panel_idioma = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=colors.PANEL_BG,
            border_width=1,
            border_color=colors.SIDEBAR_SEPARATOR
        )
        panel_idioma.grid(row=1, column=0, padx=28, pady=16, sticky='ew')
        panel_idioma.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel_idioma,
            text=t('language'),
            font=fonts.FUENTE_BASE,
            text_color=colors.TEXT_GRAY,
            anchor='w'
        ).grid(row=0, column=0, padx=(16, 12), pady=16, sticky='w')

        # Selector de idioma
        self._lang_var = ctk.StringVar(value=get_language())

        self._selector_idioma = ctk.CTkOptionMenu(
            panel_idioma,
            values=list(AVAILABLE_LANGUAGES.keys()),
            variable=self._lang_var,
            font=fonts.FUENTE_BASE,
            fg_color=colors.SIDEBAR_BG,
            button_color=colors.ACENTO,
            button_hover_color=colors.ACENTO_HOVER,
            text_color=colors.TEXT_COLOR,
            dropdown_fg_color=colors.PANEL_BG,
            dropdown_text_color=colors.TEXT_COLOR,
            dropdown_hover_color=colors.SIDEBAR_HOVER,
            command=self._cambiar_idioma
        )
        self._selector_idioma.grid(row=0, column=1, padx=(0, 16), pady=16, sticky='w')

        # Info
        self._lbl_info = ctk.CTkLabel(
            self, text='',
            font=fonts.FUENTE_CHICA,
            text_color=colors.TEXT_GRAY
        )
        self._lbl_info.grid(row=2, column=0, pady=(0, 4))

    def _cambiar_idioma(self, lang: str):
        """Cambia el idioma y reinicia la app."""
        set_language(lang)
        self._lbl_info.configure(text=t('restart_required'))
        self.after(1500, self._reiniciar_app)

    def _reiniciar_app(self):
        """Reinicia la aplicación."""
        python = sys.executable
        script = sys.argv[0]
        import subprocess
        subprocess.Popen([python, script])
        sys.exit(0)
