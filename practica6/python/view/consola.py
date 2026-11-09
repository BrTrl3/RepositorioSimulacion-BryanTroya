"""Vista de consola de la practica 6."""

from __future__ import annotations

from typing import Any, Sequence

from model.lcg import ResultadoGeneracion


def _titulo(texto: str) -> None:
    print("-" * 78)
    print(texto)
    print("-" * 78)


def mostrar_encabezado(datos: dict[str, Any]) -> None:
    print("=" * 78)
    print("PRACTICA 6 - VALIDACION ESTADISTICA DE NUMEROS PSEUDOALEATORIOS")
    print("=" * 78)
    print("H0: X ~ U(0,1)   H1: X no sigue U(0,1)   alfa = 0.05")
    print(f"Cantidad de valores = {datos['cantidad']:,}")
    print(f"Intervalos Chi-cuadrado = {datos['intervalos']}")
    print()


def mostrar_secuencia(resultado: ResultadoGeneracion) -> None:
    _titulo(f"PRIMEROS 20 VALORES ({resultado.configuracion.nombre})")
    print(f"{'n':>3}  {'estado':>12}  {'u_n':>14}")
    for indice in range(min(20, resultado.cantidad)):
        print(
            f"{indice + 1:>3}  {resultado.estados[indice]:>12}  "
            f"{resultado.normalizados[indice]:>14.10f}"
        )
    print()


def mostrar_chi_cuadrado(evaluacion: dict[str, Any]) -> None:
    chi = evaluacion["chi"]
    _titulo(f"PRUEBA CHI-CUADRADO ({evaluacion['resultado'].configuracion.nombre})")
    intervalos = len(chi["observadas"])
    print(f"{'Intervalo':<14}  {'Observada':>9}  {'Esperada':>9}")
    for indice, observada in enumerate(chi["observadas"]):
        rango = f"[{indice / intervalos:.2f}, {(indice + 1) / intervalos:.2f})"
        print(f"{rango:<14}  {observada:>9}  {chi['esperada']:>9.1f}")
    print(f"Estadistico Chi-cuadrado: {chi['estadistico']:.6f}")
    print(f"Grados de libertad:       {chi['grados_libertad']}")
    print(f"Valor p:                  {chi['valor_p']:.6f}")
    print(f"Decision:                 {chi['decision']}")
    print()


def mostrar_kolmogorov_smirnov(evaluacion: dict[str, Any]) -> None:
    ks = evaluacion["ks"]
    _titulo(f"PRUEBA KOLMOGOROV-SMIRNOV ({evaluacion['resultado'].configuracion.nombre})")
    print(f"D+ (diferencia positiva): {ks['d_positiva']:.6f}")
    print(f"D- (diferencia negativa): {ks['d_negativa']:.6f}")
    print(f"Estadistico D:            {ks['estadistico']:.6f}")
    print(f"Valor p:                  {ks['valor_p']:.6f}")
    print(f"Decision:                 {ks['decision']}")
    print()


def mostrar_configuraciones(evaluaciones: Sequence[dict[str, Any]]) -> None:
    _titulo("COMPARACION DE CONFIGURACIONES DEL GENERADOR")
    print(f"{'Configuracion':<20} {'Chi2':>13} {'p':>8} {'D':>8} {'p':>8}  Decision Chi2 / KS")
    for evaluacion in evaluaciones:
        chi, ks = evaluacion["chi"], evaluacion["ks"]
        print(
            f"{evaluacion['resultado'].configuracion.nombre:<20} "
            f"{chi['estadistico']:>13.4f} {chi['valor_p']:>8.4f} "
            f"{ks['estadistico']:>8.4f} {ks['valor_p']:>8.4f}  "
            f"{chi['decision']} / {ks['decision']}"
        )
    print()


def mostrar_comparacion_java(java: dict[str, Any]) -> None:
    _titulo("COMPARACION PYTHON vs JAVA")
    if not java["disponible"]:
        print(f"Comparacion no disponible: {java['error']}")
        print()
        return

    print(
        f"{'n':>3}  {'Python estado':>13}  {'Java estado':>13}  "
        f"{'Python u':>14}  {'Java u':>14}  {'Coincide':>8}"
    )
    for fila in java["secuencias"][0]["filas"]:
        print(
            f"{fila['n']:>3}  {fila['python_estado']:>13}  {fila['java_estado']:>13}  "
            f"{fila['python_u']:>14.10f}  {fila['java_u']:>14.10f}  "
            f"{'si' if fila['coincide'] else 'no':>8}"
        )
    print()
    print(f"{'Configuracion':<20} {'Filas':>7} {'Diferencias':>12} {'Pruebas iguales':>16}")
    for secuencia, prueba in zip(java["secuencias"], java["pruebas"]):
        print(
            f"{secuencia['configuracion']:<20} {secuencia['total']:>7} "
            f"{secuencia['diferencias']:>12} "
            f"{'si' if prueba['coincide'] else 'no':>16}"
        )
    print()


def mostrar_pi(filas: Sequence[dict[str, Any]]) -> None:
    _titulo("ESTIMACION DE PI CON EL LCG")
    print(
        f"{'N':>9}  {'pi estimado':>12}  {'Error':>10}  "
        f"{'Tiempo Python':>14}  {'Tiempo Java':>12}"
    )
    for fila in filas:
        tiempo_java = (
            f"{fila['tiempo_java']:.6f} s" if fila["tiempo_java"] is not None else "-"
        )
        print(
            f"{fila['n']:>9}  {fila['pi']:>12.6f}  {fila['error']:>10.6f}  "
            f"{fila['tiempo_python']:>12.6f} s  {tiempo_java:>12}"
        )
    print()


def mostrar_archivos(rutas: dict[str, Any]) -> None:
    _titulo("ARCHIVOS GENERADOS")
    for nombre, ruta in rutas.items():
        print(f"  {nombre}: {ruta}")
    print()
