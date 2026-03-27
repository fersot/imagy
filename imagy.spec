# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para Imagy.
Incluye todos los assets, fuentes, iconos y dependencias necesarias.
"""

import sys
import site
from pathlib import Path

block_cipher = None

# Detectar automáticamente dónde está customtkinter instalado
def find_customtkinter():
    """Busca el directorio de customtkinter en todos los site-packages."""
    for sp in site.getsitepackages() + [site.getusersitepackages()]:
        ctk = Path(sp) / 'customtkinter'
        if ctk.exists():
            return str(ctk)
    # Fallback por si es un venv local
    venv_path = Path('venv/Lib/site-packages/customtkinter')
    if venv_path.exists():
        return str(venv_path)
    raise FileNotFoundError('customtkinter no encontrado en site-packages')

# --------------------------------------------------------------------------- #
# Datos adicionales (assets, traducciones, customtkinter data)                #
# --------------------------------------------------------------------------- #
added_files = [
    # Assets de la app
    ('assets/icon.ico',         'assets'),
    ('assets/icon.png',         'assets'),
    ('assets/fonts/Inter.ttf',  'assets/fonts'),
    ('assets/icons',            'assets/icons'),

    # Customtkinter — buscado dinámicamente
    (find_customtkinter(),      'customtkinter'),

    # Traducciones
    ('app/translations/en.py',  'app/translations'),
    ('app/translations/es.py',  'app/translations'),
    ('app/translations/pt.py',  'app/translations'),
]

# --------------------------------------------------------------------------- #
# Imports ocultos (módulos cargados dinámicamente que PyInstaller no detecta) #
# --------------------------------------------------------------------------- #
hidden_imports = [
    'customtkinter',
    'tkinter',
    'tkinter.ttk',
    'tkinterdnd2',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageFilter',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'piexif',
    'piexif.helper',
    'rembg',
    'rembg.sessions',
    'rembg.sessions.base',
    'rembg.sessions.u2net',
    'rembg.sessions.u2netp',
    'onnxruntime',
    'onnxruntime.capi',
    'numba',
    'numba.core',
    'scipy',
    'scipy.ndimage',
    'skimage',
    'skimage.color',
    'skimage.transform',
    'imageio',
    'pooch',
    'tqdm',
    'app.modules.compress',
    'app.modules.convert',
    'app.modules.resize',
    'app.modules.rename',
    'app.modules.metadata',
    'app.modules.remove_bg',
    'app.modules.palette',
    'app.modules.lqip',
    'app.translations.en',
    'app.translations.es',
    'app.translations.pt',
]

# --------------------------------------------------------------------------- #
# Análisis                                                                     #
# --------------------------------------------------------------------------- #
a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=['hooks/hook_runtime.py'],
    excludes=[
        'matplotlib',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'coverage',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --------------------------------------------------------------------------- #
# Ejecutable                                                                   #
# --------------------------------------------------------------------------- #
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Imagy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,                     # Sin consola (modo GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',            # Ícono Windows / Linux
)

# --------------------------------------------------------------------------- #
# Colección (one-folder mode para mejor compatibilidad con assets dinámicos)  #
# --------------------------------------------------------------------------- #
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Imagy',
)

# --------------------------------------------------------------------------- #
# macOS: bundle .app                                                           #
# --------------------------------------------------------------------------- #
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='Imagy.app',
        icon='assets/icon.png',
        bundle_identifier='com.fersot.imagy',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDisplayName': 'Imagy',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': True,
        },
    )
