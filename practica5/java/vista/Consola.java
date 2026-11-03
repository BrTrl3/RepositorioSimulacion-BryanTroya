package vista;

import java.nio.file.Path;
import java.util.List;
import java.util.Locale;

import modelo.Analisis;
import modelo.LCG;
import modelo.Registro;

public final class Consola {

    private Consola() {
    }

    private static void titulo(String texto) {
        System.out.println("-".repeat(78));
        System.out.println(texto);
        System.out.println("-".repeat(78));
    }

    public static void mostrarEncabezado(long semilla, long semillaAlternativa, int cantidad) {
        System.out.println("=".repeat(78));
        System.out.println("PRACTICA 5 - GENERADOR CONGRUENCIAL LINEAL (JAVA)");
        System.out.println("=".repeat(78));
        System.out.printf(Locale.US, "a = %d%n", LCG.A);
        System.out.printf(Locale.US, "c = %d%n", LCG.C);
        System.out.printf(Locale.US, "m = 2^32 = %d%n", LCG.M);
        System.out.printf(Locale.US, "Semilla principal = %d%n", semilla);
        System.out.printf(Locale.US, "Semilla alternativa = %d%n", semillaAlternativa);
        System.out.printf(Locale.US, "Cantidad de valores = %d%n", cantidad);
        System.out.println();
    }

    public static void mostrarPrimeros20(List<Registro> registros) {
        titulo("PRIMEROS 20 VALORES EN JAVA");
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

    public static void mostrarEstadisticas(Analisis.Estadisticas estadisticas) {
        titulo("ESTADISTICAS DESCRIPTIVAS");
        System.out.printf(Locale.US, "Cantidad:              %d%n", estadisticas.cantidad);
        System.out.printf(Locale.US, "Media:                 %.8f%n", estadisticas.media);
        System.out.printf(Locale.US, "Desviacion estandar:   %.8f%n", estadisticas.desviacionEstandar);
        System.out.printf(Locale.US, "Minimo:                %.10f%n", estadisticas.minimo);
        System.out.printf(Locale.US, "Maximo:                %.10f%n", estadisticas.maximo);
        System.out.printf(Locale.US, "Correlacion lag 1:     %.8f%n", estadisticas.correlacionLag1);
        System.out.println("Frecuencias por decil:");
        int bins = estadisticas.frecuencias.length;
        for (int indice = 0; indice < bins; indice++) {
            System.out.printf(
                Locale.US,
                "  [%.1f, %.1f): %6d%n",
                indice / (double) bins,
                (indice + 1) / (double) bins,
                estadisticas.frecuencias[indice]
            );
        }
        System.out.println();
    }

    public static void mostrarPeriodo(Analisis.Periodo periodo) {
        titulo("ANALISIS DEL PERIODO");
        System.out.println("Condiciones de Hull-Dobell:");
        System.out.println("  - mcd(c, m) = 1: " + cumple(periodo.mcdCUnoConM));
        System.out.println("  - todo factor primo de m divide a a - 1: "
                + cumple(periodo.factoresPrimosDividenAMenos1));
        System.out.println("  - si m es divisible por 4, entonces (a - 1) es divisible por 4: "
                + cumple(periodo.divisiblePor4));
        System.out.println("Periodo completo teorico: " + siNo(periodo.periodoCompleto));
        if (periodo.periodoCompleto) {
            System.out.printf(Locale.US, "Periodo maximo teorico: %d%n", LCG.M);
        }
        System.out.printf(
            Locale.US,
            "Sin repeticion en la muestra: %s (%d valores)%n",
            siNo(periodo.sinRepeticionEnMuestra),
            periodo.cantidadMuestra
        );
        System.out.println();
    }

    public static void mostrarComparacionSemillas(long semilla, List<Registro> principal,
                                                  long semillaAlternativa, List<Registro> alternativa) {
        titulo("COMPARACION DE SEMILLAS");
        System.out.printf(
            Locale.US,
            "%3s  %14s  %14s  %14s%n",
            "n", "u_" + semilla, "u_" + semillaAlternativa, "|dif|"
        );
        int limite = Math.min(20, Math.min(principal.size(), alternativa.size()));
        for (int indice = 0; indice < limite; indice++) {
            double uPrincipal = principal.get(indice).getU();
            double uAlternativa = alternativa.get(indice).getU();
            System.out.printf(
                Locale.US,
                "%3d  %14.10f  %14.10f  %14.10f%n",
                indice + 1,
                uPrincipal,
                uAlternativa,
                Math.abs(uPrincipal - uAlternativa)
            );
        }
        System.out.println();
    }

    public static void mostrarArchivo(Path ruta) {
        System.out.println("CSV generado: " + ruta.toAbsolutePath());
    }

    private static String cumple(boolean valor) {
        return valor ? "cumple" : "no cumple";
    }

    private static String siNo(boolean valor) {
        return valor ? "si" : "no";
    }
}
