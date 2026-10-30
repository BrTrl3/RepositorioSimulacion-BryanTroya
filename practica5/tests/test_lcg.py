from __future__ import annotations

import csv
import math
import tempfile
import unittest
from pathlib import Path

from controller import lcg_controller
from model import analysis
from model.lcg import A, C, M, ParametrosLCG, generar_secuencia
from view import reportes

PRIMEROS_20 = [
    87628868,
    71072467,
    2332836374,
    2726892157,
    3908547000,
    483019191,
    2129828778,
    2355140353,
    2560230508,
    3364893915,
    171172990,
    3194601925,
    4148119648,
    316399679,
    3004788882,
    1976948425,
    1702883732,
    4121112547,
    1744294886,
    4092090893,
]


class TestLCG(unittest.TestCase):
    def test_primeros_20_valores(self) -> None:
        resultado = generar_secuencia(semilla=12345, cantidad=20)
        self.assertEqual(resultado.estados, PRIMEROS_20)

    def test_normalizados_en_rango(self) -> None:
        resultado = generar_secuencia(semilla=12345, cantidad=1000)
        self.assertTrue(all(0.0 <= valor < 1.0 for valor in resultado.normalizados))
        for estado, normalizado in zip(resultado.estados, resultado.normalizados):
            self.assertEqual(normalizado, estado / M)

    def test_reproducibilidad(self) -> None:
        primero = generar_secuencia(semilla=12345, cantidad=100)
        segundo = generar_secuencia(semilla=12345, cantidad=100)
        self.assertEqual(primero.estados, segundo.estados)

    def test_semilla_distinta_cambia_secuencia(self) -> None:
        primero = generar_secuencia(semilla=12345, cantidad=100)
        segundo = generar_secuencia(semilla=54321, cantidad=100)
        self.assertNotEqual(primero.estados, segundo.estados)

    def test_semilla_invalida(self) -> None:
        with self.assertRaises(ValueError):
            ParametrosLCG(semilla=M)
        with self.assertRaises(ValueError):
            ParametrosLCG(semilla=-1)

    def test_cantidad_invalida(self) -> None:
        with self.assertRaises(ValueError):
            generar_secuencia(cantidad=0)
        with self.assertRaises(TypeError):
            generar_secuencia(cantidad=1.5)

    def test_periodo_teorico_completo(self) -> None:
        teorico = analysis.analizar_periodo_teorico(A, C, M)
        self.assertTrue(teorico["periodo_completo"])
        self.assertEqual(teorico["factores_primos_m"], [2])
        self.assertEqual(teorico["periodo_maximo_teorico"], M)

    def test_detectar_periodo_ejemplo_pequeno(self) -> None:
        resultado = analysis.detectar_periodo(1, a=5, c=3, m=16, max_iteraciones=100)
        self.assertTrue(resultado["encontrado"])
        self.assertEqual(resultado["mu"], 0)
        self.assertEqual(resultado["lambda"], 16)

    def test_sin_repeticion_en_muestra(self) -> None:
        resultado = generar_secuencia(semilla=12345, cantidad=10000)
        analisis = analysis.analizar_periodo(resultado)
        self.assertTrue(analisis["sin_repeticion_en_muestra"])

    def test_estadisticas_basicas(self) -> None:
        valores = [0.1, 0.2, 0.3, 0.4, 0.5]
        estadisticas = analysis.estadisticas_basicas(valores, bins=10)
        self.assertEqual(estadisticas["cantidad"], 5)
        self.assertAlmostEqual(estadisticas["media"], 0.3)
        self.assertEqual(sum(estadisticas["frecuencias_bins"]), 5)
        self.assertAlmostEqual(estadisticas["minimo"], 0.1)
        self.assertAlmostEqual(estadisticas["maximo"], 0.5)

    def test_comparacion_semillas(self) -> None:
        principal = generar_secuencia(semilla=12345, cantidad=20)
        alternativa = generar_secuencia(semilla=54321, cantidad=20)
        filas = analysis.comparar_semillas(principal, alternativa)
        self.assertEqual(len(filas), 20)
        self.assertEqual(filas[0]["n"], 1)
        self.assertGreater(filas[0]["diferencia"], 0)

    def test_comparacion_con_java(self) -> None:
        resultado = generar_secuencia(semilla=12345, cantidad=20)
        registros = [
            {
                "n": indice,
                "estado": estado,
                "u": normalizado,
            }
            for indice, (estado, normalizado) in enumerate(
                zip(resultado.estados, resultado.normalizados),
                start=1,
            )
        ]
        comparacion = analysis.comparar_con_java(resultado, registros)
        self.assertTrue(comparacion["disponible"])
        self.assertTrue(comparacion["coinciden_todos"])
        self.assertEqual(comparacion["diferencias"], 0)

        registros[0]["estado"] += 1
        comparacion = analysis.comparar_con_java(resultado, registros)
        self.assertFalse(comparacion["coinciden_todos"])
        self.assertGreater(comparacion["diferencias"], 0)

    def test_exportacion_csv(self) -> None:
        resultado = generar_secuencia(semilla=12345, cantidad=20)
        estadisticas = analysis.estadisticas_basicas(resultado.normalizados)
        periodo = analysis.analizar_periodo(resultado)
        with tempfile.TemporaryDirectory() as directorio:
            rutas = reportes.exportar_todo(
                principal=resultado,
                alternativa=generar_secuencia(semilla=54321, cantidad=20),
                estadisticas=estadisticas,
                periodo=periodo,
                comparacion_semillas=analysis.comparar_semillas(
                    resultado,
                    generar_secuencia(semilla=54321, cantidad=20),
                ),
                comparacion_java=None,
                directorio=directorio,
            )
            self.assertTrue(rutas["primeros_20"].exists())
            with rutas["primeros_20"].open(encoding="utf-8") as archivo:
                filas = list(csv.DictReader(archivo))
            self.assertEqual(len(filas), 20)
            self.assertEqual(int(filas[0]["estado"]), PRIMEROS_20[0])

    def test_leer_csv_java(self) -> None:
        with tempfile.TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "java.csv"
            ruta.write_text(
                "n,estado,u\n1,87628868,0.02040268573909998\n",
                encoding="utf-8",
            )
            registros = lcg_controller.leer_csv_java(ruta)
            self.assertEqual(registros[0]["n"], 1)
            self.assertEqual(registros[0]["estado"], PRIMEROS_20[0])
            self.assertTrue(math.isclose(registros[0]["u"], PRIMEROS_20[0] / M))


if __name__ == "__main__":
    unittest.main()
