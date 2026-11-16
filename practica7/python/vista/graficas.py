"""Gráficas de la práctica (Matplotlib)."""

import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# Colores por rol (paleta categórica fija: azul, naranja, aqua)
PYTHON = "#2a78d6"
JAVA = "#eb6834"
NUMPY = "#1baf7a"
REFERENCIA = "#52514e"
TEXTO = "#0b0b0b"
GRID = "#e4e3df"
DENTRO = "#2a78d6"
FUERA = "#eb6834"


def _estilo(ax, titulo, xlabel, ylabel):
    ax.set_title(titulo, loc="left", fontsize=12, color=TEXTO, pad=10)
    ax.set_xlabel(xlabel, color=REFERENCIA)
    ax.set_ylabel(ylabel, color=REFERENCIA)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRID)
    ax.tick_params(colors=REFERENCIA)


def _guardar(fig, carpeta, nombre):
    ruta = os.path.join(carpeta, nombre)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def dispersion(x, y, dentro, carpeta):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x[dentro], y[dentro], s=8, color=DENTRO, label=f"Dentro ({dentro.sum()})")
    ax.scatter(x[~dentro], y[~dentro], s=8, color=FUERA, label=f"Fuera ({(~dentro).sum()})")
    t = np.linspace(0, math.pi / 2, 200)
    ax.plot(np.cos(t), np.sin(t), color=TEXTO, linewidth=2)
    ax.set_aspect("equal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    pi_est = 4 * dentro.sum() / len(x)
    _estilo(ax, f"Puntos generados con el LCG (N = {len(x)}, π ≈ {pi_est:.4f})", "x", "y")
    ax.legend(loc="lower left", frameon=True)
    return _guardar(fig, carpeta, "dispersion_puntos.png")


def convergencia(xs, ys, carpeta):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(xs, ys, color=PYTHON, linewidth=2, label="π estimado (acumulado)")
    ax.axhline(math.pi, color=REFERENCIA, linestyle="--", linewidth=1.5, label="π real")
    ax.set_xscale("log")
    _estilo(ax, "Convergencia de la estimación de π", "Número de puntos N (escala log)", "π estimado")
    ax.legend(frameon=False)
    return _guardar(fig, carpeta, "convergencia.png")


def error_vs_n(filas_py, filas_sem, carpeta):
    n = np.array([f["n"] for f in filas_py])
    err = np.array([f["error"] for f in filas_py])
    err_np = np.array([f["error_numpy"] for f in filas_py])
    n_s = np.array([f["n"] for f in filas_sem])
    err_medio = np.array([f["error_medio"] for f in filas_sem])
    teorico = np.array([f["error_estandar_teorico"] for f in filas_sem])

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(n, err, marker="o", markersize=8, linewidth=2, color=PYTHON, label="LCG (Python = Java)")
    ax.plot(n, err_np, marker="s", markersize=8, linewidth=2, color=NUMPY, label="NumPy (semilla única)")
    ax.plot(n_s, err_medio, marker="D", markersize=8, linewidth=2, color=JAVA, label="Error medio (30 semillas)")
    ax.plot(n_s, teorico, linestyle="--", linewidth=1.5, color=REFERENCIA, label="Error estándar teórico ∝ 1/√N")
    ax.set_xscale("log")
    ax.set_yscale("log")
    _estilo(ax, "Error absoluto frente al tamaño de muestra", "N (escala log)", "Error absoluto |π̂ − π| (escala log)")
    ax.legend(frameon=False)
    return _guardar(fig, carpeta, "error_vs_n.png")


def tiempos(tabla, carpeta):
    """Barras agrupadas de tiempo por lenguaje (escala log)."""
    etiquetas = [f"{n:,}".replace(",", " ") for n in tabla["N"]]
    series = [("Python (LCG)", "Tiempo Python (s)", PYTHON),
              ("Java (LCG)", "Tiempo Java (s)", JAVA),
              ("Python + NumPy", "Tiempo NumPy (s)", NUMPY)]
    series = [s for s in series if s[1] in tabla.columns and tabla[s[1]].notna().all()]

    x = np.arange(len(etiquetas))
    ancho = 0.8 / len(series)
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, (nombre, col, color) in enumerate(series):
        ax.bar(x + (i - (len(series) - 1) / 2) * ancho, tabla[col], ancho * 0.92,
               color=color, label=nombre)
    ax.set_xticks(x, etiquetas)
    ax.set_yscale("log")
    _estilo(ax, "Tiempo de ejecución por tamaño de muestra", "N", "Tiempo (s, escala log)")
    ax.legend(frameon=False)
    return _guardar(fig, carpeta, "tiempos.png")


def distribucion_semillas(estimaciones, carpeta):
    fig, ax = plt.subplots(figsize=(9, 5))
    tamanos = list(estimaciones.keys())
    ax.boxplot([estimaciones[n] for n in tamanos],
               tick_labels=[f"{n:,}".replace(",", " ") for n in tamanos],
               patch_artist=True,
               boxprops={"facecolor": "#cfe0f5", "edgecolor": PYTHON},
               medianprops={"color": PYTHON, "linewidth": 2},
               whiskerprops={"color": PYTHON}, capprops={"color": PYTHON},
               flierprops={"markeredgecolor": PYTHON})
    ax.axhline(math.pi, color=REFERENCIA, linestyle="--", linewidth=1.5, label="π real")
    _estilo(ax, "Dispersión de π estimado con 30 semillas distintas", "N", "π estimado")
    ax.legend(frameon=False)
    return _guardar(fig, carpeta, "dispersion_semillas.png")
