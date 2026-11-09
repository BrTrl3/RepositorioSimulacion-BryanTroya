import java.io.IOException;
import java.nio.file.Paths;

import controlador.PracticaController;

public final class Main {

    private Main() {
    }

    public static void main(String[] args) {
        int cantidad = 10000;
        int intervalos = 10;
        String salida = "resultados/java";

        try {
            for (int indice = 0; indice < args.length; indice++) {
                String argumento = args[indice];
                switch (argumento) {
                    case "--count":
                        cantidad = Integer.parseInt(valorRequerido(args, ++indice, argumento));
                        break;
                    case "--bins":
                        intervalos = Integer.parseInt(valorRequerido(args, ++indice, argumento));
                        break;
                    case "--output-dir":
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

        try {
            new PracticaController().ejecutar(cantidad, intervalos, Paths.get(salida));
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
        System.out.println("  --count N        cantidad de valores por configuracion (por defecto: 10000)");
        System.out.println("  --bins N         intervalos de Chi-cuadrado (por defecto: 10)");
        System.out.println("  --output-dir R   carpeta de salida (por defecto: resultados/java)");
        System.out.println("  --help           muestra esta ayuda");
    }
}
