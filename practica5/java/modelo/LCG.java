package modelo;

public class LCG {
    public static final long A = 1664525L;
    public static final long C = 1013904223L;
    public static final long M = 1L << 32;
    public static final long MASK = M - 1L;

    private long estado;

    public LCG(long semilla) {
        reiniciar(semilla);
    }

    public static void validarSemilla(long semilla) {
        if (semilla < 0 || semilla >= M) {
            throw new IllegalArgumentException("la semilla debe cumplir 0 <= semilla < m");
        }
    }

    public void reiniciar(long semilla) {
        validarSemilla(semilla);
        this.estado = semilla & MASK;
    }

    public long getEstado() {
        return estado;
    }

    public long siguiente() {
        estado = (A * estado + C) & MASK;
        return estado;
    }

    public double siguienteNormalizado() {
        return siguiente() / (double) M;
    }
}
