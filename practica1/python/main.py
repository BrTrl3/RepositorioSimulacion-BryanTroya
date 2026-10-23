# main.py

from python.controlador.controlador import ejecutar_modelo
from python.vista.graficas import graficar_indices
from python.modelo.datos import HORAS


def main():

    indices_originales, indices_ajustados = ejecutar_modelo()

    print("\nGenerando gráfica...")

    graficar_indices(
        HORAS,
        indices_originales,
        indices_ajustados
    )


if __name__ == "__main__":
    main()