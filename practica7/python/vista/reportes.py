"""Construcción de los cuadros estadísticos (Pandas) y exportación a CSV/Markdown."""

import os

import pandas as pd


def _fmt_n(n):
    return f"{n:,}".replace(",", " ")


def tabla_principal(filas_py, df_java):
    """Cuadro pedido en la guía: N | π estimado | Error | Tiempo Python | Tiempo Java."""
    df = pd.DataFrame(filas_py)
    tabla = pd.DataFrame({
        "N": df["n"],
        "π estimado": df["pi"],
        "Error": df["error"],
        "Error relativo (%)": df["error_relativo_pct"],
        "Tiempo Python (s)": df["tiempo_python"],
        "Tiempo Java (s)": df["n"].map(df_java.set_index("n")["tiempo"]) if df_java is not None else None,
        "Tiempo NumPy (s)": df["tiempo_numpy"],
    })
    return tabla


def tabla_python_java(filas_py, df_java):
    """Comparación detallada de ambos programas con los mismos parámetros."""
    py = pd.DataFrame(filas_py).set_index("n")
    ja = df_java.set_index("n")
    tabla = pd.DataFrame({
        "N": py.index,
        "Nc Python": py["dentro"].values,
        "Nc Java": ja.loc[py.index, "dentro"].values,
        "π Python": py["pi"].values,
        "π Java": ja.loc[py.index, "pi"].values,
        "Error Python": py["error"].values,
        "Error Java": ja.loc[py.index, "error"].values,
        "Tiempo Python (s)": py["tiempo_python"].values,
        "Tiempo Java (s)": ja.loc[py.index, "tiempo"].values,
    })
    tabla["¿Mismo resultado?"] = (tabla["Nc Python"] == tabla["Nc Java"]).map({True: "Sí", False: "No"})
    tabla["Java es N veces más rápido"] = tabla["Tiempo Python (s)"] / tabla["Tiempo Java (s)"]
    return tabla


def tabla_secuencias(sec_py, df_sec_java):
    tabla = pd.DataFrame({"i": range(1, len(sec_py) + 1), "U Python": sec_py})
    if df_sec_java is not None:
        tabla["U Java"] = df_sec_java["u"].values[: len(sec_py)]
        tabla["Diferencia"] = (tabla["U Python"] - tabla["U Java"]).abs()
    return tabla


def tabla_generadores(filas_py):
    df = pd.DataFrame(filas_py)
    return pd.DataFrame({
        "N": df["n"],
        "π LCG": df["pi"],
        "Error LCG": df["error"],
        "Tiempo LCG (s)": df["tiempo_python"],
        "π NumPy": df["pi_numpy"],
        "Error NumPy": df["error_numpy"],
        "Tiempo NumPy (s)": df["tiempo_numpy"],
    })


def tabla_semillas(filas_sem):
    df = pd.DataFrame(filas_sem)
    return pd.DataFrame({
        "N": df["n"],
        "Réplicas": df["replicas"],
        "Media π": df["media_pi"],
        "Desviación estándar": df["desviacion"],
        "Error estándar teórico": df["error_estandar_teorico"],
        "Error medio": df["error_medio"],
        "Error máximo": df["error_maximo"],
        "Mínimo": df["minimo"],
        "Máximo": df["maximo"],
    })


def _a_markdown(df, decimales=6):
    cols = list(df.columns)
    lineas = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, fila in df.iterrows():
        celdas = []
        for c in cols:
            v = fila[c]
            if c == "N" or c in ("Nc Python", "Nc Java", "Réplicas", "i"):
                celdas.append(_fmt_n(int(v)))
            elif isinstance(v, float):
                celdas.append("—" if pd.isna(v) else f"{v:.{decimales}f}")
            else:
                celdas.append(str(v))
        lineas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(lineas)


def exportar(cuadros, carpeta):
    """Guarda cada cuadro en CSV y todos juntos en un Markdown para el informe."""
    os.makedirs(carpeta, exist_ok=True)
    partes = ["# Cuadros estadísticos - Práctica 7 (Monte Carlo)\n"]
    for nombre, (titulo, df, dec) in cuadros.items():
        df.to_csv(os.path.join(carpeta, f"{nombre}.csv"), index=False, encoding="utf-8-sig")
        partes.append(f"## {titulo}\n\n{_a_markdown(df, dec)}\n")
    ruta_md = os.path.join(carpeta, "cuadros_estadisticos.md")
    with open(ruta_md, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))
    return ruta_md
