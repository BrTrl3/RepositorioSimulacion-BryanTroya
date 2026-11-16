"""Estimación de pi mediante el método de Monte Carlo.

Se generan N puntos (x, y) en el cuadrado [0,1) x [0,1) y se cuentan los que
caen dentro del cuarto de círculo de radio 1 (x^2 + y^2 <= 1):

    pi ≈ 4 * (Nc / N)
"""

import math
import time

import numpy as np

from python.modelo.lcg import LCG, A, C, M


def estimar_pi(n, semilla):
    """Monte Carlo con el LCG propio (misma secuencia que Java).

    Devuelve (pi_estimado, dentro)."""
    gen = LCG(semilla)
    dentro = 0
    for _ in range(n):
        x = gen.siguiente()
        y = gen.siguiente()
        if x * x + y * y <= 1.0:
            dentro += 1
    return 4.0 * dentro / n, dentro


def estimar_pi_numpy(n, semilla):
    """Monte Carlo vectorizado con el generador de NumPy (solo comparativo)."""
    rng = np.random.default_rng(semilla)
    x = rng.random(n)
    y = rng.random(n)
    dentro = int(np.count_nonzero(x * x + y * y <= 1.0))
    return 4.0 * dentro / n, dentro


def medir(funcion, n, semilla, repeticiones):
    """Ejecuta la función varias veces y devuelve el resultado y el tiempo
    promedio en segundos."""
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(n, semilla)
        tiempos.append(time.perf_counter() - inicio)
    return resultado, sum(tiempos) / len(tiempos)


def experimento(tamanos, semilla, repeticiones):
    """Experimento principal: una fila por tamaño de muestra."""
    filas = []
    for n in tamanos:
        (pi_est, dentro), t = medir(estimar_pi, n, semilla, repeticiones)
        (pi_np, _), t_np = medir(estimar_pi_numpy, n, semilla, repeticiones)
        filas.append({
            "n": n,
            "dentro": dentro,
            "pi": pi_est,
            "error": abs(pi_est - math.pi),
            "error_relativo_pct": abs(pi_est - math.pi) / math.pi * 100,
            "tiempo_python": t,
            "pi_numpy": pi_np,
            "error_numpy": abs(pi_np - math.pi),
            "tiempo_numpy": t_np,
        })
    return filas


def experimento_semillas(tamanos, semillas):
    """Repite el experimento con varias semillas para estudiar la variabilidad
    del estimador (media, desviación y error estándar teórico)."""
    estimaciones = {n: [estimar_pi_numpy(n, s)[0] for s in semillas] for n in tamanos}
    filas = []
    for n, valores in estimaciones.items():
        v = np.array(valores)
        errores = np.abs(v - math.pi)
        filas.append({
            "n": n,
            "replicas": len(v),
            "media_pi": float(v.mean()),
            "desviacion": float(v.std(ddof=1)),
            "error_estandar_teorico": 4 * math.sqrt((math.pi / 4) * (1 - math.pi / 4) / n),
            "error_medio": float(errores.mean()),
            "error_maximo": float(errores.max()),
            "minimo": float(v.min()),
            "maximo": float(v.max()),
        })
    return filas, estimaciones


def convergencia(n, semilla, puntos=200):
    """Estimación acumulada de pi a lo largo de una corrida (para graficar)."""
    gen = LCG(semilla)
    marcas = set(np.unique(np.logspace(1, math.log10(n), puntos).astype(int)))
    dentro = 0
    xs, ys = [], []
    for i in range(1, n + 1):
        x = gen.siguiente()
        y = gen.siguiente()
        if x * x + y * y <= 1.0:
            dentro += 1
        if i in marcas:
            xs.append(i)
            ys.append(4.0 * dentro / i)
    return xs, ys


def muestra_puntos(n, semilla):
    """Primeros n puntos generados por el LCG (para el diagrama de dispersión)."""
    gen = LCG(semilla)
    puntos = [(gen.siguiente(), gen.siguiente()) for _ in range(n)]
    x = np.array([p[0] for p in puntos])
    y = np.array([p[1] for p in puntos])
    return x, y, (x * x + y * y) <= 1.0


PARAMETROS_LCG = {"a": A, "c": C, "m": M}
