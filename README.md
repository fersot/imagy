<img width="1761" height="497" alt="banner" src="https://github.com/user-attachments/assets/0503ce8a-794b-42fc-bec9-6de98962590d" />

# Yagua - Editor de Imágenes

Aplicación de escritorio para edición y procesamiento de imágenes por lotes.

---

## Tabla de Contenidos

1. [Características](#características)
2. [Tech Stack](#tech-stack)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Arquitectura](#arquitectura)
5. [Módulos Implementados](#módulos-implementados)
6. [Sistema de Traducciones](#sistema-de-traducciones)
7. [Ejecución](#ejecución)
8. [Contribución](#contribución)

---

## Características

- **Compresión de imágenes**: Reduce el tamaño de imágenes manteniendo la calidad
- **Conversión de formatos**: Convierte entre JPEG, PNG, WEBP, AVIF, ICO, BMP, TIFF, GIF
- **Extracción de paleta de colores**: Extrae colores dominantes de una imagen
- **Gestión de metadatos EXIF**: Lee, edita, limpia y exporta metadatos
- **Redimensionar**: Redimensiona por porcentaje, píxeles o presets (Instagram, Facebook, YouTube, etc.)
- **Recortar**: Recorte centrado con dimensiones personalizadas
- **Canvas**: Ajusta el tamaño del canvas manteniendo la imagen centrada
- **Renombrar lote**: Renombra múltiples archivos con patrones personalizables
- **Marca de agua**: Agrega texto o imagen como marca de agua
- **Quitar fondo**: Elimina el fondo de imágenes usando IA (rembg)
- **LQIP**: Genera Low Quality Image Placeholders y Base64
- **Optimizer**: Optimización inteligente automática
- **Multiidioma**: Español, English, Português
- **Inicio maximizado**: La app se inicia maximizada por defecto

---

## Tech Stack

| Tecnología        | Versión | Propósito                            |
| ----------------- | ------- | ------------------------------------ |
| **Python**        | 3.13+   | Lenguaje principal                   |
| **CustomTkinter** | 5.2.2   | Framework de UI moderno              |
| **Pillow**        | 12.1.1  | Procesamiento de imágenes            |
| **piexif**       | 1.1.3   | Manipulación de metadatos EXIF       |
| **tkinterdnd2**   | 0.4.3   | Drag & Drop                          |
| **darkdetect**    | 0.8.0   | Detección de tema oscuro del sistema |
| **rembg**         | 2.0.57  | Remoción de fondo con IA            |

### Requisitos del Sistema

- Windows 10/11 (macOS y Linux parcialmente soportados)
- Python 3.13 o superior
- Al menos 4GB de RAM recomendada

---

## Estructura del Proyecto

```
Yagua/
├── main.py                 # Punto de entrada de la aplicación
├── app.py                 # Clase principal YaguaApp
├── user_settings.json     # Configuración del usuario (idioma, etc.)
├── core/                  # Lógica de negocio (re-exports)
├── modules/               # Módulos de procesamiento de imagen
│   ├── compress.py        # Compresión de imágenes
│   ├── convert.py        # Conversión de formatos
│   ├── palette.py        # Extracción de paleta de colores
│   ├── metadata.py       # Gestión de metadatos EXIF
│   └── resize.py         # Redimensionado, recorte y canvas
├── ui/                   # Interfaz de usuario
│   ├── main_window.py   # Ventana principal
│   ├── sidebar.py       # Barra lateral de navegación
│   ├── colors.py        # Paleta de colores del tema
│   ├── fonts.py         # Configuración de fuentes
│   ├── frames/          # Frames de cada módulo
│   │   ├── base.py                    # Clase base para frames
│   │   ├── compress_frame.py          # Módulo comprimir
│   │   ├── convert_frame.py           # Módulo convertir
│   │   ├── palette_frame.py           # Módulo paleta
│   │   ├── metadata_frame.py          # Módulo metadatos
│   │   ├── resize_frame.py            # Módulo redimensionar
│   │   ├── rename_frame.py            # Módulo renombrar
│   │   ├── watermark_frame.py        # Módulo marca de agua
│   │   ├── remove_bg_frame.py        # Módulo quitar fondo
│   │   ├── lqip_frame.py              # Módulo LQIP
│   │   ├── optimizer_frame.py        # Módulo optimizador
│   │   └── settings_frame.py         # Módulo ajustes
│   └── widgets/         # Componentes UI reutilizables
├── translations/         # Sistema de traducciones
│   ├── __init__.py      # Funciones t(), set_language(), get_language()
│   ├── es.py            # Traducciones español
│   ├── en.py            # Traducciones inglés
│   └── pt.py            # Traducciones portugués
├── utils/               # Funciones helper
│   └── __init__.py      # tintar_icono()
└── assets/              # Recursos estáticos
    ├── icon.ico        # Icono de la aplicación (Windows)
    ├── icon.png        # Icono de la aplicación
    ├── fonts/
    │   └── Inter.ttf   # Fuente personalizada
    └── icons/          # Íconos de la interfaz
```

---

## Arquitectura

### Patrón de Arquitectura

El proyecto sigue una arquitectura **MVC simplificada** con separación clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                   │
│  (ui/)                                                  │
│  - frames/          → Vistas (CTkFrame)                 │
│  - main_window.py  → Controlador principal             │
│  - sidebar.py      → Navegación                        │
│  - translations/   → Sistema de traducciones           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                │
│  (modules/)                                             │
│  - compress.py     → Lógica de compresión              │
│  - convert.py      → Lógica de conversión              │
│  - palette.py      → Extracción de colores            │
│  - metadata.py     → Gestión EXIF                     │
│  - resize.py       → Redimensionado y recorte          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                       UTILITIES                         │
│  (utils/)                                              │
│  - tintar_icono()  → Helper para íconos                │
└─────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Usuario** interactúa con la UI (frames)
2. **Frame** invoca método del módulo correspondiente en `modules/`
3. **Módulo** procesa la imagen usando Pillow
4. **Resultado** retorna al frame y se actualiza la UI

### Clases Principales

| Clase           | Ubicación                     | Responsabilidad                   |
| --------------- | ----------------------------- | --------------------------------- |
| `YaguaApp`      | `app.py`                      | Ventana principal, inicialización |
| `MainWindow`    | `ui/main_window.py`           | Contenedor con sidebar y frames   |
| `Sidebar`       | `ui/sidebar.py`               | Navegación entre módulos          |
| `BaseFrame`     | `ui/frames/base.py`           | Clase base con métodos comunes    |
| `SettingsFrame` | `ui/frames/settings_frame.py`| Configuración (idioma, tema)      |

---

## Módulos Implementados

### 1. Compresión (`compress.py`)

**Funcionalidades:**

- Compresión de imágenes con calidad configurable (10-100)
- Eliminación opcional de metadatos EXIF
- Estimación de tamaño antes de comprimir
- Preservación del formato original o conversión automática
- Soporte para JPEG, PNG, WEBP, AVIF, ICO, BMP, TIFF, GIF
- Vista previa de imágenes cargadas

**Funciones públicas:**

```python
comprimir_imagen(ruta_entrada, ruta_salida, calidad=85, quitar_exif=True) -> dict
estimar_tamano(ruta_entrada, calidad) -> int
formatear_bytes(bytes_val) -> str
```

### 2. Conversión (`convert.py`)

**Funcionalidades:**

- Conversión entre múltiples formatos
- Calidad configurable por formato
- Corrección automática de modos de color (RGBA → RGB para JPEG)
- Soporte para conversión por lotes
- Vista previa de imágenes cargadas

**Formatos soportados:** JPEG, PNG, WEBP, AVIF, ICO, BMP, TIFF, GIF

**Funciones públicas:**

```python
convertir_imagen(ruta_entrada, fmt_destino, carpeta_salida, calidad=90) -> dict
batch_convertir(rutas, fmt_destino, carpeta_salida, calidad=90, progress_cb=None) -> list
```

### 3. Paleta de Colores (`palette.py`)

**Funcionalidades:**

- Extracción de N colores dominantes (4-12)
- Conversión de colores a múltiples formatos (HEX, RGB, HSL, CSS)
- Exportación de paleta como imagen PNG
- Detección de luminosidad para texto legible
- Copiar color al portapapeles en diferentes formatos

**Funciones públicas:**

```python
extraer_paleta(ruta, n_colores=6) -> list[tuple[int, int, int]]
rgb_a_hex(rgb) -> str
rgb_a_hsl(rgb) -> tuple[int, int, int]
es_color_claro(rgb) -> bool
formatos_color(rgb) -> dict[str, str]
exportar_paleta_imagen(paleta, ruta_salida, ...) -> str
```

### 4. Metadatos EXIF (`metadata.py`)

**Funcionalidades:**

- Lectura de metadatos EXIF
- Edición de campos (Autor, Copyright, Software, Fecha)
- Limpieza de metadatos por lotes
- Exportación a TXT y JSON
- Coordenadas GPS con enlace a Google Maps
- Soporte para JPEG y TIFF

**Funciones públicas:**

```python
leer_metadatos(ruta) -> dict[str, str]
limpiar_exif(ruta_entrada, ruta_salida) -> dict
editar_exif(ruta_entrada, ruta_salida, campos) -> bool
exportar_txt(metadatos, ruta)
exportar_json(metadatos, ruta)
```

### 5. Redimensionar (`resize.py`)

**Funcionalidades:**

- **Redimensionar**: Por porcentaje o píxeles, manteniendo relación de aspecto
- **Recortar**: Recorte centrado con dimensiones personalizadas
- **Canvas**: Ajusta el tamaño del canvas con color de fondo (blanco, negro, transparente)
- **Presets**: Instagram, Facebook, Twitter/X, YouTube, LinkedIn, TikTok, Pinterest, Web, resoluciones estándar e íconos

**Presets disponibles:**

- Instagram: Post cuadrado 1:1, Post portrait 4:5, Story/Reels 9:16
- Facebook: Post 1200×630, Cover 851×315
- Twitter/X: Post 16:9, Header 3:1
- YouTube: Thumbnail 16:9, Channel art 16:9
- LinkedIn: Post 1.91:1, Cover personal 4:1
- TikTok/WhatsApp: Status/Video 9:16
- Pinterest: Pin estándar 2:3
- Web: OG image 1.91:1
- Resoluciones: HD 720p, Full HD 1080p, 2K, 4K UHD
- Íconos: Favicon 32×32, Ícono 256, Ícono 512

### 6. Renombrar Lote (`rename_frame.py`)

**Funcionalidades:**

- Renombrado por prefijo, sufijo o reemplazo de texto
- Numeración secuencial
- Fecha de modificación como parte del nombre
- Preview de los nuevos nombres antes de aplicar

### 7. Marca de Agua (`watermark_frame.py`)

**Funcionalidades:**

- Texto como marca de agua
- Imagen como marca de agua
- Posicionamiento (esquinas, centro, mosaico)
- Opacidad configurable
- Tamaño y ángulo ajustables

### 8. Quitar Fondo (`remove_bg_frame.py`)

**Funcionalidades:**

- Eliminación de fondo usando IA (rembg)
- Soporte para personas, productos, dibujos, etc.
- Exportación en PNG con transparencia

### 9. LQIP (`lqip_frame.py`)

**Funcionalidades:**

- Genera Low Quality Image Placeholders
- Exporta en Base64
- Vista previa de las miniaturas

### 10. Optimizer (`optimizer_frame.py`)

**Funcionalidades:**

- Optimización inteligente automática
- Compresión automática con detección de mejor calidad
- Procesamiento por lotes

### 11. Settings (`settings_frame.py`)

**Funcionalidades:**

- Cambio de idioma (Español, English, Português)
- Reinicio automático de la app al cambiar idioma

---

## Sistema de Traducciones

La aplicación cuenta con un sistema completo de traducciones multiidioma.

### Idiomas disponibles

- **Español** (`es.py`)
- **English** (`en.py`)  
- **Português** (`pt.py`)

### Uso

```python
from translations import t, set_language, get_language, AVAILABLE_LANGUAGES

# Obtener traducción
texto = t('compress_title')  # returns 'Comprimir' / 'Compress' / 'Comprimir'

# Cambiar idioma
set_language('Español')

# Obtener idioma actual
idioma = get_language()  # returns 'Español', 'English' or 'Português'

# Idiomas disponibles
print(AVAILABLE_LANGUAGES)  # {'Español': 'Español', 'English': 'English', 'Português': 'Português'}
```

### keys de traducción

El sistema usa un archivo JSON para guardar la configuración del usuario (`user_settings.json`).

### Ventana título

El título de la ventana también es traducible (`app_title`):
- Español: "Yagua - Editor de Imágenes"
- English: "Yagua - Image Editor"
- Português: "Yagua - Editor de Imagens"

---

## Ejecución

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install customtkinter==5.2.2 pillow==12.1.1 piexif==1.1.3 tkinterdnd2==0.4.3 rembg==2.0.57
```

### Ejecutar la aplicación

```bash
python main.py
```

### Estructura de temas

La aplicación usa tema oscuro por defecto. Los colores están definidos en `ui/colors.py`:

```python
FRAMES_BG = '#0A0A0B'      # Fondo principal
SIDEBAR_BG = '#121214'      # Fondo del sidebar
PANEL_BG = '#1C1C1E'        # Fondo de paneles
TEXT_COLOR = '#F2F2F7'     # Color de texto principal
ACENTO = '#FFFFFF'          # Color de acento
```

### Inicio maximizado

La aplicación se inicia maximizada automáticamente usando `self.state('zoomed')` en Windows.

---

## Contribución

### Convenciones de código

- **PEP 8** para estilo de código
- **type hints** para funciones públicas
- **docstrings** en inglés para funciones, español para UI
- Nombres descriptivos en español para variables de UI

### Nomenclatura de archivos

- `snake_case.py` para módulos
- `PascalCase.py` para clases
- `camelCase` evitado en Python

### Agregar un nuevo módulo

1. Crear la lógica en `modules/nombre.py` (opcional)
2. Crear el frame en `ui/frames/nombre_frame.py`
3. Registrar en `ui/main_window.py` → `MODULOS`
4. Agregar ícono en `assets/icons/`
5. Agregar traducciones en `translations/es.py`, `en.py`, `pt.py`
6. Agregar entrada de menú en `ui/sidebar.py` → `MENU_ITEMS`

### Testing

Para probar un módulo específico:

```bash
python -c "from modules.compress import comprimir_imagen; print(comprimir_imagen('input.jpg', 'output.jpg'))"
```

---

## Licencia

MIT License - Ver archivo LICENSE para más detalles.
