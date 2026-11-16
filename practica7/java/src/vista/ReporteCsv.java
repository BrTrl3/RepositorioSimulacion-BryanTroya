package vista;

import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import modelo.MonteCarlo.Resultado;

/** Exporta los resultados de Java a CSV para que Python los compare. */
public class ReporteCsv {

    public static void resultados(Path archivo, List<Resultado> filas) throws IOException {
        Files.createDirectories(archivo.getParent());
        try (PrintWriter pw = new PrintWriter(Files.newBufferedWriter(archivo, StandardCharsets.UTF_8))) {
            pw.println("n,dentro,pi,error,tiempo");
            for (Resultado r : filas) {
                // Double.toString conserva todos los dígitos del double
                pw.println(r.n + "," + r.dentro + "," + r.pi + "," + r.error + "," + r.tiempo);
            }
        }
    }

    public static void secuencia(Path archivo, double[] valores) throws IOException {
        Files.createDirectories(archivo.getParent());
        try (PrintWriter pw = new PrintWriter(Files.newBufferedWriter(archivo, StandardCharsets.UTF_8))) {
            pw.println("i,u");
            for (int i = 0; i < valores.length; i++) {
                pw.println((i + 1) + "," + valores[i]);
            }
        }
    }
}
