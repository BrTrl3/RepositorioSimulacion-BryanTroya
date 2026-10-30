"""Vista grafica de la practica 5."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from model.lcg import ResultadoGeneracion


def _guardar(figura: Any, ruta: Path | str) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(ruta, dpi=150)
    plt.close(figura)
    return ruta


def graficar_secuencia(
    resultado: ResultadoGeneracion,
    ruta: Path | str,
    limite: int = 300,
) -> Path:
    valores = resultado.normalizados[:limite]
    figura, eje = plt.subplots(figsize=(9, 4))
    eje.plot(
        range(1, len(valores) + 1),
        valores,
        color="#1f77b4",
        linewidth=0.8,
    )
    eje.set_title(f"Secuencia LCG con semilla {resultado.parametros.semilla}")
    eje.set_xlabel("n")
    eje.set_ylabel("u_n")
    eje.set_ylim(-0.02, 1.02)
    eje.grid(alpha=0.3)
    return _guardar(figura, ruta)


def graficar_dispersion(
    resultado: ResultadoGeneracion,
    ruta: Path | str,
) -> Path:
    x = resultado.normalizados[:-1]
    y = resultado.normalizados[1:]
    figura, eje = plt.subplots(figsize=(5, 5))
    eje.scatter(x, y, s=3, alpha=0.45, color="#2ca02c")
    eje.set_title("Pares consecutivos (u_n, u_n+1)")
    eje.set_xlabel("u_n")
    eje.set_ylabel("u_n+1")
    eje.set_xlim(0, 1)
    eje.set_ylim(0, 1)
    eje.grid(alpha=0.3)
    return _guardar(figura, ruta)


def graficar_histograma(
    resultado: ResultadoGeneracion,
    ruta: Path | str,
    bins: int = 20,
) -> Path:
    figura, eje = plt.subplots(figsize=(8, 4.5))
    eje.hist(
        resultado.normalizados,
        bins=bins,
        color="#ff7f0e",
        edgecolor="black",
        alpha=0.75,
    )
    media = sum(resultado.normalizados) / len(resultado.normalizados)
    eje.axvline(media, color="#d62728", linestyle="--", label=f"Media = {media:.5f}")
    eje.set_title(f"Histograma de {resultado.cantidad} valores normalizados")
    eje.set_xlabel("u_n")
    eje.set_ylabel("Frecuencia")
    eje.legend()
    eje.grid(alpha=0.3)
    return _guardar(figura, ruta)


def graficar_comparacion_semillas(
    principal: ResultadoGeneracion,
    alternativa: ResultadoGeneracion,
    ruta: Path | str,
    limite: int = 100,
) -> Path:
    figura, eje = plt.subplots(figsize=(9, 4))
    eje.plot(
        range(1, limite + 1),
        principal.normalizados[:limite],
        label=f"Semilla {principal.parametros.semilla}",
        linewidth=0.9,
    )
    eje.plot(
        range(1, limite + 1),
        alternativa.normalizados[:limite],
        label=f"Semilla {alternativa.parametros.semilla}",
        linewidth=0.9,
        alpha=0.8,
    )
    eje.set_title("Comparacion de las primeras 100 salidas con dos semillas")
    eje.set_xlabel("n")
    eje.set_ylabel("u_n")
    eje.set_ylim(-0.02, 1.02)
    eje.legend()
    eje.grid(alpha=0.3)
    return _guardar(figura, ruta)


def generar_graficas(
    principal: ResultadoGeneracion,
    alternativa: ResultadoGeneracion,
    directorio: Path | str,
) -> dict[str, Path]:
    directorio = Path(directorio)
    return {
        "grafica_secuencia": graficar_secuencia(
            principal, directorio / "secuencia.png"
        ),
        "grafica_dispersion": graficar_dispersion(
            principal, directorio / "dispersion.png"
        ),
        "grafica_histograma": graficar_histograma(
            principal, directorio / "histograma.png"
        ),
        "grafica_semillas": graficar_comparacion_semillas(
            principal, alternativa, directorio / "comparacion_semillas.png"
        ),
    }
