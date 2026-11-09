package controlador;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import modelo.ConfiguracionLCG;
import modelo.LCG;
import modelo.MonteCarlo;
import modelo.MonteCarlo.FilaPi;
import modelo.PruebasEstadisticas;
import modelo.PruebasEstadisticas.ResultadoChi;
import modelo.PruebasEstadisticas.ResultadoKS;
import modelo.Registro;
import vista.Consola;
import vista.ReporteCsv;

public class PracticaController {

    public void ejecutar(int cantidad, int intervalos, Path directorio) throws IOException {
        Map<String, List<Registro>> secuencias = new LinkedHashMap<>();
        Map<String, ResultadoChi> chi = new LinkedHashMap<>();
        Map<String, ResultadoKS> ks = new LinkedHashMap<>();
        for (ConfiguracionLCG configuracion : ConfiguracionLCG.CONFIGURACIONES) {
            String nombre = configuracion.getNombre();
            List<Registro> registros = new LCG(configuracion).generar(cantidad);
            secuencias.put(nombre, registros);
            chi.put(nombre, PruebasEstadisticas.chiCuadrado(registros, intervalos));
            ks.put(nombre, PruebasEstadisticas.kolmogorovSmirnov(registros));
        }

        List<FilaPi> pi = estimarPi();

        String principal = ConfiguracionLCG.CONFIGURACIONES.get(0).getNombre();
        Consola.mostrarEncabezado(cantidad, intervalos);
        Consola.mostrarSecuencia(principal, secuencias.get(principal));
        Consola.mostrarChiCuadrado(principal, chi.get(principal));
        Consola.mostrarKolmogorovSmirnov(principal, ks.get(principal));
        Consola.mostrarConfiguraciones(chi, ks);
        Consola.mostrarPi(pi);

        ReporteCsv.exportar(secuencias, chi, ks, pi, directorio);
        Consola.mostrarArchivos(directorio);
    }

    private List<FilaPi> estimarPi() {
        ConfiguracionLCG configuracion = ConfiguracionLCG.CONFIGURACIONES.get(0);
        List<FilaPi> filas = new ArrayList<>();
        for (int puntos : MonteCarlo.TAMANOS_PI) {
            long inicio = System.nanoTime();
            double pi = MonteCarlo.estimarPi(configuracion, puntos);
            double tiempo = (System.nanoTime() - inicio) / 1e9;
            filas.add(new FilaPi(puntos, pi, tiempo));
        }
        return filas;
    }
}
