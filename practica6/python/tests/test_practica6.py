from __future__ import annotations

import math
import unittest

import numpy as np

from model import comparacion, montecarlo, pruebas
from model.lcg import CONFIGURACIONES, ConfiguracionLCG, generar_secuencia

GUIA = CONFIGURACIONES[0]
PERIODO_CORTO = next(c for c in CONFIGURACIONES if c.nombre == "Periodo corto")
MULTIPLICADOR_UNO = next(c for c in CONFIGURACIONES if c.nombre == "Multiplicador a=1")


class TestLCG(unittest.TestCase):
    def test_primeros_valores(self) -> None:
        resultado = generar_secuencia(GUIA, 3)
        self.assertEqual(resultado.estados, [87628868, 71072467, 2332836374])

    def test_normalizados_en_rango(self) -> None:
        for configuracion in CONFIGURACIONES:
            valores = generar_secuencia(configuracion, 1000).normalizados
            self.assertTrue(np.all((valores >= 0.0) & (valores < 1.0)))

    def test_parametros_invalidos(self) -> None:
        with self.assertRaises(ValueError):
            ConfiguracionLCG("x", 1, 1, 16, 16)
        with self.assertRaises(ValueError):
            generar_secuencia(GUIA, 0)


class TestValoresP(unittest.TestCase):
    def test_chi_cuadrado_valores_criticos(self) -> None:
        self.assertAlmostEqual(pruebas.valor_p_chi_cuadrado(16.918978, 9), 0.05, places=6)
        self.assertAlmostEqual(pruebas.valor_p_chi_cuadrado(21.665994, 9), 0.01, places=6)
        self.assertEqual(pruebas.valor_p_chi_cuadrado(0.0, 9), 1.0)

    def test_kolmogorov_valor_critico(self) -> None:
        d_critico = 1.358099 / math.sqrt(10000)
        self.assertAlmostEqual(pruebas.valor_p_kolmogorov(d_critico, 10000), 0.05, places=2)

    def test_decision(self) -> None:
        self.assertEqual(pruebas.decidir(0.05), "No se rechaza H0")
        self.assertEqual(pruebas.decidir(0.049), "Se rechaza H0")


class TestPruebas(unittest.TestCase):
    def test_chi_cuadrado_conocido(self) -> None:
        valores = np.array([0.1] * 30 + [0.6] * 10)
        chi = pruebas.chi_cuadrado(valores, intervalos=2)
        self.assertEqual(chi["observadas"], [30, 10])
        self.assertEqual(chi["esperada"], 20.0)
        self.assertAlmostEqual(chi["estadistico"], 10.0)
        self.assertEqual(chi["grados_libertad"], 1)

    def test_grados_libertad_guia(self) -> None:
        valores = generar_secuencia(GUIA).normalizados
        chi = pruebas.chi_cuadrado(valores)
        self.assertEqual(chi["grados_libertad"], 9)
        self.assertEqual(sum(chi["observadas"]), 10000)

    def test_ks_conocido(self) -> None:
        ks = pruebas.kolmogorov_smirnov(np.array([0.5]))
        self.assertAlmostEqual(ks["d_positiva"], 0.5)
        self.assertAlmostEqual(ks["d_negativa"], 0.5)
        self.assertAlmostEqual(ks["estadistico"], 0.5)

    def test_generador_de_la_guia_no_se_rechaza(self) -> None:
        valores = generar_secuencia(GUIA).normalizados
        self.assertEqual(pruebas.chi_cuadrado(valores)["decision"], "No se rechaza H0")
        self.assertEqual(pruebas.kolmogorov_smirnov(valores)["decision"], "No se rechaza H0")

    def test_generadores_deficientes_se_rechazan(self) -> None:
        for configuracion in (PERIODO_CORTO, MULTIPLICADOR_UNO):
            valores = generar_secuencia(configuracion).normalizados
            self.assertEqual(pruebas.chi_cuadrado(valores)["decision"], "Se rechaza H0")
            self.assertEqual(pruebas.kolmogorov_smirnov(valores)["decision"], "Se rechaza H0")


class TestMonteCarlo(unittest.TestCase):
    def test_estimacion_cercana_a_pi(self) -> None:
        fila = montecarlo.estimar_pi(GUIA, 100000)
        self.assertLess(fila["error"], 0.02)


class TestComparacion(unittest.TestCase):
    def test_comparar_secuencia(self) -> None:
        resultado = generar_secuencia(GUIA, 25)
        registros = [
            {"estado": estado, "u": float(u)}
            for estado, u in zip(resultado.estados, resultado.normalizados)
        ]
        comparada = comparacion.comparar_secuencia(resultado, registros)
        self.assertEqual(comparada["diferencias"], 0)
        self.assertEqual(len(comparada["filas"]), 20)

        registros[0]["estado"] += 1
        comparada = comparacion.comparar_secuencia(resultado, registros)
        self.assertEqual(comparada["diferencias"], 1)


if __name__ == "__main__":
    unittest.main()
