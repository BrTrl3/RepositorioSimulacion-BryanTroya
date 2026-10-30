package controlador;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

import modelo.LCG;

public class LCGController {

    public static final class Registro {
        private final long n;
        private final long estado;
        private final double u;

        public Registro(long n, long estado, double u) {
            this.n = n;
            this.estado = estado;
            this.u = u;
        }

        public long getN() {
            return n;
        }

        public long getEstado() {
            return estado;
        }

        public double getU() {
            return u;
        }
    }

    public List<Registro> generar(long semilla, int cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException("cantidad debe ser mayor que cero");
        }

        LCG lcg = new LCG(semilla);
        List<Registro> registros = new ArrayList<>(cantidad);
        for (int indice = 1; indice <= cantidad; indice++) {
            long estado = lcg.siguiente();
            double normalizado = estado / (double) LCG.M;
            registros.add(new Registro(indice, estado, normalizado));
        }
        return registros;
    }

    public Path exportarCsv(List<Registro> registros, Path ruta) throws IOException {
        Path padre = ruta.toAbsolutePath().getParent();
        if (padre != null) {
            Files.createDirectories(padre);
        }

        try (BufferedWriter escritor = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            escritor.write("n,estado,u");
            escritor.newLine();
            for (Registro registro : registros) {
                escritor.write(
                    registro.getN() + "," + registro.getEstado() + "," + registro.getU()
                );
                escritor.newLine();
            }
        }
        return ruta;
    }
}
