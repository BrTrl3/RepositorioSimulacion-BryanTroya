"""Modelo matematico del generador congruencial lineal."""

from __future__ import annotations

from dataclasses import dataclass

A = 1664525
C = 1013904223
M = 2**32
SEMILLA_POR_DEFECTO = 12345


@dataclass(frozen=True)
class ParametrosLCG:
    a: int = A
    c: int = C
    m: int = M
    semilla: int = SEMILLA_POR_DEFECTO

    def __post_init__(self) -> None:
        valores = {
            "a": self.a,
            "c": self.c,
            "m": self.m,
            "semilla": self.semilla,
        }
        for nombre, valor in valores.items():
            if not isinstance(valor, int) or isinstance(valor, bool):
                raise TypeError(f"{nombre} debe ser un entero")
        if self.a <= 0:
            raise ValueError("a debe ser mayor que cero")
        if self.c < 0:
            raise ValueError("c no puede ser negativo")
        if self.m <= 1:
            raise ValueError("m debe ser mayor que uno")
        if not 0 <= self.semilla < self.m:
            raise ValueError("la semilla debe cumplir 0 <= semilla < m")

    def con_semilla(self, semilla: int) -> "ParametrosLCG":
        return ParametrosLCG(a=self.a, c=self.c, m=self.m, semilla=semilla)


@dataclass
class ResultadoGeneracion:
    parametros: ParametrosLCG
    estados: list[int]
    normalizados: list[float]

    @property
    def cantidad(self) -> int:
        return len(self.estados)

    def primeros(self, cantidad: int = 20) -> list[tuple[int, int, float]]:
        return [
            (indice, estado, normalizado)
            for indice, (estado, normalizado) in enumerate(
                zip(self.estados[:cantidad], self.normalizados[:cantidad]),
                start=1,
            )
        ]


class LCG:
    def __init__(
        self,
        parametros: ParametrosLCG | None = None,
        semilla: int | None = None,
    ) -> None:
        if parametros is None:
            parametros = ParametrosLCG()
        if semilla is not None:
            parametros = parametros.con_semilla(semilla)
        self.parametros = parametros
        self._estado = parametros.semilla

    @property
    def estado(self) -> int:
        return self._estado

    def reiniciar(self, semilla: int | None = None) -> None:
        if semilla is None:
            semilla = self.parametros.semilla
        self.parametros = self.parametros.con_semilla(semilla)
        self._estado = semilla

    def siguiente(self) -> int:
        self._estado = (
            self.parametros.a * self._estado + self.parametros.c
        ) % self.parametros.m
        return self._estado

    def siguiente_normalizado(self) -> float:
        return self.siguiente() / self.parametros.m

    def generar(self, cantidad: int) -> ResultadoGeneracion:
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("cantidad debe ser un entero")
        if cantidad <= 0:
            raise ValueError("cantidad debe ser mayor que cero")

        estados: list[int] = []
        normalizados: list[float] = []
        for _ in range(cantidad):
            estado = self.siguiente()
            estados.append(estado)
            normalizados.append(estado / self.parametros.m)

        return ResultadoGeneracion(
            parametros=self.parametros,
            estados=estados,
            normalizados=normalizados,
        )


def generar_secuencia(
    semilla: int = SEMILLA_POR_DEFECTO,
    cantidad: int = 10000,
    a: int = A,
    c: int = C,
    m: int = M,
) -> ResultadoGeneracion:
    parametros = ParametrosLCG(a=a, c=c, m=m, semilla=semilla)
    return LCG(parametros=parametros).generar(cantidad)
