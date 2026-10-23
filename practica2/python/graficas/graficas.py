import matplotlib.pyplot as plt


def graficar_modelos(
    t_deterministico,
    P_deterministico,
    t_discreto,
    P_discreto,
    t_estocastico,
    P_estocastico,
    t_continuo,
    P_continuo
):

    plt.figure(figsize=(10, 5))

    plt.plot(
        t_deterministico,
        P_deterministico,
        label="Deterministico"
    )

    plt.plot(
        t_discreto,
        P_discreto,
        label="Discreto"
    )

    plt.plot(
        t_estocastico,
        P_estocastico,
        label="Estocastico"
    )

    plt.plot(
        t_continuo,
        P_continuo,
        label="Continuo - Euler"
    )

    plt.xlabel("Tiempo")
    plt.ylabel("Poblacion")

    plt.title(
        "Comparacion de modelos de crecimiento poblacional"
    )

    plt.grid(True)

    plt.legend()

    plt.show()