# vista.py


ANCHO = 140


def mostrar_titulo():
    print("=" * ANCHO)
    print("MODELO DE POSIBILIDAD DE LLUVIA")
    print("=" * ANCHO)


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
    print("=" * ANCHO)
    print("RESULTADOS")
    print("=" * ANCHO)

    print(
        f"{'Hora':<8}"
        f"{'Humedad (%)':<12}"
        f"{'Nubosidad (%)':<14}"
        f"{'Temp. (C)':<10}"
        f"{'H':<10}"
        f"{'N':<10}"
        f"{'Tf':<10}"
        f"{'I original':<12}"
        f"{'Estado original':<20}"
        f"{'I ajustado':<12}"
        f"{'Estado ajustado':<20}"
    )

    print("-" * ANCHO)


def mostrar_fila(
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
):
    print(
        f"{hora:<8}"
        f"{humedad:<12}"
        f"{nubosidad:<14}"
        f"{temperatura:<10}"
        f"{H:<10.2f}"
        f"{N:<10.2f}"
        f"{Tf:<10.2f}"
        f"{indice_original:<12.4f}"
        f"{estado_original:<20}"
        f"{indice_ajustado:<12.4f}"
        f"{estado_ajustado:<20}"
    )


def mostrar_fin_tabla():
    print("=" * ANCHO)