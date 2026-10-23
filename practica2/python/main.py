from modelos.deterministico import modelo_deterministico
from modelos.discreto import modelo_discreto
from modelos.estocastico import modelo_estocastico
from modelos.continuo import modelo_continuo

from graficas.graficas import graficar_modelos


def main():

    # Parámetros
    P0 = 1000
    r = 0.10
    sigma = 50
    tiempo = 20
    dt = 0.1

    # Modelo determinístico

    t_deterministico, P_deterministico = modelo_deterministico(
        P0,
        r,
        tiempo
    )

    # Modelo discreto
    t_discreto, P_discreto = modelo_discreto(
        P0,
        r,
        tiempo
    )

    # Modelo estocástico
    t_estocastico, P_estocastico = modelo_estocastico(
        P0,
        r,
        sigma,
        tiempo
    )

    # Modelo continuo mediante Euler
    t_continuo, P_continuo = modelo_continuo(
        P0,
        r,
        tiempo,
        dt
    )

    # Mostrar resultados
    graficar_modelos(
        t_deterministico,
        P_deterministico,
        t_discreto,
        P_discreto,
        t_estocastico,
        P_estocastico,
        t_continuo,
        P_continuo
    )


if __name__ == "__main__":
    main()