package modelo;

import java.util.List;

public final class ConfiguracionLCG {
    public static final List<ConfiguracionLCG> CONFIGURACIONES = List.of(
        new ConfiguracionLCG("Guia semilla 12345", 1664525L, 1013904223L, 1L << 32, 12345L),
        new ConfiguracionLCG("Guia semilla 54321", 1664525L, 1013904223L, 1L << 32, 54321L),
        new ConfiguracionLCG("MINSTD", 16807L, 0L, (1L << 31) - 1L, 12345L),
        new ConfiguracionLCG("RANDU", 65539L, 0L, 1L << 31, 12345L),
        new ConfiguracionLCG("Periodo corto", 5L, 3L, 16L, 1L),
        new ConfiguracionLCG("Multiplicador a=1", 1L, 1000L, 1L << 32, 12345L)
    );

    private final String nombre;
    private final long a;
    private final long c;
    private final long m;
    private final long semilla;

    public ConfiguracionLCG(String nombre, long a, long c, long m, long semilla) {
        if (a <= 0) {
            throw new IllegalArgumentException("a debe ser mayor que cero");
        }
        if (c < 0) {
            throw new IllegalArgumentException("c no puede ser negativo");
        }
        if (m <= 1) {
            throw new IllegalArgumentException("m debe ser mayor que uno");
        }
        if (semilla < 0 || semilla >= m) {
            throw new IllegalArgumentException("la semilla debe cumplir 0 <= semilla < m");
        }
        this.nombre = nombre;
        this.a = a;
        this.c = c;
        this.m = m;
        this.semilla = semilla;
    }

    public String getNombre() {
        return nombre;
    }

    public long getA() {
        return a;
    }

    public long getC() {
        return c;
    }

    public long getM() {
        return m;
    }

    public long getSemilla() {
        return semilla;
    }
}
