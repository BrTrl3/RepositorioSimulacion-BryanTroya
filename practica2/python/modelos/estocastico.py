import numpy as np


def modelo_estocastico(P0, r, sigma, tiempo):

    poblacion = [P0]

    for _ in range(1, tiempo + 1):

        ruido = np.random.normal(0, sigma)

        poblacion_actual = poblacion[-1]

        nueva_poblacion = (
            poblacion_actual
            + (r * poblacion_actual)
            + ruido
        )

        if nueva_poblacion < 0:
            nueva_poblacion = 0

        poblacion.append(nueva_poblacion)

    tiempo = list(range(tiempo + 1))

    return tiempo, poblacion