"""Controlador: ejecuta el experimento, invoca Java (opcional) y genera cuadros y gráficas."""

import os
import shutil
import subprocess

import pandas as pd

from python.modelo import montecarlo as mc
from python.modelo.lcg import LCG
from python.vista import consola, graficas, reportes

TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
SEMILLAS_REPLICAS = list(range(1, 31))  # 30 semillas para el análisis de variabilidad

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA_RESULTADOS = os.path.join(RAIZ, "resultados")
CARPETA_JAVA = os.path.join(CARPETA_RESULTADOS, "java")
CARPETA_GRAFICAS = os.path.join(CARPETA_RESULTADOS, "graficas")


def ejecutar_java(semilla, repeticiones):
    """Compila y ejecuta la versión Java con los mismos parámetros."""
    if not shutil.which("javac") or not shutil.which("java"):
        consola.mensaje("[!] No se encontró javac/java en el PATH; se usará el CSV existente.")
        return
    src = os.path.join(RAIZ, "java", "src")
    out = os.path.join(RAIZ, "java", "out")
    fuentes = [os.path.join(d, f) for d, _, fs in os.walk(src) for f in fs if f.endswith(".java")]
    consola.mensaje("Compilando y ejecutando la versión Java...")
    subprocess.run(["javac", "-encoding", "UTF-8", "-d", out, *fuentes], check=True)
    subprocess.run(["java", "-cp", out, "Main", str(semilla), str(repeticiones), CARPETA_JAVA],
                   check=True)
    print()


def _leer_csv(nombre):
    ruta = os.path.join(CARPETA_JAVA, nombre)
    return pd.read_csv(ruta) if os.path.exists(ruta) else None


def ejecutar(semilla, repeticiones, con_java):
    os.makedirs(CARPETA_GRAFICAS, exist_ok=True)
    if con_java:
        ejecutar_java(semilla, repeticiones)

    consola.encabezado(semilla, repeticiones, mc.PARAMETROS_LCG)

    # 1. Experimento principal (LCG propio y NumPy)
    filas_py = mc.experimento(TAMANOS, semilla, repeticiones)

    # 2. Variabilidad con 30 semillas
    filas_sem, estimaciones = mc.experimento_semillas(TAMANOS, SEMILLAS_REPLICAS)

    # 3. Secuencia generada (verificación Python vs Java)
    gen = LCG(semilla)
    sec_py = [gen.siguiente() for _ in range(10)]

    df_java = _leer_csv("pi_java.csv")
    df_sec_java = _leer_csv("secuencia_java.csv")
    if df_java is None:
        consola.mensaje("[!] No hay resultados de Java. Ejecute con --java o corra Main.java primero.\n")

    cuadros = {
        "tabla_principal": ("Cuadro 1. Resultados por tamaño de muestra (formato de la guía)",
                            reportes.tabla_principal(filas_py, df_java), 6),
        "secuencia_python_java": ("Cuadro 2. Primeros 10 números U generados (misma semilla)",
                                  reportes.tabla_secuencias(sec_py, df_sec_java), 10),
    }
    if df_java is not None:
        cuadros["comparacion_python_java"] = ("Cuadro 3. Comparación Python vs Java",
                                              reportes.tabla_python_java(filas_py, df_java), 6)
    cuadros["comparacion_generadores"] = ("Cuadro 4. LCG propio vs generador de NumPy",
                                          reportes.tabla_generadores(filas_py), 6)
    cuadros["estadisticas_semillas"] = ("Cuadro 5. Variabilidad del estimador con 30 semillas",
                                        reportes.tabla_semillas(filas_sem), 6)

    for titulo, df, _ in cuadros.values():
        consola.cuadro(titulo, df)

    ruta_md = reportes.exportar(cuadros, CARPETA_RESULTADOS)

    # Gráficas
    x, y, dentro = mc.muestra_puntos(1_000, semilla)
    xs, ys = mc.convergencia(1_000_000, semilla)
    rutas = [
        graficas.dispersion(x, y, dentro, CARPETA_GRAFICAS),
        graficas.convergencia(xs, ys, CARPETA_GRAFICAS),
        graficas.error_vs_n(filas_py, filas_sem, CARPETA_GRAFICAS),
        graficas.tiempos(cuadros["tabla_principal"][1], CARPETA_GRAFICAS),
        graficas.distribucion_semillas(estimaciones, CARPETA_GRAFICAS),
    ]

    consola.mensaje(f"Cuadros guardados en: {CARPETA_RESULTADOS} (CSV y {os.path.basename(ruta_md)})")
    consola.mensaje("Gráficas generadas:")
    for r in rutas:
        consola.mensaje(f"  - {os.path.relpath(r, RAIZ)}")
