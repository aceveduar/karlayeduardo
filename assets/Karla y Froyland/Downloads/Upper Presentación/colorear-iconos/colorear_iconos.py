"""
Colorear Íconos - Cambia el color de íconos PNG o SVG a cualquier hexadecimal.

Uso:
    python colorear_iconos.py icono.png "#46C2CE"
    python colorear_iconos.py icono.svg "#FF5733"
    python colorear_iconos.py carpeta_iconos/ "#46C2CE"

Requisitos:
    pip install Pillow
"""

import sys
import os
import re
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Instala las dependencias con:")
    print("  pip install Pillow numpy")
    sys.exit(1)


def hex_a_rgb(hex_color: str) -> tuple:
    """Convierte un color hexadecimal a tupla RGB."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Color inválido: #{hex_color}. Usa formato #RRGGBB")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def colorear_png(ruta_entrada: str, color_hex: str, ruta_salida: str):
    """
    Recolorea un ícono PNG al color indicado.
    
    Funciona con:
    - Íconos con transparencia (RGBA): colorea los píxeles visibles.
    - Íconos sin transparencia (RGB): convierte píxeles oscuros al color
      y los claros a transparente.
    """
    r, g, b = hex_a_rgb(color_hex)
    img = Image.open(ruta_entrada)
    original_mode = img.mode

    if original_mode in ("RGBA", "LA", "PA"):
        # Tiene canal alfa → colorear todo lo visible
        img = img.convert("RGBA")
        data = np.array(img)
        alfa = data[:, :, 3]

        nuevo = np.zeros_like(data)
        nuevo[:, :, 0] = r
        nuevo[:, :, 1] = g
        nuevo[:, :, 2] = b
        nuevo[:, :, 3] = alfa

    else:
        # Sin alfa → usar luminancia para crear transparencia
        img = img.convert("RGBA")
        data = np.array(img)

        luminancia = (
            0.299 * data[:, :, 0]
            + 0.587 * data[:, :, 1]
            + 0.114 * data[:, :, 2]
        )

        nuevo = np.zeros_like(data)
        nuevo[:, :, 0] = r
        nuevo[:, :, 1] = g
        nuevo[:, :, 2] = b
        # Oscuro = opaco, claro = transparente
        nuevo[:, :, 3] = (255 - luminancia).clip(0, 255).astype(np.uint8)

    resultado = Image.fromarray(nuevo, "RGBA")
    resultado.save(ruta_salida)
    print(f"  OK {ruta_salida}")


def colorear_svg(ruta_entrada: str, color_hex: str, ruta_salida: str):
    """
    Recolorea un SVG reemplazando todos los atributos fill y stroke
    por el color indicado.
    """
    color = color_hex if color_hex.startswith("#") else f"#{color_hex}"
    contenido = Path(ruta_entrada).read_text(encoding="utf-8")

    # Reemplazar fill="..." y stroke="..." (excepto "none" y "transparent")
    contenido = re.sub(
        r'(fill\s*=\s*["\'])(?!none|transparent)([^"\']+)(["\'])',
        rf"\g<1>{color}\g<3>",
        contenido,
    )
    contenido = re.sub(
        r'(stroke\s*=\s*["\'])(?!none|transparent)([^"\']+)(["\'])',
        rf"\g<1>{color}\g<3>",
        contenido,
    )

    # También en estilos inline: fill:...; y stroke:...;
    contenido = re.sub(
        r'(fill\s*:\s*)(?!none|transparent)([^;"\']+)',
        rf"\g<1>{color}",
        contenido,
    )
    contenido = re.sub(
        r'(stroke\s*:\s*)(?!none|transparent)([^;"\']+)',
        rf"\g<1>{color}",
        contenido,
    )

    Path(ruta_salida).write_text(contenido, encoding="utf-8")
    print(f"  OK {ruta_salida}")


def generar_nombre_salida(ruta: str, color_hex: str) -> str:
    """Genera el nombre del archivo de salida."""
    p = Path(ruta)
    color_limpio = color_hex.lstrip("#")
    return str(p.parent / f"{p.stem}_{color_limpio}{p.suffix}")


def procesar(ruta: str, color_hex: str):
    """Procesa un archivo o una carpeta entera."""
    ruta_path = Path(ruta)
    extensiones_validas = {".png", ".svg", ".jpg", ".jpeg", ".bmp", ".webp"}

    if ruta_path.is_dir():
        archivos = [
            f for f in ruta_path.iterdir()
            if f.suffix.lower() in extensiones_validas
        ]
        if not archivos:
            print(f"No se encontraron íconos en: {ruta}")
            return
        print(f"Procesando {len(archivos)} archivo(s) en {ruta}...\n")
    else:
        if ruta_path.suffix.lower() not in extensiones_validas:
            print(f"Formato no soportado: {ruta_path.suffix}")
            return
        archivos = [ruta_path]
        print(f"Procesando 1 archivo...\n")

    for archivo in sorted(archivos):
        salida = generar_nombre_salida(str(archivo), color_hex)
        ext = archivo.suffix.lower()

        try:
            if ext == ".svg":
                colorear_svg(str(archivo), color_hex, salida)
            else:
                colorear_png(str(archivo), color_hex, salida)
        except Exception as e:
            print(f"  ERROR con {archivo.name}: {e}")

    print(f"\n¡Listo! Color aplicado: {color_hex}")


def main():
    carpeta_script = str(Path(__file__).parent)
    color_defecto = "#f59e0b"

    if len(sys.argv) == 1:
        ruta = carpeta_script
        color = color_defecto
    elif len(sys.argv) == 2:
        ruta = carpeta_script
        color = sys.argv[1]
    else:
        ruta = sys.argv[1]
        color = sys.argv[2]

    if not os.path.exists(ruta):
        print(f"No existe: {ruta}")
        sys.exit(1)

    try:
        hex_a_rgb(color)
    except ValueError as e:
        print(e)
        sys.exit(1)

    procesar(ruta, color)


if __name__ == "__main__":
    main()
