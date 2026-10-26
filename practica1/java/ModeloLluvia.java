import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;

/**
 * Implementacion en Java del modelo de posibilidad de lluvia.
 *
 * I = 0.5 H + 0.3 N + 0.2 Tf
 */
public class ModeloLluvia {

    private static final String[] HORAS = {
        "06:00", "08:00", "10:00", "12:00", "14:00",
        "16:00", "18:00", "20:00", "22:00"
    };

    private static final int[] HUMEDAD = {
        65, 70, 68, 60, 75, 85, 92, 88, 80
    };

    private static final int[] NUBOSIDAD = {
        40, 50, 45, 30, 70, 85, 95, 90, 75
    };

    private static final int[] TEMPERATURA = {
        14, 16, 18, 22, 20, 18, 16, 17, 15
    };

    private static final double PESO_HUMEDAD_ORIGINAL = 0.5;
    private static final double PESO_NUBOSIDAD_ORIGINAL = 0.3;
    private static final double PESO_TEMPERATURA_ORIGINAL = 0.2;

    private static final double[] TEMPERATURAS_TABLA = {
        10, 12, 14, 16, 18, 20, 22, 24, 26, 28
    };

    private static final double[] FACTORES_TABLA = {
        1.00, 0.90, 0.80, 0.70, 0.60,
        0.50, 0.40, 0.30, 0.20, 0.10
    };

    public static void main(String[] args) throws IOException {

        Locale.setDefault(Locale.US);

        double pesoHumedad = 0.40;
        double pesoNubosidad = 0.40;
        double pesoTemperatura = 0.20;

        if (args.length >= 3) {
            pesoHumedad = Double.parseDouble(args[0]);
            pesoNubosidad = Double.parseDouble(args[1]);
            pesoTemperatura = Double.parseDouble(args[2]);
        }

        System.out.println("========================================");
        System.out.println("MODELO DE POSIBILIDAD DE LLUVIA - JAVA");
        System.out.println("========================================");

        System.out.println("\nPESOS DEL MODELO");
        System.out.println("----------------------------------------");
        System.out.println("Modelo original:");
        System.out.printf("Humedad = %.2f%n", PESO_HUMEDAD_ORIGINAL);
        System.out.printf("Nubosidad = %.2f%n", PESO_NUBOSIDAD_ORIGINAL);
        System.out.printf("Temperatura = %.2f%n", PESO_TEMPERATURA_ORIGINAL);

        System.out.println("\nModelo ajustado:");
        System.out.printf("Humedad = %.4f%n", pesoHumedad);
        System.out.printf("Nubosidad = %.4f%n", pesoNubosidad);
        System.out.printf("Temperatura = %.4f%n", pesoTemperatura);
        System.out.printf(
            "Suma de pesos ajustados: %.4f%n",
            pesoHumedad + pesoNubosidad + pesoTemperatura
        );

        System.out.println("\n========================================");
        System.out.println("RESULTADOS");
        System.out.println("========================================");
        System.out.printf(
            "%-8s %-12s %-14s %-10s %-8s %-8s %-8s "
            + "%-12s %-20s %-12s %-20s%n",
            "Hora", "Humedad(%)", "Nubosidad(%)", "Temp.(C)",
            "H", "N", "Tf", "I original", "Estado original",
            "I ajustado", "Estado ajustado"
        );
        System.out.println("----------------------------------------"
            + "--------------------------------------------------"
            + "--------------------------");

        Path directorio = Paths.get("resultados");
        Files.createDirectories(directorio);
        Path rutaCsv = directorio.resolve("tabla_resultados_java.csv");

        try (
            BufferedWriter escritor = Files.newBufferedWriter(
                rutaCsv,
                StandardCharsets.UTF_8
            )
        ) {
            escritor.write(
                "Hora,Humedad (%),Nubosidad (%),Temperatura (C),"
                + "H,N,Tf,Indice original,Estado original,"
                + "Indice ajustado,Estado ajustado\n"
            );

            for (int i = 0; i < HORAS.length; i++) {

                double h = HUMEDAD[i] / 100.0;
                double n = NUBOSIDAD[i] / 100.0;
                double tf = factorTemperatura(TEMPERATURA[i]);

                double indiceOriginal = indice(
                    h, n, tf,
                    PESO_HUMEDAD_ORIGINAL,
                    PESO_NUBOSIDAD_ORIGINAL,
                    PESO_TEMPERATURA_ORIGINAL
                );

                double indiceAjustado = indice(
                    h, n, tf,
                    pesoHumedad,
                    pesoNubosidad,
                    pesoTemperatura
                );

                String estadoOriginal = estado(indiceOriginal);
                String estadoAjustado = estado(indiceAjustado);

                System.out.printf(
                    "%-8s %-12d %-14d %-10d %-8.2f %-8.2f %-8.2f "
                    + "%-12.4f %-20s %-12.4f %-20s%n",
                    HORAS[i],
                    HUMEDAD[i],
                    NUBOSIDAD[i],
                    TEMPERATURA[i],
                    h,
                    n,
                    tf,
                    indiceOriginal,
                    estadoOriginal,
                    indiceAjustado,
                    estadoAjustado
                );

                escritor.write(String.format(
                    "%s,%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%s,%.4f,%s%n",
                    HORAS[i],
                    HUMEDAD[i],
                    NUBOSIDAD[i],
                    TEMPERATURA[i],
                    h,
                    n,
                    tf,
                    indiceOriginal,
                    estadoOriginal,
                    indiceAjustado,
                    estadoAjustado
                ));
            }
        }

        System.out.println("========================================");
        System.out.println("\nArchivo generado: " + rutaCsv);
    }

    private static double indice(
        double h,
        double n,
        double tf,
        double pesoHumedad,
        double pesoNubosidad,
        double pesoTemperatura
    ) {
        return pesoHumedad * h
            + pesoNubosidad * n
            + pesoTemperatura * tf;
    }

    private static double factorTemperatura(double temperatura) {

        if (temperatura <= TEMPERATURAS_TABLA[0]) {
            return FACTORES_TABLA[0];
        }

        if (temperatura >= TEMPERATURAS_TABLA[TEMPERATURAS_TABLA.length - 1]) {
            return FACTORES_TABLA[FACTORES_TABLA.length - 1];
        }

        for (int i = 0; i < TEMPERATURAS_TABLA.length - 1; i++) {

            double inferior = TEMPERATURAS_TABLA[i];
            double superior = TEMPERATURAS_TABLA[i + 1];

            if (temperatura >= inferior && temperatura <= superior) {

                double factorInferior = FACTORES_TABLA[i];
                double factorSuperior = FACTORES_TABLA[i + 1];

                return factorInferior
                    + ((temperatura - inferior) / (superior - inferior))
                    * (factorSuperior - factorInferior);
            }
        }

        return 0.0;
    }

    private static String estado(double indice) {

        if (indice < 0.40) {
            return "Sin lluvia";
        }

        if (indice < 0.60) {
            return "Baja posibilidad";
        }

        if (indice < 0.75) {
            return "Lluvia probable";
        }

        return "Lluvia";
    }
}
