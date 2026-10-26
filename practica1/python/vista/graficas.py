# graficas.py

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from python.modelo.modelo import (
    calcular_indice_normalizado,
    PESO_HUMEDAD_ORIGINAL,
    PESO_NUBOSIDAD_ORIGINAL,
    PESO_TEMPERATURA_ORIGINAL,
)


DIRECTORIO_RESULTADOS = (
    Path(__file__).resolve().parents[2] / "resultados"
)


def _guardar(figura, nombre):
    DIRECTORIO_RESULTADOS.mkdir(exist_ok=True)
    ruta = DIRECTORIO_RESULTADOS / nombre
    figura.savefig(ruta, dpi=150, bbox_inches="tight")
    return ruta


def _grafica_comparacion(resultados):

    figura, eje = plt.subplots(figsize=(12, 6))

    eje.plot(
        resultados["horas"],
        resultados["indice_original"],
        marker="o",
        label="Modelo original"
    )

    eje.plot(
        resultados["horas"],
        resultados["indice_ajustado"],
        marker="s",
        label="Modelo ajustado"
    )

    for limite in (0.40, 0.60, 0.75):
        eje.axhline(
            y=limite,
            linestyle="--",
            label=f"Límite {limite:.2f}"
        )

    eje.set_xlabel("Hora")
    eje.set_ylabel("Índice de posibilidad de lluvia")
    eje.set_title(
        "Comparación del modelo original y modelo ajustado"
    )
    eje.set_ylim(0, 1)
    eje.grid(True)
    eje.legend()

    return _guardar(figura, "01_comparacion.png")


def _grafica_variables(resultados):

    figura, ejes = plt.subplots(
        3,
        1,
        figsize=(12, 9),
        sharex=True
    )

    series = [
        ("H", "Humedad normalizada (H)", "tab:blue"),
        ("N", "Nubosidad normalizada (N)", "tab:green"),
        ("Tf", "Factor de temperatura (Tf)", "tab:orange"),
    ]

    for eje, (clave, etiqueta, color) in zip(ejes, series):
        eje.plot(
            resultados["horas"],
            resultados[clave],
            marker="o",
            color=color,
            label=etiqueta
        )
        eje.set_ylabel(etiqueta)
        eje.set_ylim(0, 1.05)
        eje.grid(True)
        eje.legend(loc="upper right")

    ejes[-1].set_xlabel("Hora")

    figura.suptitle(
        "Comportamiento de las variables del modelo durante el día"
    )
    figura.tight_layout()

    return _guardar(figura, "02_variables.png")


def _grafica_influencia():

    valores = np.linspace(0, 1, 100)
    fijo = 0.6

    figura, ejes = plt.subplots(
        1,
        3,
        figsize=(15, 5)
    )

    # Influencia de H
    indices = [
        calcular_indice_normalizado(h, fijo, fijo)
        for h in valores
    ]
    ejes[0].plot(valores, indices, color="tab:blue")
    ejes[0].set_title("Influencia de H")
    ejes[0].set_xlabel("H")
    ejes[0].set_ylabel("Índice I")

    # Influencia de N
    indices = [
        calcular_indice_normalizado(fijo, n, fijo)
        for n in valores
    ]
    ejes[1].plot(valores, indices, color="tab:green")
    ejes[1].set_title("Influencia de N")
    ejes[1].set_xlabel("N")

    # Influencia de Tf
    indices = [
        calcular_indice_normalizado(fijo, fijo, tf)
        for tf in valores
    ]
    ejes[2].plot(valores, indices, color="tab:orange")
    ejes[2].set_title("Influencia de Tf")
    ejes[2].set_xlabel("Tf")

    for eje in ejes:
        eje.set_ylim(0, 1)
        eje.grid(True)

    figura.suptitle(
        "Influencia de cada parámetro en el índice de lluvia "
        f"(pesos {PESO_HUMEDAD_ORIGINAL}, {PESO_NUBOSIDAD_ORIGINAL}, "
        f"{PESO_TEMPERATURA_ORIGINAL})"
    )
    figura.tight_layout()

    return _guardar(figura, "03_influencia_parametros.png")


def generar_graficas(resultados):
    """
    Genera y guarda las gráficas de la práctica.
    Devuelve las rutas de los archivos creados.
    """

    rutas = [
        _grafica_comparacion(resultados),
        _grafica_variables(resultados),
        _grafica_influencia(),
    ]

    if matplotlib.get_backend().lower() != "agg":
        plt.show()

    return rutas
