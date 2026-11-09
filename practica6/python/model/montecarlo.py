"""Estimacion de pi por Monte Carlo usando el LCG."""

from __future__ import annotations

import math
from typing import Any

from .lcg import ConfiguracionLCG

TAMANOS_PI = [1000, 10000, 100000, 1000000]


def estimar_pi(configuracion: ConfiguracionLCG, puntos: int) -> dict[str, Any]:
    if puntos <= 0:
        raise ValueError("puntos debe ser mayor que cero")

    a, c, m = configuracion.a, configuracion.c, configuracion.m
    actual = configuracion.semilla
    dentro = 0
    for _ in range(puntos):
        actual = (a * actual + c) % m
        x = actual / m
        actual = (a * actual + c) % m
        y = actual / m
        if x * x + y * y <= 1.0:
            dentro += 1

    pi = 4.0 * dentro / puntos
    return {"n": puntos, "pi": pi, "error": abs(pi - math.pi)}
