# vista.py


def mostrar_titulo():
    print("=" * 120)
    print("MODELO DE POSIBILIDAD DE LLUVIA")
    print("=" * 120)


def mostrar_pesos(
    peso_humedad,
    peso_nubosidad,
    peso_temperatura
):
    print("\nPESOS DEL MODELO")
    print("-" * 40)

    print("Modelo original:")
    print("Humedad = 0.50")
    print("Nubosidad = 0.30")
    print("Temperatura = 0.20")

    print("\nAjuste aleatorio:")
    print(f"Humedad = {peso_humedad:.4f}")
    print(f"Nubosidad = {peso_nubosidad:.4f}")
    print(f"Temperatura = {peso_temperatura:.4f}")


def mostrar_suma_pesos(suma):
    print(f"\nSuma de pesos ajustados: {suma:.4f}")


def mostrar_encabezado_tabla():
    print("\n")
    print("=" * 120)
    print("RESULTADOS")
    print("=" * 120)

    print(
        f"{'Hora':<8}"
        f"{'H (%)':<8}"
        f"{'N (%)':<8}"
        f"{'Temp.':<8}"
        f"{'Tf':<8}"
        f"{'I original':<15}"
        f"{'Estado original':<20}"
        f"{'I ajustado':<15}"
        f"{'Estado ajustado':<20}"
    )

    print("-" * 120)


def mostrar_fila(
    hora,
    humedad,
    nubosidad,
    temperatura,
    Tf,
    indice_original,
    estado_original,
    indice_ajustado,
    estado_ajustado
):
    print(
        f"{hora:<8}"
        f"{humedad:<8}"
        f"{nubosidad:<8}"
        f"{temperatura:<8}"
        f"{Tf:<8.2f}"
        f"{indice_original:<15.2f}"
        f"{estado_original:<20}"
        f"{indice_ajustado:<15.2f}"
        f"{estado_ajustado:<20}"
    )


def mostrar_fin_tabla():
    print("=" * 120)