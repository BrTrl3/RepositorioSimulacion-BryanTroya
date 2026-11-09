package vista;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import modelo.MonteCarlo.FilaPi;
import modelo.PruebasEstadisticas.ResultadoChi;
import modelo.PruebasEstadisticas.ResultadoKS;
import modelo.Registro;

public final class ReporteCsv {

    private ReporteCsv() {
    }

    public static void exportar(Map<String, List<Registro>> secuencias,
                                Map<String, ResultadoChi> chi,
                                Map<String, ResultadoKS> ks,
                                List<FilaPi> pi,
                                Path directorio) throws IOException {
        Files.createDirectories(directorio);
        exportarSecuencias(secuencias, directorio.resolve("secuencias.csv"));
        exportarPruebas(chi, ks, directorio.resolve("pruebas.csv"));
        exportarPi(pi, directorio.resolve("pi.csv"));
    }

    private static void exportarSecuencias(Map<String, List<Registro>> secuencias, Path ruta)
            throws IOException {
        try (BufferedWriter escritor = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            escritor.write("configuracion,n,estado,u");
            escritor.newLine();
            for (Map.Entry<String, List<Registro>> entrada : secuencias.entrySet()) {
                for (Registro registro : entrada.getValue()) {
                    escritor.write(entrada.getKey() + "," + registro.getN() + ","
                            + registro.getEstado() + "," + registro.getU());
                    escritor.newLine();
                }
            }
        }
    }

    private static void exportarPruebas(Map<String, ResultadoChi> chi,
                                        Map<String, ResultadoKS> ks,
                                        Path ruta) throws IOException {
        try (BufferedWriter escritor = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            escritor.write("configuracion,chi2,gl,p_chi2,d,p_ks");
            escritor.newLine();
            for (Map.Entry<String, ResultadoChi> entrada : chi.entrySet()) {
                ResultadoChi resultadoChi = entrada.getValue();
                ResultadoKS resultadoKs = ks.get(entrada.getKey());
                escritor.write(entrada.getKey() + "," + resultadoChi.estadistico + ","
                        + resultadoChi.gradosLibertad + "," + resultadoChi.valorP + ","
                        + resultadoKs.estadistico + "," + resultadoKs.valorP);
                escritor.newLine();
            }
        }
    }

    private static void exportarPi(List<FilaPi> filas, Path ruta) throws IOException {
        try (BufferedWriter escritor = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            escritor.write("n,pi,error,tiempo");
            escritor.newLine();
            for (FilaPi fila : filas) {
                escritor.write(fila.n + "," + fila.pi + "," + fila.error + "," + fila.tiempo);
                escritor.newLine();
            }
        }
    }
}
