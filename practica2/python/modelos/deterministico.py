import numpy as np


def modelo_deterministico(P0, r, tiempo):
    t = np.arange(0, tiempo + 1)

    P = P0 * np.exp(r * t)

    return t, P