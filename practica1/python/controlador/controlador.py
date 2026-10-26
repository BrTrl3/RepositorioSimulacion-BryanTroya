# controlador.py

from python.modelo.datos import (
    HORAS,
    HUMEDAD,
    NUBOSIDAD,
    TEMPERATURA
)

from python.modelo.modelo import (
    calcular_indice,
    calcular_indice_ajustado,
    determinar_estado,
    generar_pesos_aleatorios,
    verificar_pesos
)

from python.vista.vista import (
    mostrar_titulo,
    mostrar_pesos,
    mostrar_suma_pesos,
    mostrar_encabezado_tabla,
    mostrar_fila,
    mostrar_fin_tabla
)


def ejecutar_modelo():

    mostrar_titulo()

    # ==========================================
    # GENERAR PESOS ALEATORIOS
    # ==========================================

    (
        peso_humedad,
        peso_nubosidad,
        peso_temperatura
    ) = generar_pesos_aleatorios()

    # ==========================================
    # VERIFICAR PESOS
    # ==========================================

    suma_ajustada = verificar_pesos(
        peso_humedad,
        peso_nubosidad,
        peso_temperatura
    )

    # Mostrar los pesos mediante la vista
    mostrar_pesos(
        peso_humedad,
        peso_nubosidad,
        peso_temperatura
    )

    mostrar_suma_pesos(suma_ajustada)
    mostrar_encabezado_tabla()

    # ==========================================
    # RESULTADOS
    # ==========================================

    resultados = {
        "horas": list(HORAS),
        "humedad": list(HUMEDAD),
        "nubosidad": list(NUBOSIDAD),
        "temperatura": list(TEMPERATURA),
        "H": [],
        "N": [],
        "Tf": [],
        "indice_original": [],
        "estado_original": [],
        "indice_ajustado": [],
        "estado_ajustado": [],
        "pesos_ajustados": {
            "humedad": peso_humedad,
            "nubosidad": peso_nubosidad,
            "temperatura": peso_temperatura,
        },
    }

    for hora, humedad, nubosidad, temperatura in zip(
        HORAS,
        HUMEDAD,
        NUBOSIDAD,
        TEMPERATURA
    ):

        # ==========================================
        # MODELO ORIGINAL
        # ==========================================

        H, N, Tf, indice_original = calcular_indice(
            humedad,
            nubosidad,
            temperatura
        )

        estado_original = determinar_estado(
            indice_original
        )

        # ==========================================
        # MODELO AJUSTADO
        # ==========================================

        _, _, _, indice_ajustado = calcular_indice_ajustado(
            humedad,
            nubosidad,
            temperatura,
            peso_humedad,
            peso_nubosidad,
            peso_temperatura
        )

        estado_ajustado = determinar_estado(
            indice_ajustado
        )

        # ==========================================
        # GUARDAR RESULTADOS
        # ==========================================

        resultados["H"].append(H)
        resultados["N"].append(N)
        resultados["Tf"].append(Tf)
        resultados["indice_original"].append(indice_original)
        resultados["estado_original"].append(estado_original)
        resultados["indice_ajustado"].append(indice_ajustado)
        resultados["estado_ajustado"].append(estado_ajustado)

        # ==========================================
        # MOSTRAR RESULTADO
        # ==========================================

        mostrar_fila(
            hora,
            humedad,
            nubosidad,
            temperatura,
            H,
            N,
            Tf,
            indice_original,
            estado_original,
            indice_ajustado,
            estado_ajustado
        )

    mostrar_fin_tabla()

    return resultados
