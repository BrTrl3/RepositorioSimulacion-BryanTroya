package modelo;

/**
 * Generador Congruencial Lineal (LCG).
 *
 * X_{n+1} = (a * X_n + c) mod m        U_n = X_n / m  en [0, 1)
 *
 * Mismos parámetros que la versión Python: con la misma semilla ambos
 * programas generan exactamente la misma secuencia.
 */
public class LCG {

    public static final long A = 1664525L;
    public static final long C = 1013904223L;
    public static final long M = 4294967296L; // 2^32

    private long x;

    public LCG(long semilla) {
        this.x = Math.floorMod(semilla, M);
    }

    /** Devuelve el siguiente número pseudoaleatorio U en [0, 1). */
    public double siguiente() {
        // a * x < 2^53, no hay desbordamiento en long; el módulo 2^32 es un AND
        x = (A * x + C) & 0xFFFFFFFFL;
        return x / (double) M;
    }
}
