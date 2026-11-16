"""Generador Congruencial Lineal (LCG).

X_{n+1} = (a * X_n + c) mod m        U_n = X_n / m  en [0, 1)

Se usan los mismos parámetros que en la versión Java para que, con la
misma semilla, ambos programas produzcan exactamente la misma secuencia.
"""

# Parámetros de Numerical Recipes (periodo completo m = 2^32)
A = 1664525
C = 1013904223
M = 2 ** 32


class LCG:
    def __init__(self, semilla, a=A, c=C, m=M):
        self.a = a
        self.c = c
        self.m = m
        self.x = semilla % m

    def siguiente(self):
        """Devuelve el siguiente número pseudoaleatorio U en [0, 1)."""
        self.x = (self.a * self.x + self.c) % self.m
        return self.x / self.m
