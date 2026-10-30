"""Vista de consola de la practica 5."""

from __future__ import annotations

from typing import Any, Sequence

from model.lcg import ResultadoGeneracion


def mostrar_encabezado(config: dict[str, Any]) -> None:
    print("=" * 78)
    print("PRACTICA 5 - GENERADOR CONGRUENCIAL LINEAL (LCG)")
    print("=" * 78)
    print(f"a = {config['a']:,}")
    print(f"c = {config['c']:,}")
    print(f"m = 2^32 = {config['m']:,}")
    print(f"Semilla principal = {config['semilla']}")
    print(f"Semilla alternativa = {config['semilla_alternativa']}")
    print(f"Cantidad de valores = {config['cantidad']:,}")
    print()


def mostrar_primeros_20(resultado: ResultadoGeneracion) -> None:
    print("-" * 78)
    print("PRIMEROS 20 VALORES EN PYTHON")
    print("-" * 78)
    print(f"{'n':>3}  {'estado':>12}  {'u_n':>14}")
    for indice, estado, normalizado in resultado.primeros(20):
        print(f"{indice:>3}  {estado:>12}  {normalizado:>14.10f}")
    print()


def mostrar_estadisticas(estadisticas: dict[str, Any]) -> None:
    print("-" * 78)
    print("ESTADISTICAS DESCRIPTIVAS")
    print("-" * 78)
    print(f"Cantidad:              {estadisticas['cantidad']:,}")
    print(f"Media:                 {estadisticas['media']:.8f}")
    print(f"Desviacion estandar:   {estadisticas['desviacion_estandar']:.8f}")
    print(f"Minimo:                {estadisticas['minimo']:.10f}")
    print(f"Maximo:                {estadisticas['maximo']:.10f}")
    print(f"Correlacion lag 1:     {estadisticas['correlacion_lag1']:.8f}")
    print("Frecuencias por decil:")
    for indice, frecuencia in enumerate(estadisticas["frecuencias_bins"], start=1):
        limite_inferior = (indice - 1) / estadisticas["bins"]
        limite_superior = indice / estadisticas["bins"]
        print(
            f"  [{limite_inferior:.1f}, {limite_superior:.1f}): "
            f"{frecuencia:>6,}"
        )
    print()


def mostrar_periodo(periodo: dict[str, Any]) -> None:
    teorico = periodo["teorico"]
    toy = periodo["toy"]
    print("-" * 78)
    print("ANALISIS DEL PERIODO")
    print("-" * 78)
    print(f"Factores primos de m: {teorico['factores_primos_m']}")
    print("Condiciones de Hull-Dobell:")
    for condicion in teorico["condiciones"]:
        estado = "cumple" if condicion["cumple"] else "no cumple"
        print(f"  - {condicion['nombre']}: {estado}")
    print(
        "Periodo completo teorico: "
        f"{'si' if teorico['periodo_completo'] else 'no'}"
    )
    print(f"Periodo maximo teorico: {teorico['periodo_maximo_teorico']:,}")
    print(
        "Sin repeticion en la muestra: "
        f"{'si' if periodo['sin_repeticion_en_muestra'] else 'no'} "
        f"({periodo['cantidad_muestra']:,} valores)"
    )
    if toy["encontrado"]:
        print(
            "Prueba con LCG pequeno (a=5, c=3, m=16, semilla=1): "
            f"mu={toy['mu']}, lambda={toy['lambda']}"
        )
    else:
        print("No se detecto el ciclo en la prueba pequena")
    print()


def mostrar_comparacion_semillas(
    principal: ResultadoGeneracion,
    alternativa: ResultadoGeneracion,
    filas: Sequence[dict[str, Any]],
) -> None:
    print("-" * 78)
    print("COMPARACION DE SEMILLAS")
    print("-" * 78)
    print(
        f"{'n':>3}  {'u_' + str(principal.parametros.semilla):>14}  "
        f"{'u_' + str(alternativa.parametros.semilla):>14}  {'|dif|':>14}"
    )
    for fila in filas[:20]:
        print(
            f"{fila['n']:>3}  {fila['u_principal']:>14.10f}  "
            f"{fila['u_alternativa']:>14.10f}  {fila['diferencia']:>14.10f}"
        )
    print(
        "La semilla alternativa aparece en la muestra principal: "
        f"{'si' if alternativa.parametros.semilla in set(principal.estados) else 'no'}"
    )
    print()


def mostrar_comparacion_java(comparacion: dict[str, Any]) -> None:
    print("-" * 78)
    print("COMPARACION PYTHON vs JAVA")
    print("-" * 78)
    if not comparacion.get("disponible"):
        print(f"Comparacion no disponible: {comparacion.get('error', 'error desconocido')}")
        print()
        return

    print(
        f"{'n':>3}  {'Python estado':>13}  {'Java estado':>13}  "
        f"{'Python u':>14}  {'Java u':>14}  {'Coincide':>8}"
    )
    for fila in comparacion["filas"]:
        print(
            f"{fila['n']:>3}  {fila['python_estado']:>13}  "
            f"{fila['java_estado']:>13}  {fila['python_u']:>14.10f}  "
            f"{fila['java_u']:>14.10f}  "
            f"{'si' if fila['coincide'] else 'no':>8}"
        )
    print(
        f"Filas comparadas: {comparacion['total']:,} | "
        f"diferencias: {comparacion['diferencias']:,} | "
        f"coinciden todos: {'si' if comparacion['coinciden_todos'] else 'no'}"
    )
    print()


def mostrar_resumen(rutas: dict[str, Any]) -> None:
    print("-" * 78)
    print("ARCHIVOS GENERADOS")
    print("-" * 78)
    for nombre, ruta in rutas.items():
        print(f"  {nombre}: {ruta}")
    print()


def mostrar_conclusiones() -> None:
    print("-" * 78)
    print("CONCLUSIONES")
    print("-" * 78)
    print("1. Python y Java producen la misma secuencia cuando usan long y mascara")
    print("   de 32 bits en Java.")
    print("2. La secuencia normalizada cae en [0, 1) y su media se aproxima a 0.5.")
    print("3. La correlacion lag 1 es cercana a cero, sin patron lineal evidente.")
    print("4. Con a=1664525, c=1013904223 y m=2^32 se cumple Hull-Dobell.")
    print("5. Cambiar la semilla produce otra ventana de la misma secuencia.")
    print()
