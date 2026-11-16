package controlador;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

import modelo.LCG;
import modelo.MonteCarlo;
import modelo.MonteCarlo.Resultado;
import vista.Consola;
import vista.ReporteCsv;

/** Orquesta el experimento: modelo -> consola -> CSV. */
public class MonteCarloController {

    private static final int[] TAMANOS = {1_000, 10_000, 100_000, 1_000_000};

    private final long semilla;
    private final int repeticiones;
    private final Path carpetaSalida;

    public MonteCarloController(long semilla, int repeticiones, Path carpetaSalida) {
        this.semilla = semilla;
        this.repeticiones = repeticiones;
        this.carpetaSalida = carpetaSalida;
    }

    public void ejecutar() throws IOException {
        Consola.encabezado(semilla, repeticiones);

        double[] secuencia = new double[10];
        LCG gen = new LCG(semilla);
        for (int i = 0; i < secuencia.length; i++) {
            secuencia[i] = gen.siguiente();
        }
        Consola.secuencia(secuencia);

        List<Resultado> filas = new ArrayList<>();
        for (int n : TAMANOS) {
            filas.add(MonteCarlo.ejecutar(n, semilla, repeticiones));
        }
        Consola.tabla(filas);

        Path csv = carpetaSalida.resolve("pi_java.csv");
        ReporteCsv.resultados(csv, filas);
        ReporteCsv.secuencia(carpetaSalida.resolve("secuencia_java.csv"), secuencia);
        Consola.mensaje("Resultados guardados en: " + csv.toAbsolutePath().normalize());
    }
}
