def modelo_continuo(P0, r, tiempo, dt):

    t = [0]
    poblacion = [P0]

    while t[-1] < tiempo:

        poblacion_actual = poblacion[-1]

        cambio = r * poblacion_actual

        nueva_poblacion = (
            poblacion_actual
            + dt * cambio
        )

        poblacion.append(nueva_poblacion)

        t.append(t[-1] + dt)

    return t, poblacion