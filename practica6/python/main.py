"""Punto de entrada de la practica 6."""

from __future__ import annotations

import argparse
from pathlib import Path

from controller import practica_controller
from model.lcg import CANTIDAD_POR_DEFECTO
from model.pruebas import INTERVALOS_POR_DEFECTO
from view import consola, graficas, reportes

BASE_DIR = Path(__file__).resolve().parent.parent


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validacion de un LCG con Chi-cuadrado y Kolmogorov-Smirnov."
    )
    parser.add_argument(
        "--cantidad",
        type=int,
        default=CANTIDAD_POR_DEFECTO,
        help="cantidad de valores por configuracion (por defecto: 10000)",
    )
    parser.add_argument(
        "--intervalos",
        type=int,
        default=INTERVALOS_POR_DEFECTO,
        help="intervalos de la prueba Chi-cuadrado (por defecto: 10)",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=BASE_DIR / "resultados",
        help="directorio de salida (por defecto: practica6/resultados)",
    )
    parser.add_argument(
        "--sin-java",
        action="store_true",
        help="no compilar ni ejecutar la version Java",
    )
    parser.add_argument(
        "--sin-graficas",
        action="store_true",
        help="no generar las graficas PNG",
    )
    return parser


def main() -> int:
    argumentos = crear_parser().parse_args()
    try:
        datos = practica_controller.ejecutar_practica(
            cantidad=argumentos.cantidad,
            intervalos=argumentos.intervalos,
            intentar_java=not argumentos.sin_java,
            directorio_salida=argumentos.salida,
        )
    except ValueError as error:
        print(f"Error en los parametros: {error}")
        return 2

    principal = datos["evaluaciones"][0]
    consola.mostrar_encabezado(datos)
    consola.mostrar_secuencia(principal["resultado"])
    consola.mostrar_chi_cuadrado(principal)
    consola.mostrar_kolmogorov_smirnov(principal)
    consola.mostrar_configuraciones(datos["evaluaciones"])
    consola.mostrar_comparacion_java(datos["java"])
    consola.mostrar_pi(datos["pi"])

    rutas = reportes.exportar_todo(datos)
    if not argumentos.sin_graficas:
        rutas.update(graficas.generar_graficas(datos))
    consola.mostrar_archivos(rutas)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
