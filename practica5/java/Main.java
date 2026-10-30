import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import controlador.LCGController;
import controlador.LCGController.Registro;
import modelo.LCG;
import vista.Consola;

public final class Main {

    private Main() {
    }

    public static void main(String[] args) {
        long semilla = 12345L;
        int cantidad = 10000;
        String salida = null;

        try {
            for (int indice = 0; indice < args.length; indice++) {
                String argumento = args[indice];
                switch (argumento) {
                    case "--seed":
                        semilla = Long.parseLong(valorRequerido(args, ++indice, argumento));
                        break;
                    case "--count":
                        cantidad = Integer.parseInt(valorRequerido(args, ++indice, argumento));
                        break;
                    case "--output":
                        salida = valorRequerido(args, ++indice, argumento);
                        break;
                    case "--help":
                    case "-h":
                        mostrarAyuda();
                        return;
                    default:
                        throw new IllegalArgumentException("argumento no reconocido: " + argumento);
                }
            }
        } catch (IllegalArgumentException error) {
            System.err.println("Error: " + error.getMessage());
            mostrarAyuda();
            System.exit(2);
            return;
        }

        if (salida == null) {
            salida = "resultados/java_lcg_" + semilla + ".csv";
        }

        try {
            LCG.validarSemilla(semilla);
            LCGController controlador = new LCGController();
            List<Registro> registros = controlador.generar(semilla, cantidad);
            Consola.mostrarEncabezado(semilla, cantidad);
            Consola.mostrarPrimeros20(registros);
            Path ruta = controlador.exportarCsv(registros, Paths.get(salida));
            System.out.println("CSV generado: " + ruta.toAbsolutePath());
        } catch (IllegalArgumentException error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(2);
        } catch (IOException error) {
            System.err.println("Error de escritura: " + error.getMessage());
            System.exit(1);
        }
    }

    private static String valorRequerido(String[] args, int indice, String argumento) {
        if (indice >= args.length) {
            throw new IllegalArgumentException("falta el valor para " + argumento);
        }
        return args[indice];
    }

    private static void mostrarAyuda() {
        System.out.println("Uso: java -cp java Main [opciones]");
        System.out.println("  --seed N     semilla del generador (por defecto: 12345)");
        System.out.println("  --count N    cantidad de valores (por defecto: 10000)");
        System.out.println("  --output R   archivo CSV de salida");
        System.out.println("  --help       muestra esta ayuda");
    }
}
