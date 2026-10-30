"""Analisis estadistico, de periodo y comparaciones del LCG."""

from __future__ import annotations

import math
from statistics import fmean, pstdev
from typing import Any, Sequence

from .lcg import A, C, M, ResultadoGeneracion


def estadisticas_basicas(
    normalizados: Sequence[float],
    bins: int = 10,
) -> dict[str, Any]:
    if not normalizados:
        raise ValueError("se requiere al menos un valor normalizado")
    if bins <= 0:
        raise ValueError("bins debe ser mayor que cero")

    cantidad = len(normalizados)
    media = fmean(normalizados)
    desviacion = pstdev(normalizados) if cantidad > 1 else 0.0
    minimo = min(normalizados)
    maximo = max(normalizados)

    frecuencias = [0] * bins
    for valor in normalizados:
        indice = min(int(valor * bins), bins - 1)
        frecuencias[indice] += 1

    if cantidad > 1:
        x = normalizados[:-1]
        y = normalizados[1:]
        media_x = fmean(x)
        media_y = fmean(y)
        covarianza = sum(
            (valor_x - media_x) * (valor_y - media_y)
            for valor_x, valor_y in zip(x, y)
        ) / len(x)
        desviacion_x = pstdev(x)
        desviacion_y = pstdev(y)
        correlacion = (
            covarianza / (desviacion_x * desviacion_y)
            if desviacion_x > 0 and desviacion_y > 0
            else 0.0
        )
    else:
        correlacion = 0.0

    return {
        "cantidad": cantidad,
        "media": media,
        "desviacion_estandar": desviacion,
        "minimo": minimo,
        "maximo": maximo,
        "frecuencias_bins": frecuencias,
        "bins": bins,
        "correlacion_lag1": correlacion,
    }


def factores_primos(numero: int) -> list[int]:
    if numero < 2:
        return []

    factores: list[int] = []
    if numero % 2 == 0:
        factores.append(2)
        while numero % 2 == 0:
            numero //= 2

    divisor = 3
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            factores.append(divisor)
            while numero % divisor == 0:
                numero //= divisor
        divisor += 2

    if numero > 1:
        factores.append(numero)
    return factores


def analizar_periodo_teorico(
    a: int = A,
    c: int = C,
    m: int = M,
) -> dict[str, Any]:
    if m <= 1:
        raise ValueError("m debe ser mayor que uno")

    primos = factores_primos(m)
    condiciones = [
        {
            "nombre": "mcd(c, m) = 1",
            "cumple": math.gcd(c, m) == 1,
            "detalle": f"mcd({c}, {m}) = {math.gcd(c, m)}",
        },
        {
            "nombre": "todo factor primo de m divide a a - 1",
            "cumple": all((a - 1) % primo == 0 for primo in primos),
            "detalle": f"factores primos de m: {primos}",
        },
        {
            "nombre": "si m es divisible por 4, entonces (a - 1) es divisible por 4",
            "cumple": (m % 4 != 0) or ((a - 1) % 4 == 0),
            "detalle": f"(a - 1) mod 4 = {(a - 1) % 4}",
        },
    ]
    periodo_completo = all(condicion["cumple"] for condicion in condiciones)

    return {
        "a": a,
        "c": c,
        "m": m,
        "factores_primos_m": primos,
        "condiciones": condiciones,
        "periodo_completo": periodo_completo,
        "periodo_maximo_teorico": m if periodo_completo else None,
    }


def detectar_periodo(
    semilla: int,
    a: int = A,
    c: int = C,
    m: int = M,
    max_iteraciones: int = 2_000_000,
) -> dict[str, Any]:
    if max_iteraciones <= 0:
        raise ValueError("max_iteraciones debe ser mayor que cero")
    if not 0 <= semilla < m:
        raise ValueError("la semilla debe cumplir 0 <= semilla < m")

    def f(x: int) -> int:
        return (a * x + c) % m

    tortuga = f(semilla)
    liebre = f(f(semilla))
    pasos = 0

    while tortuga != liebre and pasos < max_iteraciones:
        tortuga = f(tortuga)
        liebre = f(f(liebre))
        pasos += 1

    if tortuga != liebre:
        return {
            "encontrado": False,
            "iteraciones": pasos,
            "max_iteraciones": max_iteraciones,
            "mu": None,
            "lambda": None,
        }

    mu = 0
    tortuga = semilla
    while tortuga != liebre:
        tortuga = f(tortuga)
        liebre = f(liebre)
        mu += 1

    lambda_ciclo = 1
    liebre = f(tortuga)
    while tortuga != liebre:
        liebre = f(liebre)
        lambda_ciclo += 1

    return {
        "encontrado": True,
        "iteraciones": pasos,
        "max_iteraciones": max_iteraciones,
        "mu": mu,
        "lambda": lambda_ciclo,
    }


def analizar_periodo(resultado: ResultadoGeneracion) -> dict[str, Any]:
    parametros = resultado.parametros
    teorico = analizar_periodo_teorico(parametros.a, parametros.c, parametros.m)
    toy = detectar_periodo(
        semilla=1,
        a=5,
        c=3,
        m=16,
        max_iteraciones=100,
    )
    sin_repeticion = len(set(resultado.estados)) == len(resultado.estados)

    return {
        "teorico": teorico,
        "toy": toy,
        "sin_repeticion_en_muestra": sin_repeticion,
        "cantidad_muestra": resultado.cantidad,
    }


def comparar_semillas(
    principal: ResultadoGeneracion,
    alternativa: ResultadoGeneracion,
    cantidad: int = 20,
) -> list[dict[str, float | int]]:
    limite = min(cantidad, principal.cantidad, alternativa.cantidad)
    filas: list[dict[str, float | int]] = []
    for indice in range(limite):
        u_principal = principal.normalizados[indice]
        u_alternativa = alternativa.normalizados[indice]
        filas.append(
            {
                "n": indice + 1,
                "u_principal": u_principal,
                "u_alternativa": u_alternativa,
                "diferencia": abs(u_principal - u_alternativa),
            }
        )
    return filas


def comparar_con_java(
    resultado_python: ResultadoGeneracion,
    registros_java: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    if not registros_java:
        return {
            "disponible": False,
            "error": "Java no genero registros",
            "coinciden_todos": False,
            "total": 0,
            "filas": [],
        }

    total_python = resultado_python.cantidad
    total_java = len(registros_java)
    filas: list[dict[str, Any]] = []
    diferencias = 0

    for indice in range(min(total_python, total_java)):
        estado_python = resultado_python.estados[indice]
        u_python = resultado_python.normalizados[indice]
        registro_java = registros_java[indice]
        estado_java = int(registro_java["estado"])
        u_java = float(registro_java.get("u", estado_java / resultado_python.parametros.m))
        coincide = estado_python == estado_java and math.isclose(
            u_python,
            u_java,
            rel_tol=0.0,
            abs_tol=1e-15,
        )
        if not coincide:
            diferencias += 1
        filas.append(
            {
                "n": indice + 1,
                "python_estado": estado_python,
                "java_estado": estado_java,
                "python_u": u_python,
                "java_u": u_java,
                "coincide": coincide,
            }
        )

    coinciden_todos = (
        total_python == total_java
        and diferencias == 0
        and total_python > 0
    )

    return {
        "disponible": True,
        "coinciden_todos": coinciden_todos,
        "total": min(total_python, total_java),
        "total_python": total_python,
        "total_java": total_java,
        "diferencias": diferencias,
        "filas": filas[:20],
    }
