package controlador;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

import modelo.Analisis;
import modelo.LCG;
import modelo.Registro;
import vista.Consola;
import vista.ReporteCsv;

public class LCGController {

    public List<Registro> generar(long semilla, int cantidad) {
        return new LCG(semilla).generar(cantidad);
    }

    public void ejecutar(long semilla, long semillaAlternativa, int cantidad, Path salida)
            throws IOException {
        LCG.validarSemilla(semilla);
        LCG.validarSemilla(semillaAlternativa);

        List<Registro> principal = generar(semilla, cantidad);
        List<Registro> alternativa = generar(semillaAlternativa, cantidad);

        Consola.mostrarEncabezado(semilla, semillaAlternativa, cantidad);
        Consola.mostrarPrimeros20(principal);
        Consola.mostrarEstadisticas(Analisis.estadisticas(principal, 10));
        Consola.mostrarPeriodo(Analisis.periodo(principal));
        Consola.mostrarComparacionSemillas(semilla, principal, semillaAlternativa, alternativa);

        Path ruta = ReporteCsv.exportar(principal, salida);
        Consola.mostrarArchivo(ruta);
    }
}
