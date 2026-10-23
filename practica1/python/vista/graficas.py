# graficas.py

import matplotlib.pyplot as plt


def graficar_indices(
    horas,
    indices_originales,
    indices_ajustados
):

    plt.figure(figsize=(12, 6))

    # Modelo original
    plt.plot(
        horas,
        indices_originales,
        marker="o",
        label="Modelo original"
    )

    # Modelo ajustado
    plt.plot(
        horas,
        indices_ajustados,
        marker="s",
        label="Modelo ajustado"
    )

    # Límites de clasificación
    plt.axhline(
        y=0.40,
        linestyle="--",
        label="Límite 0.40"
    )

    plt.axhline(
        y=0.60,
        linestyle="--",
        label="Límite 0.60"
    )

    plt.axhline(
        y=0.75,
        linestyle="--",
        label="Límite 0.75"
    )

    # Etiquetas
    plt.xlabel("Hora")
    plt.ylabel("Índice de posibilidad de lluvia")

    plt.title(
        "Comparación del modelo original y modelo ajustado"
    )

    # Escala del índice
    plt.ylim(0, 1)

    # Cuadrícula
    plt.grid(True)

    # Leyenda
    plt.legend()

    # Mostrar gráfica
    plt.show()