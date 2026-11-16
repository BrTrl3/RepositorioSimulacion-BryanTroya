import java.nio.file.Path;
import java.nio.file.Paths;

import controlador.MonteCarloController;

/**
 * Punto de entrada.
 * Uso: java -cp out Main [semilla] [repeticiones] [carpeta_salida]
 */
public class Main {
    public static void main(String[] args) throws Exception {
        long semilla = args.length > 0 ? Long.parseLong(args[0]) : 12345L;
        int repeticiones = args.length > 1 ? Integer.parseInt(args[1]) : 5;
        Path salida = args.length > 2 ? Paths.get(args[2]) : Paths.get("resultados", "java");

        new MonteCarloController(semilla, repeticiones, salida).ejecutar();
    }
}
