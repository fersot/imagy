"""
Modulo de eliminacion de fondo de imagenes.
Usa el modelo U2Net via rembg para segmentacion inteligente.

Relacionado con:
    - app/ui/frames/remove_bg/: UI relacionada.
"""

from pathlib import Path
from PIL import Image, ImageOps


def quitar_fondo(ruta_entrada, ruta_salida, color_fondo=None):
    try:
        from rembg import remove as rembg_remove
    except ImportError:
        raise ImportError('rembg no está instalado. Ejecutá: pip install rembg')

    imagen = Image.open(ruta_entrada)
    imagen = ImageOps.exif_transpose(imagen)
    tam_original = Path(ruta_entrada).stat().st_size

    # Cast explícito — rembg retorna Image pero Pylance no lo infiere
    resultado: Image.Image = Image.fromarray(
        __import__('numpy').array(rembg_remove(imagen))
    )

    if color_fondo is not None:
        fondo = Image.new('RGBA', resultado.size, (*color_fondo, 255))
        fondo.paste(resultado, mask=resultado.split()[3])
        resultado = fondo.convert('RGB')
        extension = '.jpg'
        formato = 'JPEG'
    else:
        extension = '.png'
        formato = 'PNG'

    ruta_archivo = Path(ruta_entrada)
    ruta_final = Path(ruta_salida) / (ruta_archivo.stem + '_sinFondo' + extension)

    resultado.save(str(ruta_final), formato)
    tam_resultado = ruta_final.stat().st_size

    return {
        'ruta_salida': str(ruta_final),
        'tam_original': tam_original,
        'tam_resultado': tam_resultado,
    }

def batch_quitar_fondo(rutas, carpeta_salida, color_fondo=None):
    """
    Elimina el fondo de multiples imagenes.

    Args:
        rutas: Lista de rutas de imagenes.
        carpeta_salida: Carpeta donde guardar los resultados.
        color_fondo: Tupla (R,G,B) o None para transparente.

    Returns:
        Diccionario con ok, errores, resultados.
    """
    resultados = []
    errores = 0

    for ruta in rutas:
        try:
            res = quitar_fondo(ruta, carpeta_salida, color_fondo)
            resultados.append(res)
        except Exception:
            errores += 1

    return {
        'ok': len(resultados),
        'errores': errores,
        'resultados': resultados,
    }


def rembg_disponible():
    """
    Verifica si rembg esta instalado y disponible.

    Returns:
        True si rembg esta disponible, False si no.
    """
    try:
        import rembg  # noqa: F401
        return True
    except ImportError:
        return False


def modelo_descargado():
    """
    Verifica si el modelo U2Net ya fue descargado.

    Returns:
        True si el modelo existe en cache, False si no.
    """
    ruta_modelo = Path.home() / '.u2net' / 'u2net.onnx'
    return ruta_modelo.exists()