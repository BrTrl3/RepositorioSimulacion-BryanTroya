# modelo.py

import numpy as np


# ==========================================
# MODELO ORIGINAL
# ==========================================

PESO_HUMEDAD_ORIGINAL = 0.5
PESO_NUBOSIDAD_ORIGINAL = 0.3
PESO_TEMPERATURA_ORIGINAL = 0.2

SEMILLA_POR_DEFECTO = 42


# ==========================================
# AJUSTE ALEATORIO
# ==========================================

def generar_pesos_aleatorios(semilla=SEMILLA_POR_DEFECTO):
    """
    Genera tres pesos aleatorios y los normaliza
    para que su suma sea igual a 1.

    Se usa una semilla fija para que los resultados
    sean reproducibles. Utilice semilla=None para
    obtener pesos distintos en cada ejecución.
    """

    generador = np.random.default_rng(semilla)

    pesos = generador.random(3)

    pesos = pesos / np.sum(pesos)

    peso_humedad = pesos[0]
    peso_nubosidad = pesos[1]
    peso_temperatura = pesos[2]

    return peso_humedad, peso_nubosidad, peso_temperatura


# ==========================================
# FACTOR DE TEMPERATURA
# ==========================================

def calcular_factor_temperatura(temperatura):
    """
    Obtiene el factor de temperatura según
    la tabla proporcionada en la guía.
    """

    factores = {
        10: 1.00,
        12: 0.90,
        14: 0.80,
        16: 0.70,
        18: 0.60,
        20: 0.50,
        22: 0.40,
        24: 0.30,
        26: 0.20,
        28: 0.10
    }

    if temperatura <= 10:
        return 1.00

    if temperatura >= 28:
        return 0.10

    if temperatura in factores:
        return factores[temperatura]

    temperaturas = sorted(factores.keys())

    for i in range(len(temperaturas) - 1):

        temperatura_inferior = temperaturas[i]
        temperatura_superior = temperaturas[i + 1]

        if temperatura_inferior < temperatura < temperatura_superior:

            factor_inferior = factores[temperatura_inferior]
            factor_superior = factores[temperatura_superior]

            factor = factor_inferior + (
                (temperatura - temperatura_inferior)
                / (temperatura_superior - temperatura_inferior)
            ) * (
                factor_superior - factor_inferior
            )

            return factor


# ==========================================
# MODELO ORIGINAL
# ==========================================

def calcular_indice_normalizado(
    H,
    N,
    Tf,
    peso_humedad=PESO_HUMEDAD_ORIGINAL,
    peso_nubosidad=PESO_NUBOSIDAD_ORIGINAL,
    peso_temperatura=PESO_TEMPERATURA_ORIGINAL
):
    """
    Calcula el índice a partir de las variables ya normalizadas.
    """

    return (
        peso_humedad * H
        + peso_nubosidad * N
        + peso_temperatura * Tf
    )


def calcular_indice(humedad, nubosidad, temperatura):
    """
    Calcula el índice utilizando:

    I = 0.5H + 0.3N + 0.2Tf
    """

    H = humedad / 100
    N = nubosidad / 100
    Tf = calcular_factor_temperatura(temperatura)

    indice = calcular_indice_normalizado(H, N, Tf)

    return H, N, Tf, indice


# ==========================================
# MODELO AJUSTADO ALEATORIAMENTE
# ==========================================

def calcular_indice_ajustado(
    humedad,
    nubosidad,
    temperatura,
    peso_humedad,
    peso_nubosidad,
    peso_temperatura
):
    """
    Calcula el índice utilizando los pesos
    generados aleatoriamente.

    I = wH + wN + wTf
    """

    H = humedad / 100
    N = nubosidad / 100
    Tf = calcular_factor_temperatura(temperatura)

    indice = calcular_indice_normalizado(
        H,
        N,
        Tf,
        peso_humedad,
        peso_nubosidad,
        peso_temperatura
    )

    return H, N, Tf, indice


# ==========================================
# DETERMINAR ESTADO
# ==========================================

def determinar_estado(indice):
    """
    Determina el estado según el índice obtenido.
    """

    if indice < 0.40:
        return "Sin lluvia"

    elif indice < 0.60:
        return "Baja posibilidad"

    elif indice < 0.75:
        return "Lluvia probable"

    else:
        return "Lluvia"


# ==========================================
# VERIFICAR PESOS
# ==========================================

def verificar_pesos(
    peso_humedad,
    peso_nubosidad,
    peso_temperatura
):
    """
    Verifica que los pesos ajustados sumen 1.
    """

    suma = (
        peso_humedad
        + peso_nubosidad
        + peso_temperatura
    )

    return suma