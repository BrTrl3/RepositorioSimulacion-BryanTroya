"""Salida por consola."""

import pandas as pd


def encabezado(semilla, repeticiones, parametros):
    print("=" * 70)
    print("   PRÁCTICA 7 - Estimación de π con Monte Carlo (Python)")
    print("=" * 70)
    print(f"Semilla: {semilla} | Repeticiones por tamaño: {repeticiones}")
    print(f"LCG: a = {parametros['a']}, c = {parametros['c']}, m = 2^32")
    print()


def cuadro(titulo, df):
    print(f"--- {titulo} ---")
    with pd.option_context("display.max_columns", None, "display.width", 200,
                           "display.float_format", "{:.6f}".format):
        print(df.to_string(index=False))
    print()


def mensaje(texto):
    print(texto, flush=True)
