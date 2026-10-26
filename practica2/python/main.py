from modelos.deterministico import modelo_deterministico
from modelos.discreto import modelo_discreto
from modelos.estocastico import modelo_estocastico
from modelos.continuo import modelo_continuo

from graficas.graficas import (
    graficar_modelos,
    graficar_crecimiento_decrecimiento,
    graficar_influencia_r,
    graficar_replicas_estocasticas,
)

import numpy as np


DATOS = [1000, 1100, 1250, 1400, 1600, 1850, 2100]


def main():

    P0 = DATOS[0]
    r = 0.10
    sigma = 50
    dt = 0.1

    tiempo_datos = len(DATOS) - 1

    t_deterministico, P_deterministico = modelo_deterministico(
        P0,
        r,
        tiempo_datos
    )

    t_discreto, P_discreto = modelo_discreto(
        P0,
        r,
        tiempo_datos
    )

    t_estocastico, P_estocastico = modelo_estocastico(
        P0,
        r,
        sigma,
        tiempo_datos
    )

    t_continuo, P_continuo = modelo_continuo(
        P0,
        r,
        tiempo_datos,
        dt
    )

    graficar_modelos(
        t_deterministico,
        P_deterministico,
        t_discreto,
        P_discreto,
        t_estocastico,
        P_estocastico,
        t_continuo,
        P_continuo,
        DATOS
    )

    tiempo = 20
    r_crecimiento = 0.10
    r_decrecimiento = -0.05

    t_det_crec, P_det_crec = modelo_deterministico(
        P0,
        r_crecimiento,
        tiempo
    )
    t_dis_crec, P_dis_crec = modelo_discreto(
        P0,
        r_crecimiento,
        tiempo
    )
    t_con_crec, P_con_crec = modelo_continuo(
        P0,
        r_crecimiento,
        tiempo,
        dt
    )

    t_det_dec, P_det_dec = modelo_deterministico(
        P0,
        r_decrecimiento,
        tiempo
    )
    t_dis_dec, P_dis_dec = modelo_discreto(
        P0,
        r_decrecimiento,
        tiempo
    )
    t_con_dec, P_con_dec = modelo_continuo(
        P0,
        r_decrecimiento,
        tiempo,
        dt
    )

    graficar_crecimiento_decrecimiento(
        t_det_crec,
        P_det_crec,
        t_dis_crec,
        P_dis_crec,
        t_con_crec,
        P_con_crec,
        t_det_dec,
        P_det_dec,
        t_dis_dec,
        P_dis_dec,
        t_con_dec,
        P_con_dec
    )

    tasas = [0.05, 0.10, 0.20, -0.05]
    curvas = {}

    for tasa in tasas:
        t, P = modelo_deterministico(P0, tasa, tiempo)
        curvas[f"r = {tasa:+.2f}"] = (t, P)

    graficar_influencia_r(curvas)

    replicas = 30
    resultados = []

    for _ in range(replicas):
        _, P = modelo_estocastico(P0, r, sigma, tiempo)
        resultados.append(P)

    t_replicas = list(range(tiempo + 1))
    promedio = np.mean(resultados, axis=0)
    t_det_referencia, P_det_referencia = modelo_deterministico(
        P0,
        r,
        tiempo
    )

    graficar_replicas_estocasticas(
        t_replicas,
        resultados,
        promedio,
        t_det_referencia,
        P_det_referencia
    )


if __name__ == "__main__":
    main()
