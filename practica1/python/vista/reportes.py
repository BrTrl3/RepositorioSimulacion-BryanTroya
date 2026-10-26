# reportes.py

import csv
from pathlib import Path


DIRECTORIO_RESULTADOS = (
    Path(__file__).resolve().parents[2] / "resultados"
)


def guardar_resultados(resultados):
    """
    Guarda la tabla de resultados en formato CSV.
    """

    DIRECTORIO_RESULTADOS.mkdir(exist_ok=True)

    ruta = DIRECTORIO_RESULTADOS / "tabla_resultados.csv"

    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow([
            "Hora",
            "Humedad (%)",
            "Nubosidad (%)",
            "Temperatura (C)",
            "H",
            "N",
            "Tf",
            "Indice original",
            "Estado original",
            "Indice ajustado",
            "Estado ajustado",
        ])

        for i, hora in enumerate(resultados["horas"]):

            escritor.writerow([
                hora,
                resultados["humedad"][i],
                resultados["nubosidad"][i],
                resultados["temperatura"][i],
                f'{resultados["H"][i]:.4f}',
                f'{resultados["N"][i]:.4f}',
                f'{resultados["Tf"][i]:.4f}',
                f'{resultados["indice_original"][i]:.4f}',
                resultados["estado_original"][i],
                f'{resultados["indice_ajustado"][i]:.4f}',
                resultados["estado_ajustado"][i],
            ])

    return ruta
