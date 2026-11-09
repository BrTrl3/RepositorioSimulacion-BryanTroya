"""Controlador de la practica 6: orquesta generacion, pruebas y comparacion."""

from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

import pandas as pd

from model import comparacion, montecarlo, pruebas
from model.lcg import CANTIDAD_POR_DEFECTO, CONFIGURACIONES, generar_secuencia

BASE_DIR = Path(__file__).resolve().parent.parent.parent
JAVA_DIR = BASE_DIR / "java"
RESULTADOS_DIR = BASE_DIR / "resultados"


class ErrorJava(Exception):
    """Error controlado cuando no es posible ejecutar la implementacion Java."""


def ejecutar_practica(
    cantidad: int = CANTIDAD_POR_DEFECTO,
    intervalos: int = pruebas.INTERVALOS_POR_DEFECTO,
    intentar_java: bool = True,
    directorio_salida: Path | str | None = None,
) -> dict[str, Any]:
    salida = Path(directorio_salida) if directorio_salida is not None else RESULTADOS_DIR
    salida.mkdir(parents=True, exist_ok=True)

    evaluaciones = []
    for configuracion in CONFIGURACIONES:
        resultado = generar_secuencia(configuracion, cantidad)
        evaluaciones.append(
            {
                "resultado": resultado,
                "chi": pruebas.chi_cuadrado(resultado.normalizados, intervalos),
                "ks": pruebas.kolmogorov_smirnov(resultado.normalizados),
            }
        )

    pi_python = []
    for puntos in montecarlo.TAMANOS_PI:
        inicio = time.perf_counter()
        fila = montecarlo.estimar_pi(CONFIGURACIONES[0], puntos)
        fila["tiempo"] = time.perf_counter() - inicio
        pi_python.append(fila)

    datos_java: dict[str, Any] = {"disponible": False, "error": "omitido con --sin-java"}
    if intentar_java:
        try:
            datos_java = _comparar_con_java(evaluaciones, cantidad, intervalos, salida)
        except ErrorJava as error:
            datos_java = {"disponible": False, "error": str(error)}

    return {
        "cantidad": cantidad,
        "intervalos": intervalos,
        "evaluaciones": evaluaciones,
        "pi": _tabla_pi(pi_python, datos_java),
        "java": datos_java,
        "directorio_salida": salida,
    }


def _tabla_pi(
    pi_python: list[dict[str, Any]],
    datos_java: dict[str, Any],
) -> list[dict[str, Any]]:
    pi_java = {fila["n"]: fila for fila in datos_java.get("pi", [])}
    tabla = []
    for fila in pi_python:
        java = pi_java.get(fila["n"])
        tabla.append(
            {
                "n": fila["n"],
                "pi": fila["pi"],
                "error": fila["error"],
                "tiempo_python": fila["tiempo"],
                "pi_java": java["pi"] if java else None,
                "tiempo_java": java["tiempo"] if java else None,
            }
        )
    return tabla


def _comparar_con_java(
    evaluaciones: list[dict[str, Any]],
    cantidad: int,
    intervalos: int,
    salida: Path,
) -> dict[str, Any]:
    directorio_java = salida / "java"
    ejecutar_java(cantidad, intervalos, directorio_java)

    secuencias = _leer_csv(directorio_java / "secuencias.csv")
    tabla_pruebas = _leer_csv(directorio_java / "pruebas.csv").set_index("configuracion")
    pi = _leer_csv(directorio_java / "pi.csv")

    comparaciones_secuencia = []
    comparaciones_pruebas = []
    for evaluacion in evaluaciones:
        resultado = evaluacion["resultado"]
        nombre = resultado.configuracion.nombre
        registros = secuencias[secuencias["configuracion"] == nombre]
        comparaciones_secuencia.append(
            comparacion.comparar_secuencia(resultado, registros.to_dict("records"))
        )
        comparaciones_pruebas.append(
            comparacion.comparar_pruebas(
                nombre,
                evaluacion["chi"],
                evaluacion["ks"],
                tabla_pruebas.loc[nombre].to_dict(),
            )
        )

    return {
        "disponible": True,
        "secuencias": comparaciones_secuencia,
        "pruebas": comparaciones_pruebas,
        "pi": pi.to_dict("records"),
    }


def _leer_csv(ruta: Path) -> pd.DataFrame:
    if not ruta.exists():
        raise ErrorJava(f"Java no genero el archivo esperado: {ruta.name}")
    return pd.read_csv(ruta, float_precision="round_trip")


def ejecutar_java(cantidad: int, intervalos: int, directorio: Path) -> None:
    java = shutil.which("java")
    javac = shutil.which("javac")
    if java is None or javac is None:
        raise ErrorJava("no se encontro Java en el PATH; instale un JDK o use --sin-java")

    compilar_java(javac)
    _ejecutar(
        [
            java,
            "-cp",
            str(JAVA_DIR),
            "Main",
            "--count",
            str(cantidad),
            "--bins",
            str(intervalos),
            "--output-dir",
            str(directorio),
        ],
        "la ejecucion de Java fallo",
    )


def compilar_java(javac: str) -> None:
    fuentes = sorted(JAVA_DIR.rglob("*.java"))
    if not fuentes:
        raise ErrorJava("no se encontraron archivos Java")
    if not any(_necesita_compilacion(fuente) for fuente in fuentes):
        return

    _ejecutar(
        [javac, "-encoding", "UTF-8", "-d", str(JAVA_DIR), *map(str, fuentes)],
        "la compilacion de Java fallo",
    )


def _necesita_compilacion(fuente: Path) -> bool:
    clase = fuente.with_suffix(".class")
    return not clase.exists() or fuente.stat().st_mtime > clase.stat().st_mtime


def _ejecutar(comando: list[str], mensaje: str) -> None:
    try:
        subprocess.run(
            comando,
            cwd=BASE_DIR,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.CalledProcessError as error:
        detalle = (error.stderr or error.stdout or "").strip()
        raise ErrorJava(f"{mensaje}: {detalle}") from error
