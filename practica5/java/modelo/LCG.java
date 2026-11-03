package modelo;

import java.util.ArrayList;
import java.util.List;

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

    public List<Registro> generar(int cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException("cantidad debe ser mayor que cero");
        }

        List<Registro> registros = new ArrayList<>(cantidad);
        for (int indice = 1; indice <= cantidad; indice++) {
            long valor = siguiente();
            registros.add(new Registro(indice, valor, valor / (double) M));
        }
        return registros;
    }
}
