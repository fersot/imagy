
# Imagy - Procesador de Imágenes

Aplicación de escritorio para procesar imágenes en lote de forma rápida y elegante. Pensada para flujos de trabajo reales: compresión, conversión, quitar fondo con IA, metadatos EXIF y LQIP/Base64.

<a href="https://buymeacoffee.com/fersot" target="_blank">Buy Me a Coffee</a>

## 📖 Descripción

Imagy surgió como alternativa a las herramientas web de procesamiento de imágenes: limitadas y con planes de pago para tareas que deberían ser simples. Es una app de escritorio gratuita y open source que corre todo localmente.

Está pensada para desarrolladores web, diseñadores, fotógrafos y cualquier usuario que necesite procesar imágenes en lote sin depender de un navegador ni pagar una suscripción.

Imagy integra en una sola interfaz features orientadas al flujo de trabajo web moderno: generación de LQIP y Base64, quitar fondo con IA (rembg, funciona offline una vez descargado el modelo), edición de metadatos EXIF y compresión/conversión en lote sin límite de archivos.

## ✨ Features

- Compresión inteligente con control de calidad
- Conversión entre múltiples formatos de imagen
- Eliminación de fondo con IA (rembg)
- Redimensionado, recorte y edición en canvas
- Extracción automática de paleta de colores
- Renombrado masivo con vista previa
- Gestión de metadatos EXIF (visualizar, editar y limpiar)
- Generación de LQIP y codificación Base64
- Soporte multi-idioma (ES / EN / PT)
- Temas oscuros predefinidos

## ⚙️ Instalación

### 🖥️ Instalación (Windows)
1. Descargar `Imagy_Setup_1.1.0.zip`
2. Descomprimir archivo `.zip`
3. Ejecutar `Imagy_Setup_1.1.0.exe`
4. Seguir instrucciones de instalación
5. Ejecutar programa desde el escritorio

### 🐧 Instalación (Linux)
1. Descargar `Imagy-1.1.0-x86_64.AppImage`
2. Ejecutar en terminal `chmod +x Imagy-1.1.0-x86_64.AppImage`
3. Luego `./Imagy-1.1.0-x86_64.AppImage`

### 🐍 Código fuente

1. Clona el repositorio.
2. Crea y activa tu entorno virtual.
3. Instala dependencias con `pip install -r requirements.txt`.
4. Ejecuta `python main.py`.

## 🧩 Requisitos recomendados

Para que Imagy funcione de manera fluida, especialmente con lotes grandes (hasta 100 imágenes):

#### ✅ Sistema
- Windows 10/11 o Linux x64
- CPU: 4 núcleos o más recomendado
- RAM: 8 GB mínimo
- Disco: 500 MB libres + espacio para outputs
#### ✅ Dependencias (Linux)
- AppImage suele correr directo, pero puede requerir:
  - `libfuse2`
  - `libgl1`
  - `libglib2.0-0`
#### ✅ Límites de carga
- 100 imágenes por lote (compresión, conversión, resize, rename, LQIP)
- 10 imágenes por lote en Quitar Fondo
- 100 imágenes en limpieza de metadatos (EXIF)

## 🚀 Uso

1. Abre la app.
2. Selecciona un módulo en la barra lateral.
3. Carga imágenes y procesa.
4. Guarda los resultados en la carpeta de salida.

ℹ️ Nota: Próximamente compatibilidad para macOS.

## 🔧 Tecnologías Utilizadas

| Tecnología        | Versión | Propósito                          |
| ----------------- | ------- | ---------------------------------- |
| Python            | 3.13+   | Lenguaje principal                 |
| CustomTkinter     | 5.2.2   | UI moderna para escritorio         |
| Pillow            | 12.1.1  | Procesamiento de imágenes          |
| piexif            | 1.1.3   | Metadatos EXIF                     |
| darkdetect        | 0.8.0   | Detección de tema del sistema      |
| rembg             | 2.0.73  | Quitar fondo con IA                |
| Codex             | N/A     | Asistencia de desarrollo           |

## 🤝 Contribución

- Abre un issue para bugs o ideas.
- Envía un PR con cambios claros y pequeños.
- Mantén el estilo del proyecto y la estructura actual.

## ⭐ Apoyá el proyecto

Si Imagy te resultó útil, dejá una estrella en el repo — es gratis y ayuda un montón a que más gente lo encuentre :)

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles.
