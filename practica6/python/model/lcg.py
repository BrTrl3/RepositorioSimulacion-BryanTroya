"""Modelo matematico del generador congruencial lineal."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

CANTIDAD_POR_DEFECTO = 10000


@dataclass(frozen=True)
class ConfiguracionLCG:
    nombre: str
    a: int
    c: int
    m: int
    semilla: int

    def __post_init__(self) -> None:
        if self.a <= 0:
            raise ValueError("a debe ser mayor que cero")
        if self.c < 0:
            raise ValueError("c no puede ser negativo")
        if self.m <= 1:
            raise ValueError("m debe ser mayor que uno")
        if not 0 <= self.semilla < self.m:
            raise ValueError("la semilla debe cumplir 0 <= semilla < m")


CONFIGURACIONES = [
    ConfiguracionLCG("Guia semilla 12345", 1664525, 1013904223, 2**32, 12345),
    ConfiguracionLCG("Guia semilla 54321", 1664525, 1013904223, 2**32, 54321),
    ConfiguracionLCG("MINSTD", 16807, 0, 2**31 - 1, 12345),
    ConfiguracionLCG("RANDU", 65539, 0, 2**31, 12345),
    ConfiguracionLCG("Periodo corto", 5, 3, 16, 1),
    ConfiguracionLCG("Multiplicador a=1", 1, 1000, 2**32, 12345),
]


@dataclass
class ResultadoGeneracion:
    configuracion: ConfiguracionLCG
    estados: list[int]
    normalizados: np.ndarray

    @property
    def cantidad(self) -> int:
        return len(self.estados)


def generar_secuencia(
    configuracion: ConfiguracionLCG,
    cantidad: int = CANTIDAD_POR_DEFECTO,
) -> ResultadoGeneracion:
    if cantidad <= 0:
        raise ValueError("cantidad debe ser mayor que cero")

    a, c, m = configuracion.a, configuracion.c, configuracion.m
    actual = configuracion.semilla
    estados: list[int] = []
    for _ in range(cantidad):
        actual = (a * actual + c) % m
        estados.append(actual)

    return ResultadoGeneracion(
        configuracion=configuracion,
        estados=estados,
        normalizados=np.array(estados, dtype=np.float64) / m,
    )
