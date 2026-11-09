"""Pruebas de bondad de ajuste: Chi-cuadrado y Kolmogorov-Smirnov."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

ALFA = 0.05
INTERVALOS_POR_DEFECTO = 10
_EPSILON = 1e-15
_MAX_ITERACIONES = 1000


def _gamma_inferior_serie(a: float, x: float) -> float:
    termino = 1.0 / a
    suma = termino
    denominador = a
    for _ in range(_MAX_ITERACIONES):
        denominador += 1.0
        termino *= x / denominador
        suma += termino
        if abs(termino) < abs(suma) * _EPSILON:
            break
    return suma * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gamma_superior_fraccion(a: float, x: float) -> float:
    minimo = 1e-300
    b = x + 1.0 - a
    c = 1.0 / minimo
    d = 1.0 / b
    h = d
    for i in range(1, _MAX_ITERACIONES):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < minimo:
            d = minimo
        c = b + an / c
        if abs(c) < minimo:
            c = minimo
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _EPSILON:
            break
    return h * math.exp(-x + a * math.log(x) - math.lgamma(a))


def valor_p_chi_cuadrado(estadistico: float, grados_libertad: int) -> float:
    """P(X >= estadistico) con la gamma incompleta regularizada superior."""
    if estadistico <= 0.0:
        return 1.0
    a = grados_libertad / 2.0
    x = estadistico / 2.0
    if x < a + 1.0:
        return 1.0 - _gamma_inferior_serie(a, x)
    return _gamma_superior_fraccion(a, x)


def valor_p_kolmogorov(estadistico: float, cantidad: int) -> float:
    """Distribucion asintotica de Kolmogorov con la correccion de Stephens."""
    raiz = math.sqrt(cantidad)
    lam = (raiz + 0.12 + 0.11 / raiz) * estadistico
    if lam < 0.2:
        return 1.0

    suma = 0.0
    signo = 1.0
    for j in range(1, 101):
        termino = signo * math.exp(-2.0 * j * j * lam * lam)
        suma += termino
        if abs(termino) < 1e-16:
            break
        signo = -signo
    return min(max(2.0 * suma, 0.0), 1.0)


def decidir(valor_p: float, alfa: float = ALFA) -> str:
    return "No se rechaza H0" if valor_p >= alfa else "Se rechaza H0"


def chi_cuadrado(
    valores: np.ndarray,
    intervalos: int = INTERVALOS_POR_DEFECTO,
    alfa: float = ALFA,
) -> dict[str, Any]:
    if len(valores) == 0:
        raise ValueError("se requiere al menos un valor")
    if intervalos < 2:
        raise ValueError("se requieren al menos dos intervalos")

    indices = np.minimum((valores * intervalos).astype(np.int64), intervalos - 1)
    observadas = np.bincount(indices, minlength=intervalos)
    esperada = len(valores) / intervalos

    estadistico = 0.0
    for observada in observadas:
        estadistico += (int(observada) - esperada) ** 2 / esperada

    grados_libertad = intervalos - 1
    valor_p = valor_p_chi_cuadrado(estadistico, grados_libertad)
    return {
        "observadas": [int(valor) for valor in observadas],
        "esperada": esperada,
        "estadistico": estadistico,
        "grados_libertad": grados_libertad,
        "valor_p": valor_p,
        "decision": decidir(valor_p, alfa),
    }


def kolmogorov_smirnov(valores: np.ndarray, alfa: float = ALFA) -> dict[str, Any]:
    if len(valores) == 0:
        raise ValueError("se requiere al menos un valor")

    ordenados = np.sort(valores)
    cantidad = len(ordenados)
    posiciones = np.arange(1, cantidad + 1)
    d_positiva = float(np.max(posiciones / cantidad - ordenados))
    d_negativa = float(np.max(ordenados - (posiciones - 1) / cantidad))
    estadistico = max(d_positiva, d_negativa)

    valor_p = valor_p_kolmogorov(estadistico, cantidad)
    return {
        "d_positiva": d_positiva,
        "d_negativa": d_negativa,
        "estadistico": estadistico,
        "valor_p": valor_p,
        "decision": decidir(valor_p, alfa),
    }
