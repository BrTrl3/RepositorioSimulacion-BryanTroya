def modelo_discreto(P0, r, tiempo):

    poblacion = [P0]

    for _ in range(1, tiempo + 1):

        poblacion_actual = poblacion[-1]

        incremento = r * poblacion_actual

        nueva_poblacion = poblacion_actual + incremento

        poblacion.append(nueva_poblacion)

    tiempo = list(range(tiempo + 1))

    return tiempo, poblacion