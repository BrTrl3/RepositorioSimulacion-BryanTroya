package vista;

import java.util.List;
import java.util.Locale;

import modelo.MonteCarlo.Resultado;

/** Presentación de resultados en consola. */
public class Consola {

    public static void encabezado(long semilla, int repeticiones) {
        System.out.println("==============================================================");
        System.out.println("   PRACTICA 7 - Estimacion de pi con Monte Carlo (Java)");
        System.out.println("==============================================================");
        System.out.printf(Locale.ROOT, "Semilla: %d | Repeticiones por tamano: %d%n", semilla, repeticiones);
        System.out.println("LCG: a = 1664525, c = 1013904223, m = 2^32");
        System.out.println();
    }

    public static void secuencia(double[] valores) {
        System.out.println("Primeros valores U generados por el LCG:");
        for (int i = 0; i < valores.length; i++) {
            System.out.printf(Locale.ROOT, "  U%-2d = %.10f%n", i + 1, valores[i]);
        }
        System.out.println();
    }

    public static void tabla(List<Resultado> filas) {
        System.out.printf("%-12s %-10s %-14s %-12s %-14s%n", "N", "Nc", "pi estimado", "Error", "Tiempo (s)");
        System.out.println("--------------------------------------------------------------");
        for (Resultado r : filas) {
            System.out.printf(Locale.ROOT, "%-12d %-10d %-14.6f %-12.6f %-14.6f%n",
                    r.n, r.dentro, r.pi, r.error, r.tiempo);
        }
        System.out.println();
    }

    public static void mensaje(String texto) {
        System.out.println(texto);
    }
}
