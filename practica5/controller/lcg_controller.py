"""Controlador de la practica 5: orquesta generacion, analisis y comparacion."""

from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any

from model import analysis
from model.lcg import (
    A,
    C,
    M,
    SEMILLA_POR_DEFECTO,
    ParametrosLCG,
    generar_secuencia,
)

BASE_DIR = Path(__file__).resolve().parent.parent
JAVA_DIR = BASE_DIR / "java"
RESULTADOS_DIR = BASE_DIR / "resultados"
SEMILLA_ALTERNATIVA_POR_DEFECTO = 54321
CANTIDAD_POR_DEFECTO = 10000


class ErrorJava(Exception):
    """Error controlado cuando no es posible ejecutar la implementacion Java."""


def ejecutar_practica(
    semilla: int = SEMILLA_POR_DEFECTO,
    cantidad: int = CANTIDAD_POR_DEFECTO,
    semilla_alternativa: int = SEMILLA_ALTERNATIVA_POR_DEFECTO,
    intentar_java: bool = True,
    directorio_salida: Path | str | None = None,
) -> dict[str, Any]:
    if not isinstance(cantidad, int) or isinstance(cantidad, bool):
        raise TypeError("cantidad debe ser un entero")
    if cantidad <= 0:
        raise ValueError("cantidad debe ser mayor que cero")

    salida = Path(directorio_salida) if directorio_salida is not None else RESULTADOS_DIR
    salida.mkdir(parents=True, exist_ok=True)

    parametros = ParametrosLCG(a=A, c=C, m=M, semilla=semilla)
    principal = generar_secuencia(
        semilla=semilla,
        cantidad=cantidad,
        a=parametros.a,
        c=parametros.c,
        m=parametros.m,
    )
    alternativa = generar_secuencia(
        semilla=semilla_alternativa,
        cantidad=cantidad,
        a=parametros.a,
        c=parametros.c,
        m=parametros.m,
    )

    estadisticas = analysis.estadisticas_basicas(principal.normalizados)
    periodo = analysis.analizar_periodo(principal)
    comparacion_semillas = analysis.comparar_semillas(principal, alternativa)

    comparacion_java: dict[str, Any] | None = None
    if intentar_java:
        try:
            comparacion_java = _comparar_con_java(
                principal=principal,
                semilla=semilla,
                cantidad=cantidad,
                directorio_salida=salida,
            )
        except ErrorJava as error:
            comparacion_java = {
                "disponible": False,
                "error": str(error),
                "coinciden_todos": False,
                "total": 0,
                "filas": [],
            }

    return {
        "config": {
            "a": parametros.a,
            "c": parametros.c,
            "m": parametros.m,
            "semilla": semilla,
            "semilla_alternativa": semilla_alternativa,
            "cantidad": cantidad,
        },
        "principal": principal,
        "alternativa": alternativa,
        "estadisticas": estadisticas,
        "periodo": periodo,
        "comparacion_semillas": comparacion_semillas,
        "comparacion_java": comparacion_java,
        "directorio_salida": salida,
    }


def _comparar_con_java(
    principal: Any,
    semilla: int,
    cantidad: int,
    directorio_salida: Path,
) -> dict[str, Any]:
    ruta_csv = directorio_salida / f"java_lcg_{semilla}.csv"
    ejecutar_java(semilla=semilla, cantidad=cantidad, ruta_salida=ruta_csv)
    registros = leer_csv_java(ruta_csv)
    comparacion = analysis.comparar_con_java(principal, registros)
    comparacion["ruta_csv"] = str(ruta_csv)
    return comparacion


def ejecutar_java(
    semilla: int = SEMILLA_POR_DEFECTO,
    cantidad: int = CANTIDAD_POR_DEFECTO,
    ruta_salida: Path | str | None = None,
) -> Path:
    java = shutil.which("java")
    javac = shutil.which("javac")
    if java is None or javac is None:
        raise ErrorJava(
            "no se encontro Java en el PATH; instale un JDK o use --sin-java"
        )

    compilar_java(javac)

    salida = Path(ruta_salida) if ruta_salida is not None else (
        RESULTADOS_DIR / f"java_lcg_{semilla}.csv"
    )
    salida.parent.mkdir(parents=True, exist_ok=True)

    comando = [
        java,
        "-cp",
        str(JAVA_DIR),
        "Main",
        "--seed",
        str(semilla),
        "--count",
        str(cantidad),
        "--output",
        str(salida),
    ]
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
        raise ErrorJava(f"la ejecucion de Java fallo: {detalle}") from error

    if not salida.exists():
        raise ErrorJava("Java no genero el archivo CSV esperado")

    return salida


def compilar_java(javac: str | None = None) -> None:
    if not _necesita_compilacion():
        return

    javac = javac or shutil.which("javac")
    if javac is None:
        raise ErrorJava("no se encontro javac en el PATH")

    fuentes = [
        JAVA_DIR / "Main.java",
        JAVA_DIR / "modelo" / "LCG.java",
        JAVA_DIR / "controlador" / "LCGController.java",
        JAVA_DIR / "vista" / "Consola.java",
    ]
    faltantes = [str(fuente) for fuente in fuentes if not fuente.exists()]
    if faltantes:
        raise ErrorJava(f"faltan archivos Java: {', '.join(faltantes)}")

    comando = [
        javac,
        "-encoding",
        "UTF-8",
        "-d",
        str(JAVA_DIR),
        *[str(fuente) for fuente in fuentes],
    ]
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
        raise ErrorJava(f"la compilacion de Java fallo: {detalle}") from error


def _necesita_compilacion() -> bool:
    pares = [
        (JAVA_DIR / "Main.java", JAVA_DIR / "Main.class"),
        (JAVA_DIR / "modelo" / "LCG.java", JAVA_DIR / "modelo" / "LCG.class"),
        (
            JAVA_DIR / "controlador" / "LCGController.java",
            JAVA_DIR / "controlador" / "LCGController.class",
        ),
        (JAVA_DIR / "vista" / "Consola.java", JAVA_DIR / "vista" / "Consola.class"),
    ]
    for fuente, clase in pares:
        if not clase.exists():
            return True
        if fuente.stat().st_mtime > clase.stat().st_mtime:
            return True
    return False


def leer_csv_java(ruta: Path | str) -> list[dict[str, Any]]:
    ruta = Path(ruta)
    with ruta.open("r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        campos = set(lector.fieldnames or [])
        requeridos = {"n", "estado", "u"}
        if not requeridos.issubset(campos):
            raise ErrorJava(
                f"el CSV de Java no tiene las columnas esperadas: {sorted(requeridos)}"
            )
        return [
            {
                "n": int(fila["n"]),
                "estado": int(fila["estado"]),
                "u": float(fila["u"]),
            }
            for fila in lector
        ]
