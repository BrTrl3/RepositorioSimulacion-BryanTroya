"""Vista grafica de la practica 6."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

AZUL = "#2a78d6"
NARANJA = "#eb6834"
TEXTO = "#0b0b0b"
TEXTO_SECUNDARIO = "#52514e"
REJILLA = "#e4e3df"
FONDO = "#fcfcfb"

plt.rcParams.update(
    {
        "figure.facecolor": FONDO,
        "axes.facecolor": FONDO,
        "axes.edgecolor": REJILLA,
        "axes.labelcolor": TEXTO_SECUNDARIO,
        "axes.titlecolor": TEXTO,
        "axes.titlesize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": REJILLA,
        "grid.linewidth": 0.8,
        "xtick.color": TEXTO_SECUNDARIO,
        "ytick.color": TEXTO_SECUNDARIO,
        "legend.frameon": False,
        "lines.linewidth": 2,
    }
)


def _guardar(figura: Any, ruta: Path) -> Path:
    figura.tight_layout()
    figura.savefig(ruta, dpi=150)
    plt.close(figura)
    return ruta


def _distribucion_empirica(valores: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ordenados = np.sort(valores)
    return ordenados, np.arange(1, len(ordenados) + 1) / len(ordenados)


def graficar_frecuencias(evaluacion: dict[str, Any], ruta: Path) -> Path:
    chi = evaluacion["chi"]
    intervalos = len(chi["observadas"])
    ancho = 1 / intervalos
    centros = (np.arange(intervalos) + 0.5) * ancho

    figura, eje = plt.subplots(figsize=(8, 4.5))
    eje.bar(centros, chi["observadas"], width=ancho * 0.9, color=AZUL, label="Observada")
    eje.axhline(chi["esperada"], color=NARANJA, label=f"Esperada = {chi['esperada']:.0f}")
    eje.set_title(
        f"Frecuencias por intervalo: chi2 = {chi['estadistico']:.3f}, "
        f"p = {chi['valor_p']:.4f}"
    )
    eje.set_xlabel("Intervalo de u")
    eje.set_ylabel("Frecuencia")
    eje.set_xticks(np.arange(intervalos + 1) * ancho)
    eje.grid(axis="x", visible=False)
    eje.set_ylim(0, max(chi["observadas"]) * 1.2)
    eje.legend(loc="upper right", ncols=2)
    return _guardar(figura, ruta)


def graficar_kolmogorov_smirnov(evaluacion: dict[str, Any], ruta: Path) -> Path:
    ks = evaluacion["ks"]
    x, empirica = _distribucion_empirica(evaluacion["resultado"].normalizados)

    figura, (izquierda, derecha) = plt.subplots(1, 2, figsize=(11, 4.5))
    izquierda.plot([0, 1], [0, 1], color=NARANJA, label="F(x) teorica")
    izquierda.step(x, empirica, where="post", color=AZUL, linewidth=1.2, label="Fn(x) empirica")
    izquierda.set_title("Distribucion acumulada")
    izquierda.set_xlabel("x")
    izquierda.set_ylabel("Probabilidad acumulada")
    izquierda.legend(loc="upper left")

    diferencia = empirica - x
    indice = int(np.argmax(np.abs(diferencia)))
    derecha.axhline(0, color=TEXTO_SECUNDARIO, linewidth=1)
    derecha.plot(x, diferencia, color=AZUL, linewidth=1.2)
    derecha.scatter([x[indice]], [diferencia[indice]], s=45, color=NARANJA, zorder=3)
    derecha.annotate(
        f"D = {ks['estadistico']:.5f}",
        (x[indice], diferencia[indice]),
        xytext=(8, 8),
        textcoords="offset points",
        color=TEXTO,
    )
    derecha.margins(y=0.15)
    derecha.set_title(f"Diferencia Fn(x) - F(x), p = {ks['valor_p']:.4f}")
    derecha.set_xlabel("x")
    derecha.set_ylabel("Diferencia")
    return _guardar(figura, ruta)


def graficar_configuraciones(evaluaciones: list[dict[str, Any]], ruta: Path) -> Path:
    columnas = 3
    filas = (len(evaluaciones) + columnas - 1) // columnas
    figura, ejes = plt.subplots(
        filas, columnas, figsize=(11, 3.5 * filas), sharex=True, sharey=True
    )
    for eje, evaluacion in zip(ejes.flat, evaluaciones):
        x, empirica = _distribucion_empirica(evaluacion["resultado"].normalizados)
        eje.plot([0, 1], [0, 1], color=NARANJA, label="F(x) teorica")
        eje.step(x, empirica, where="post", color=AZUL, linewidth=1.2, label="Fn(x) empirica")
        eje.set_title(
            f"{evaluacion['resultado'].configuracion.nombre}\n"
            f"D = {evaluacion['ks']['estadistico']:.4f}, "
            f"p KS = {evaluacion['ks']['valor_p']:.4f}",
            fontsize=10,
        )
        eje.set_xlim(0, 1)
    ejes.flat[0].legend(loc="upper left", fontsize=8)
    figura.supxlabel("x", color=TEXTO_SECUNDARIO)
    figura.supylabel("Probabilidad acumulada", color=TEXTO_SECUNDARIO)
    return _guardar(figura, ruta)


def graficar_pi(filas: list[dict[str, Any]], ruta: Path) -> Path:
    tamanos = [fila["n"] for fila in filas]
    figura, (izquierda, derecha) = plt.subplots(1, 2, figsize=(11, 4.5))

    izquierda.plot(tamanos, [fila["error"] for fila in filas], color=AZUL, marker="o")
    izquierda.set_xscale("log")
    izquierda.set_yscale("log")
    izquierda.set_title("Error absoluto de pi estimado")
    izquierda.set_xlabel("N (puntos)")
    izquierda.set_ylabel("Error")

    derecha.plot(
        tamanos,
        [fila["tiempo_python"] for fila in filas],
        color=AZUL,
        marker="o",
        label="Python",
    )
    if all(fila["tiempo_java"] is not None for fila in filas):
        derecha.plot(
            tamanos,
            [fila["tiempo_java"] for fila in filas],
            color=NARANJA,
            marker="s",
            label="Java",
        )
    derecha.set_xscale("log")
    derecha.set_yscale("log")
    derecha.set_title("Tiempo de ejecucion")
    derecha.set_xlabel("N (puntos)")
    derecha.set_ylabel("Segundos")
    derecha.legend(loc="upper left")
    return _guardar(figura, ruta)


def generar_graficas(datos: dict[str, Any]) -> dict[str, Path]:
    directorio = Path(datos["directorio_salida"])
    principal = datos["evaluaciones"][0]
    return {
        "grafica_frecuencias": graficar_frecuencias(principal, directorio / "frecuencias.png"),
        "grafica_ks": graficar_kolmogorov_smirnov(principal, directorio / "ks_acumulada.png"),
        "grafica_configuraciones": graficar_configuraciones(
            datos["evaluaciones"], directorio / "configuraciones.png"
        ),
        "grafica_pi": graficar_pi(datos["pi"], directorio / "pi.png"),
    }
