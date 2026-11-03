package vista;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import modelo.Registro;

public final class ReporteCsv {

    private ReporteCsv() {
    }

    public static Path exportar(List<Registro> registros, Path ruta) throws IOException {
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
