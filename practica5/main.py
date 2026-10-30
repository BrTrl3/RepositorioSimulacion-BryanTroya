"""Punto de entrada de la practica 5."""

from __future__ import annotations

import argparse
from pathlib import Path

from controller import lcg_controller
from view import consola, graficas, reportes

BASE_DIR = Path(__file__).resolve().parent


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generador congruencial lineal con analisis y comparacion Python/Java."
    )
    parser.add_argument(
        "--semilla",
        type=int,
        default=lcg_controller.SEMILLA_POR_DEFECTO,
        help="semilla principal (por defecto: 12345)",
    )
    parser.add_argument(
        "--semilla-alternativa",
        type=int,
        default=lcg_controller.SEMILLA_ALTERNATIVA_POR_DEFECTO,
        help="semilla para la comparacion (por defecto: 54321)",
    )
    parser.add_argument(
        "--cantidad",
        type=int,
        default=lcg_controller.CANTIDAD_POR_DEFECTO,
        help="cantidad de valores a generar (por defecto: 10000)",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=BASE_DIR / "resultados",
        help="directorio de salida (por defecto: practica5/resultados)",
    )
    parser.add_argument(
        "--sin-java",
        action="store_true",
        help="no intentar compilar ni ejecutar la version Java",
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
        datos = lcg_controller.ejecutar_practica(
            semilla=argumentos.semilla,
            cantidad=argumentos.cantidad,
            semilla_alternativa=argumentos.semilla_alternativa,
            intentar_java=not argumentos.sin_java,
            directorio_salida=argumentos.salida,
        )
    except (TypeError, ValueError) as error:
        print(f"Error en los parametros: {error}")
        return 2

    consola.mostrar_encabezado(datos["config"])
    consola.mostrar_primeros_20(datos["principal"])
    consola.mostrar_estadisticas(datos["estadisticas"])
    consola.mostrar_periodo(datos["periodo"])
    consola.mostrar_comparacion_semillas(
        datos["principal"],
        datos["alternativa"],
        datos["comparacion_semillas"],
    )
    if datos["comparacion_java"] is not None:
        consola.mostrar_comparacion_java(datos["comparacion_java"])

    rutas = reportes.exportar_todo(
        principal=datos["principal"],
        alternativa=datos["alternativa"],
        estadisticas=datos["estadisticas"],
        periodo=datos["periodo"],
        comparacion_semillas=datos["comparacion_semillas"],
        comparacion_java=datos["comparacion_java"],
        directorio=datos["directorio_salida"],
    )
    if not argumentos.sin_graficas:
        rutas.update(
            graficas.generar_graficas(
                datos["principal"],
                datos["alternativa"],
                datos["directorio_salida"],
            )
        )

    consola.mostrar_resumen(rutas)
    consola.mostrar_conclusiones()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
