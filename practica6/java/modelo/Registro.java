package modelo;

public final class Registro {
    private final long n;
    private final long estado;
    private final double u;

    public Registro(long n, long estado, double u) {
        this.n = n;
        this.estado = estado;
        this.u = u;
    }

    public long getN() {
        return n;
    }

    public long getEstado() {
        return estado;
    }

    public double getU() {
        return u;
    }
}
