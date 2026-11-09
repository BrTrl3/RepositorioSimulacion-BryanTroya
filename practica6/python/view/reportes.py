"""Exportacion de resultados de la practica 6 a archivos CSV."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _guardar(tabla: pd.DataFrame, ruta: Path) -> Path:
    tabla.to_csv(ruta, index=False, encoding="utf-8")
    return ruta


def _tabla_secuencia(evaluacion: dict[str, Any]) -> pd.DataFrame:
    resultado = evaluacion["resultado"]
    return pd.DataFrame(
        {
            "n": range(1, resultado.cantidad + 1),
            "estado": resultado.estados,
            "u": resultado.normalizados,
        }
    )


def _tabla_frecuencias(evaluacion: dict[str, Any]) -> pd.DataFrame:
    chi = evaluacion["chi"]
    intervalos = len(chi["observadas"])
    return pd.DataFrame(
        {
            "limite_inferior": [i / intervalos for i in range(intervalos)],
            "limite_superior": [(i + 1) / intervalos for i in range(intervalos)],
            "observada": chi["observadas"],
            "esperada": chi["esperada"],
        }
    )


def _tabla_pruebas(evaluaciones: list[dict[str, Any]]) -> pd.DataFrame:
    filas = []
    for evaluacion in evaluaciones:
        configuracion = evaluacion["resultado"].configuracion
        chi, ks = evaluacion["chi"], evaluacion["ks"]
        filas.append(
            {
                "configuracion": configuracion.nombre,
                "a": configuracion.a,
                "c": configuracion.c,
                "m": configuracion.m,
                "semilla": configuracion.semilla,
                "chi2": chi["estadistico"],
                "gl": chi["grados_libertad"],
                "p_chi2": chi["valor_p"],
                "decision_chi2": chi["decision"],
                "d": ks["estadistico"],
                "p_ks": ks["valor_p"],
                "decision_ks": ks["decision"],
            }
        )
    return pd.DataFrame(filas)


def exportar_todo(datos: dict[str, Any]) -> dict[str, Path]:
    directorio = Path(datos["directorio_salida"])
    principal = datos["evaluaciones"][0]
    rutas = {
        "secuencia": _guardar(_tabla_secuencia(principal), directorio / "secuencia_python.csv"),
        "frecuencias": _guardar(_tabla_frecuencias(principal), directorio / "frecuencias_chi2.csv"),
        "pruebas": _guardar(_tabla_pruebas(datos["evaluaciones"]), directorio / "pruebas_python.csv"),
        "pi": _guardar(pd.DataFrame(datos["pi"]), directorio / "tabla_pi.csv"),
    }

    java = datos["java"]
    if java["disponible"]:
        rutas["comparacion_secuencia"] = _guardar(
            pd.DataFrame(java["secuencias"][0]["filas"]),
            directorio / "comparacion_python_java.csv",
        )
        rutas["comparacion_pruebas"] = _guardar(
            pd.DataFrame(java["pruebas"]),
            directorio / "comparacion_pruebas_python_java.csv",
        )
    return rutas
