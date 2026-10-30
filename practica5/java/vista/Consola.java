package vista;

import java.util.List;
import java.util.Locale;

import controlador.LCGController.Registro;
import modelo.LCG;

public final class Consola {

    private Consola() {
    }

    public static void mostrarEncabezado(long semilla, int cantidad) {
        System.out.println("=".repeat(78));
        System.out.println("PRACTICA 5 - GENERADOR CONGRUENCIAL LINEAL (JAVA)");
        System.out.println("=".repeat(78));
        System.out.printf(Locale.US, "a = %d%n", LCG.A);
        System.out.printf(Locale.US, "c = %d%n", LCG.C);
        System.out.printf(Locale.US, "m = 2^32 = %d%n", LCG.M);
        System.out.printf(Locale.US, "Semilla = %d%n", semilla);
        System.out.printf(Locale.US, "Cantidad de valores = %d%n", cantidad);
        System.out.println();
    }

    public static void mostrarPrimeros20(List<Registro> registros) {
        System.out.println("-".repeat(78));
        System.out.println("PRIMEROS 20 VALORES EN JAVA");
        System.out.println("-".repeat(78));
        System.out.printf(Locale.US, "%3s  %12s  %14s%n", "n", "estado", "u_n");
        int limite = Math.min(20, registros.size());
        for (int indice = 0; indice < limite; indice++) {
            Registro registro = registros.get(indice);
            System.out.printf(
                Locale.US,
                "%3d  %12d  %14.10f%n",
                registro.getN(),
                registro.getEstado(),
                registro.getU()
            );
        }
        System.out.println();
    }
}
