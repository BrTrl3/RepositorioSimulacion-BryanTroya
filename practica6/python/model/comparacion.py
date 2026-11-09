"""Comparacion de los resultados de Python y Java."""

from __future__ import annotations

import math
from typing import Any, Sequence

from .lcg import ResultadoGeneracion

TOLERANCIA = 1e-9


def comparar_secuencia(
    resultado: ResultadoGeneracion,
    registros_java: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    total = min(resultado.cantidad, len(registros_java))
    filas: list[dict[str, Any]] = []
    diferencias = abs(resultado.cantidad - len(registros_java))

    for indice in range(total):
        estado_python = resultado.estados[indice]
        u_python = float(resultado.normalizados[indice])
        registro = registros_java[indice]
        coincide = estado_python == registro["estado"] and u_python == registro["u"]
        if not coincide:
            diferencias += 1
        if indice < 20:
            filas.append(
                {
                    "n": indice + 1,
                    "python_estado": estado_python,
                    "java_estado": registro["estado"],
                    "python_u": u_python,
                    "java_u": registro["u"],
                    "coincide": coincide,
                }
            )

    return {
        "configuracion": resultado.configuracion.nombre,
        "total": total,
        "diferencias": diferencias,
        "filas": filas,
    }


def comparar_pruebas(
    nombre: str,
    chi: dict[str, Any],
    ks: dict[str, Any],
    java: dict[str, Any],
) -> dict[str, Any]:
    pares = [
        (chi["estadistico"], java["chi2"]),
        (chi["valor_p"], java["p_chi2"]),
        (ks["estadistico"], java["d"]),
        (ks["valor_p"], java["p_ks"]),
    ]
    coincide = all(
        math.isclose(python, valor_java, rel_tol=1e-12, abs_tol=TOLERANCIA)
        for python, valor_java in pares
    )
    return {
        "configuracion": nombre,
        "python_chi2": chi["estadistico"],
        "java_chi2": java["chi2"],
        "python_p_chi2": chi["valor_p"],
        "java_p_chi2": java["p_chi2"],
        "python_d": ks["estadistico"],
        "java_d": java["d"],
        "python_p_ks": ks["valor_p"],
        "java_p_ks": java["p_ks"],
        "coincide": coincide,
    }
