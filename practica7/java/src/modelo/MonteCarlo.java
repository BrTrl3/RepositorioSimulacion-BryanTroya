package modelo;

/**
 * Estimación de pi mediante Monte Carlo:  pi ≈ 4 * (Nc / N)
 * Se generan N puntos (x, y) en [0,1) x [0,1) y se cuentan los que cumplen
 * x^2 + y^2 <= 1 (cuarto de círculo de radio 1).
 */
public class MonteCarlo {

    /** Resultado de una corrida para un tamaño de muestra. */
    public static class Resultado {
        public final int n;
        public final long dentro;
        public final double pi;
        public final double error;
        public final double tiempo; // segundos (promedio de repeticiones)

        public Resultado(int n, long dentro, double pi, double tiempo) {
            this.n = n;
            this.dentro = dentro;
            this.pi = pi;
            this.error = Math.abs(pi - Math.PI);
            this.tiempo = tiempo;
        }
    }

    /** Cuenta los puntos dentro del círculo usando el LCG propio. */
    public static long contarDentro(int n, long semilla) {
        LCG gen = new LCG(semilla);
        long dentro = 0;
        for (int i = 0; i < n; i++) {
            double x = gen.siguiente();
            double y = gen.siguiente();
            if (x * x + y * y <= 1.0) {
                dentro++;
            }
        }
        return dentro;
    }

    /** Ejecuta el experimento midiendo el tiempo promedio de varias repeticiones. */
    public static Resultado ejecutar(int n, long semilla, int repeticiones) {
        // Calentamiento: permite que el compilador JIT optimice antes de medir
        contarDentro(n, semilla);

        long dentro = 0;
        long total = 0;
        for (int r = 0; r < repeticiones; r++) {
            long inicio = System.nanoTime();
            dentro = contarDentro(n, semilla);
            total += System.nanoTime() - inicio;
        }
        double tiempo = total / (double) repeticiones / 1e9;
        return new Resultado(n, dentro, 4.0 * dentro / n, tiempo);
    }
}
