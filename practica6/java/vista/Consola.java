package vista;

import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import modelo.MonteCarlo.FilaPi;
import modelo.PruebasEstadisticas.ResultadoChi;
import modelo.PruebasEstadisticas.ResultadoKS;
import modelo.Registro;

public final class Consola {

    private Consola() {
    }

    private static void titulo(String texto) {
        System.out.println("-".repeat(78));
        System.out.println(texto);
        System.out.println("-".repeat(78));
    }

    public static void mostrarEncabezado(int cantidad, int intervalos) {
        System.out.println("=".repeat(78));
        System.out.println("PRACTICA 6 - VALIDACION ESTADISTICA (JAVA)");
        System.out.println("=".repeat(78));
        System.out.println("H0: X ~ U(0,1)   H1: X no sigue U(0,1)   alfa = 0.05");
        System.out.printf(Locale.US, "Cantidad de valores = %d%n", cantidad);
        System.out.printf(Locale.US, "Intervalos Chi-cuadrado = %d%n", intervalos);
        System.out.println();
    }

    public static void mostrarSecuencia(String nombre, List<Registro> registros) {
        titulo("PRIMEROS 20 VALORES (" + nombre + ")");
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

    public static void mostrarChiCuadrado(String nombre, ResultadoChi chi) {
        titulo("PRUEBA CHI-CUADRADO (" + nombre + ")");
        int intervalos = chi.observadas.length;
        System.out.printf(Locale.US, "%-14s  %9s  %9s%n", "Intervalo", "Observada", "Esperada");
        for (int indice = 0; indice < intervalos; indice++) {
            String rango = String.format(
                Locale.US,
                "[%.2f, %.2f)",
                indice / (double) intervalos,
                (indice + 1) / (double) intervalos
            );
            System.out.printf(
                Locale.US,
                "%-14s  %9d  %9.1f%n",
                rango,
                chi.observadas[indice],
                chi.esperada
            );
        }
        System.out.printf(Locale.US, "Estadistico Chi-cuadrado: %.6f%n", chi.estadistico);
        System.out.printf(Locale.US, "Grados de libertad:       %d%n", chi.gradosLibertad);
        System.out.printf(Locale.US, "Valor p:                  %.6f%n", chi.valorP);
        System.out.println("Decision:                 " + chi.decision);
        System.out.println();
    }

    public static void mostrarKolmogorovSmirnov(String nombre, ResultadoKS ks) {
        titulo("PRUEBA KOLMOGOROV-SMIRNOV (" + nombre + ")");
        System.out.printf(Locale.US, "D+ (diferencia positiva): %.6f%n", ks.dPositiva);
        System.out.printf(Locale.US, "D- (diferencia negativa): %.6f%n", ks.dNegativa);
        System.out.printf(Locale.US, "Estadistico D:            %.6f%n", ks.estadistico);
        System.out.printf(Locale.US, "Valor p:                  %.6f%n", ks.valorP);
        System.out.println("Decision:                 " + ks.decision);
        System.out.println();
    }

    public static void mostrarConfiguraciones(Map<String, ResultadoChi> chi,
                                              Map<String, ResultadoKS> ks) {
        titulo("COMPARACION DE CONFIGURACIONES DEL GENERADOR");
        System.out.printf(
            Locale.US,
            "%-20s %13s %8s %8s %8s  %s%n",
            "Configuracion", "Chi2", "p", "D", "p", "Decision Chi2 / KS"
        );
        for (Map.Entry<String, ResultadoChi> entrada : chi.entrySet()) {
            ResultadoChi resultadoChi = entrada.getValue();
            ResultadoKS resultadoKs = ks.get(entrada.getKey());
            System.out.printf(
                Locale.US,
                "%-20s %13.4f %8.4f %8.4f %8.4f  %s / %s%n",
                entrada.getKey(),
                resultadoChi.estadistico,
                resultadoChi.valorP,
                resultadoKs.estadistico,
                resultadoKs.valorP,
                resultadoChi.decision,
                resultadoKs.decision
            );
        }
        System.out.println();
    }

    public static void mostrarPi(List<FilaPi> filas) {
        titulo("ESTIMACION DE PI CON EL LCG");
        System.out.printf(
            Locale.US,
            "%9s  %12s  %10s  %12s%n",
            "N", "pi estimado", "Error", "Tiempo Java"
        );
        for (FilaPi fila : filas) {
            System.out.printf(
                Locale.US,
                "%9d  %12.6f  %10.6f  %10.6f s%n",
                fila.n,
                fila.pi,
                fila.error,
                fila.tiempo
            );
        }
        System.out.println();
    }

    public static void mostrarArchivos(Path directorio) {
        System.out.println("CSV generados en: " + directorio.toAbsolutePath());
    }
}
