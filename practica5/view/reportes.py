"""Exportacion de resultados de la practica 5 a archivos CSV."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable, Sequence

from model.lcg import ResultadoGeneracion


def _escribir_csv(
    ruta: Path | str,
    campos: Sequence[str],
    filas: Iterable[dict[str, Any]],
) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(campos))
        escritor.writeheader()
        for fila in filas:
            escritor.writerow(fila)
    return ruta


def exportar_valores(
    resultado: ResultadoGeneracion,
    ruta: Path | str,
) -> Path:
    filas = [
        {"n": indice, "estado": estado, "u": normalizado}
        for indice, (estado, normalizado) in enumerate(
            zip(resultado.estados, resultado.normalizados),
            start=1,
        )
    ]
    return _escribir_csv(ruta, ["n", "estado", "u"], filas)


def exportar_primeros_20(
    resultado: ResultadoGeneracion,
    ruta: Path | str,
) -> Path:
    filas = [
        {"n": indice, "estado": estado, "u": normalizado}
        for indice, estado, normalizado in resultado.primeros(20)
    ]
    return _escribir_csv(ruta, ["n", "estado", "u"], filas)


def exportar_resumen(
    estadisticas: dict[str, Any],
    ruta: Path | str,
) -> Path:
    filas = [
        {"metrica": "cantidad", "valor": estadisticas["cantidad"]},
        {"metrica": "media", "valor": estadisticas["media"]},
        {
            "metrica": "desviacion_estandar",
            "valor": estadisticas["desviacion_estandar"],
        },
        {"metrica": "minimo", "valor": estadisticas["minimo"]},
        {"metrica": "maximo", "valor": estadisticas["maximo"]},
        {
            "metrica": "correlacion_lag1",
            "valor": estadisticas["correlacion_lag1"],
        },
    ]
    for indice, frecuencia in enumerate(estadisticas["frecuencias_bins"], start=1):
        filas.append(
            {
                "metrica": f"bin_{indice}",
                "valor": frecuencia,
            }
        )
    return _escribir_csv(ruta, ["metrica", "valor"], filas)


def exportar_comparacion_semillas(
    filas_comparacion: Sequence[dict[str, Any]],
    ruta: Path | str,
) -> Path:
    return _escribir_csv(
        ruta,
        ["n", "u_principal", "u_alternativa", "diferencia"],
        filas_comparacion,
    )


def exportar_periodo(
    periodo: dict[str, Any],
    ruta: Path | str,
) -> Path:
    teorico = periodo["teorico"]
    toy = periodo["toy"]
    filas = [
        {
            "elemento": "periodo_completo",
            "valor": teorico["periodo_completo"],
        },
        {
            "elemento": "periodo_maximo_teorico",
            "valor": teorico["periodo_maximo_teorico"],
        },
        {
            "elemento": "sin_repeticion_en_muestra",
            "valor": periodo["sin_repeticion_en_muestra"],
        },
        {
            "elemento": "cantidad_muestra",
            "valor": periodo["cantidad_muestra"],
        },
        {
            "elemento": "toy_encontrado",
            "valor": toy["encontrado"],
        },
        {
            "elemento": "toy_mu",
            "valor": toy["mu"],
        },
        {
            "elemento": "toy_lambda",
            "valor": toy["lambda"],
        },
    ]
    for condicion in teorico["condiciones"]:
        filas.append(
            {
                "elemento": condicion["nombre"],
                "valor": condicion["cumple"],
            }
        )
    return _escribir_csv(ruta, ["elemento", "valor"], filas)


def exportar_comparacion_java(
    comparacion: dict[str, Any],
    ruta: Path | str,
) -> Path:
    filas = [
        {
            "n": fila["n"],
            "python_estado": fila["python_estado"],
            "java_estado": fila["java_estado"],
            "python_u": fila["python_u"],
            "java_u": fila["java_u"],
            "coincide": fila["coincide"],
        }
        for fila in comparacion["filas"]
    ]
    return _escribir_csv(
        ruta,
        [
            "n",
            "python_estado",
            "java_estado",
            "python_u",
            "java_u",
            "coincide",
        ],
        filas,
    )


def exportar_todo(
    principal: ResultadoGeneracion,
    alternativa: ResultadoGeneracion,
    estadisticas: dict[str, Any],
    periodo: dict[str, Any],
    comparacion_semillas: Sequence[dict[str, Any]],
    comparacion_java: dict[str, Any] | None,
    directorio: Path | str,
) -> dict[str, Path]:
    directorio = Path(directorio)
    rutas = {
        "valores_python": exportar_valores(
            principal, directorio / f"valores_python_{principal.parametros.semilla}.csv"
        ),
        "valores_python_alternativa": exportar_valores(
            alternativa,
            directorio
            / f"valores_python_{alternativa.parametros.semilla}.csv",
        ),
        "primeros_20": exportar_primeros_20(
            principal, directorio / "primeros_20_python.csv"
        ),
        "resumen": exportar_resumen(estadisticas, directorio / "resumen.csv"),
        "periodo": exportar_periodo(periodo, directorio / "periodo.csv"),
        "comparacion_semillas": exportar_comparacion_semillas(
            comparacion_semillas, directorio / "comparacion_semillas.csv"
        ),
    }
    if comparacion_java is not None and comparacion_java.get("disponible"):
        rutas["comparacion_java"] = exportar_comparacion_java(
            comparacion_java, directorio / "comparacion_python_java.csv"
        )
    return rutas
