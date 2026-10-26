"""Práctica 2 - Simulación
Autor: Bryan Troya
"""

import sys
from pathlib import Path


def main():
    ruta_python = Path(__file__).parent / "python"
    sys.path.insert(0, str(ruta_python))
    from main import main as ejecutar_practica
    ejecutar_practica()


if __name__ == "__main__":
    main()
