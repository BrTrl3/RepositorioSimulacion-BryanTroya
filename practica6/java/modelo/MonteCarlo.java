package modelo;

public final class MonteCarlo {
    public static final int[] TAMANOS_PI = {1000, 10000, 100000, 1000000};

    private MonteCarlo() {
    }

    public static final class FilaPi {
        public final int n;
        public final double pi;
        public final double error;
        public final double tiempo;

        public FilaPi(int n, double pi, double tiempo) {
            this.n = n;
            this.pi = pi;
            this.error = Math.abs(pi - Math.PI);
            this.tiempo = tiempo;
        }
    }

    public static double estimarPi(ConfiguracionLCG configuracion, int puntos) {
        if (puntos <= 0) {
            throw new IllegalArgumentException("puntos debe ser mayor que cero");
        }

        LCG lcg = new LCG(configuracion);
        int dentro = 0;
        for (int indice = 0; indice < puntos; indice++) {
            double x = lcg.siguienteNormalizado();
            double y = lcg.siguienteNormalizado();
            if (x * x + y * y <= 1.0) {
                dentro++;
            }
        }
        return 4.0 * dentro / puntos;
    }
}
