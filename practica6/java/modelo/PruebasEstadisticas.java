package modelo;

import java.util.Arrays;
import java.util.List;

public final class PruebasEstadisticas {
    public static final double ALFA = 0.05;

    private static final double EPSILON = 1e-15;
    private static final int MAX_ITERACIONES = 1000;
    private static final double[] LANCZOS = {
        0.99999999999980993, 676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.61502916214059, 12.507343278686905,
        -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7
    };

    private PruebasEstadisticas() {
    }

    public static final class ResultadoChi {
        public final int[] observadas;
        public final double esperada;
        public final double estadistico;
        public final int gradosLibertad;
        public final double valorP;
        public final String decision;

        ResultadoChi(int[] observadas, double esperada, double estadistico, int gradosLibertad,
                     double valorP) {
            this.observadas = observadas;
            this.esperada = esperada;
            this.estadistico = estadistico;
            this.gradosLibertad = gradosLibertad;
            this.valorP = valorP;
            this.decision = decidir(valorP);
        }
    }

    public static final class ResultadoKS {
        public final double dPositiva;
        public final double dNegativa;
        public final double estadistico;
        public final double valorP;
        public final String decision;

        ResultadoKS(double dPositiva, double dNegativa, double valorP) {
            this.dPositiva = dPositiva;
            this.dNegativa = dNegativa;
            this.estadistico = Math.max(dPositiva, dNegativa);
            this.valorP = valorP;
            this.decision = decidir(valorP);
        }
    }

    public static String decidir(double valorP) {
        return valorP >= ALFA ? "No se rechaza H0" : "Se rechaza H0";
    }

    public static ResultadoChi chiCuadrado(List<Registro> registros, int intervalos) {
        if (registros.isEmpty()) {
            throw new IllegalArgumentException("se requiere al menos un valor");
        }
        if (intervalos < 2) {
            throw new IllegalArgumentException("se requieren al menos dos intervalos");
        }

        int[] observadas = new int[intervalos];
        for (Registro registro : registros) {
            observadas[Math.min((int) (registro.getU() * intervalos), intervalos - 1)]++;
        }

        double esperada = registros.size() / (double) intervalos;
        double estadistico = 0.0;
        for (int observada : observadas) {
            double diferencia = observada - esperada;
            estadistico += diferencia * diferencia / esperada;
        }

        int gradosLibertad = intervalos - 1;
        return new ResultadoChi(observadas, esperada, estadistico, gradosLibertad,
                valorPChiCuadrado(estadistico, gradosLibertad));
    }

    public static ResultadoKS kolmogorovSmirnov(List<Registro> registros) {
        if (registros.isEmpty()) {
            throw new IllegalArgumentException("se requiere al menos un valor");
        }

        int cantidad = registros.size();
        double[] ordenados = new double[cantidad];
        for (int indice = 0; indice < cantidad; indice++) {
            ordenados[indice] = registros.get(indice).getU();
        }
        Arrays.sort(ordenados);

        double dPositiva = Double.NEGATIVE_INFINITY;
        double dNegativa = Double.NEGATIVE_INFINITY;
        for (int indice = 0; indice < cantidad; indice++) {
            double posicion = indice + 1.0;
            dPositiva = Math.max(dPositiva, posicion / cantidad - ordenados[indice]);
            dNegativa = Math.max(dNegativa, ordenados[indice] - (posicion - 1.0) / cantidad);
        }

        return new ResultadoKS(dPositiva, dNegativa,
                valorPKolmogorov(Math.max(dPositiva, dNegativa), cantidad));
    }

    public static double valorPChiCuadrado(double estadistico, int gradosLibertad) {
        if (estadistico <= 0.0) {
            return 1.0;
        }
        double a = gradosLibertad / 2.0;
        double x = estadistico / 2.0;
        if (x < a + 1.0) {
            return 1.0 - gammaInferiorSerie(a, x);
        }
        return gammaSuperiorFraccion(a, x);
    }

    public static double valorPKolmogorov(double estadistico, int cantidad) {
        double raiz = Math.sqrt(cantidad);
        double lambda = (raiz + 0.12 + 0.11 / raiz) * estadistico;
        if (lambda < 0.2) {
            return 1.0;
        }

        double suma = 0.0;
        double signo = 1.0;
        for (int j = 1; j <= 100; j++) {
            double termino = signo * Math.exp(-2.0 * j * j * lambda * lambda);
            suma += termino;
            if (Math.abs(termino) < 1e-16) {
                break;
            }
            signo = -signo;
        }
        return Math.min(Math.max(2.0 * suma, 0.0), 1.0);
    }

    private static double gammaInferiorSerie(double a, double x) {
        double termino = 1.0 / a;
        double suma = termino;
        double denominador = a;
        for (int i = 0; i < MAX_ITERACIONES; i++) {
            denominador += 1.0;
            termino *= x / denominador;
            suma += termino;
            if (Math.abs(termino) < Math.abs(suma) * EPSILON) {
                break;
            }
        }
        return suma * Math.exp(-x + a * Math.log(x) - logGamma(a));
    }

    private static double gammaSuperiorFraccion(double a, double x) {
        double minimo = 1e-300;
        double b = x + 1.0 - a;
        double c = 1.0 / minimo;
        double d = 1.0 / b;
        double h = d;
        for (int i = 1; i < MAX_ITERACIONES; i++) {
            double an = -i * (i - a);
            b += 2.0;
            d = an * d + b;
            if (Math.abs(d) < minimo) {
                d = minimo;
            }
            c = b + an / c;
            if (Math.abs(c) < minimo) {
                c = minimo;
            }
            d = 1.0 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1.0) < EPSILON) {
                break;
            }
        }
        return h * Math.exp(-x + a * Math.log(x) - logGamma(a));
    }

    // Java no incluye lgamma: aproximacion de Lanczos (g = 7) para x > 0
    private static double logGamma(double x) {
        double z = x - 1.0;
        double suma = LANCZOS[0];
        for (int i = 1; i < LANCZOS.length; i++) {
            suma += LANCZOS[i] / (z + i);
        }
        double t = z + 7.5;
        return 0.5 * Math.log(2.0 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(suma);
    }
}
