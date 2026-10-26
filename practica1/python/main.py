# main.py

from python.controlador.controlador import ejecutar_modelo
from python.vista.graficas import generar_graficas
from python.vista.reportes import guardar_resultados


def main():

    resultados = ejecutar_modelo()

    print("\nGenerando graficas y archivo de resultados...")

    rutas = generar_graficas(resultados)
    rutas.append(guardar_resultados(resultados))

    print("\nArchivos generados:")
    for ruta in rutas:
        print(f"  - {ruta}")


if __name__ == "__main__":
    main()
