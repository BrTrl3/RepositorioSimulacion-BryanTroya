"""Punto de entrada.

Uso (desde la carpeta practica7):
    python -m python.main                  # solo Python (usa CSV de Java si existe)
    python -m python.main --java           # compila y ejecuta también Java
    python -m python.main --semilla 2026 --repeticiones 3 --java
"""

import argparse
import sys

from python.controlador.controlador import ejecutar


def main():
    # Evita errores con caracteres como π en consolas de Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Estimación de π con Monte Carlo")
    parser.add_argument("--semilla", type=int, default=12345, help="semilla del LCG (default 12345)")
    parser.add_argument("--repeticiones", type=int, default=5,
                        help="repeticiones para promediar tiempos (default 5)")
    parser.add_argument("--java", action="store_true", help="compilar y ejecutar también la versión Java")
    args = parser.parse_args()
    ejecutar(args.semilla, args.repeticiones, args.java)


if __name__ == "__main__":
    main()
