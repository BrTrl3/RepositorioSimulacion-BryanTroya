package modelo;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

public final class Analisis {

    private Analisis() {
    }

    public static final class Estadisticas {
        public final int cantidad;
        public final double media;
        public final double desviacionEstandar;
        public final double minimo;
        public final double maximo;
        public final double correlacionLag1;
        public final int[] frecuencias;

        Estadisticas(int cantidad, double media, double desviacionEstandar, double minimo,
                     double maximo, double correlacionLag1, int[] frecuencias) {
            this.cantidad = cantidad;
            this.media = media;
            this.desviacionEstandar = desviacionEstandar;
            this.minimo = minimo;
            this.maximo = maximo;
            this.correlacionLag1 = correlacionLag1;
            this.frecuencias = frecuencias;
        }
    }

    public static final class Periodo {
        public final boolean mcdCUnoConM;
        public final boolean factoresPrimosDividenAMenos1;
        public final boolean divisiblePor4;
        public final boolean periodoCompleto;
        public final boolean sinRepeticionEnMuestra;
        public final int cantidadMuestra;

        Periodo(boolean mcdCUnoConM, boolean factoresPrimosDividenAMenos1, boolean divisiblePor4,
                boolean sinRepeticionEnMuestra, int cantidadMuestra) {
            this.mcdCUnoConM = mcdCUnoConM;
            this.factoresPrimosDividenAMenos1 = factoresPrimosDividenAMenos1;
            this.divisiblePor4 = divisiblePor4;
            this.periodoCompleto = mcdCUnoConM && factoresPrimosDividenAMenos1 && divisiblePor4;
            this.sinRepeticionEnMuestra = sinRepeticionEnMuestra;
            this.cantidadMuestra = cantidadMuestra;
        }
    }

    public static Estadisticas estadisticas(List<Registro> registros, int bins) {
        if (registros.isEmpty()) {
            throw new IllegalArgumentException("se requiere al menos un valor");
        }

        int cantidad = registros.size();
        double suma = 0.0;
        double minimo = Double.MAX_VALUE;
        double maximo = -Double.MAX_VALUE;
        int[] frecuencias = new int[bins];
        for (Registro registro : registros) {
            double u = registro.getU();
            suma += u;
            minimo = Math.min(minimo, u);
            maximo = Math.max(maximo, u);
            frecuencias[Math.min((int) (u * bins), bins - 1)]++;
        }
        double media = suma / cantidad;

        double sumaCuadrados = 0.0;
        for (Registro registro : registros) {
            double diferencia = registro.getU() - media;
            sumaCuadrados += diferencia * diferencia;
        }
        double desviacion = Math.sqrt(sumaCuadrados / cantidad);

        return new Estadisticas(cantidad, media, desviacion, minimo, maximo,
                correlacionLag1(registros), frecuencias);
    }

    private static double correlacionLag1(List<Registro> registros) {
        int pares = registros.size() - 1;
        if (pares < 1) {
            return 0.0;
        }

        double mediaX = 0.0;
        double mediaY = 0.0;
        for (int i = 0; i < pares; i++) {
            mediaX += registros.get(i).getU();
            mediaY += registros.get(i + 1).getU();
        }
        mediaX /= pares;
        mediaY /= pares;

        double covarianza = 0.0;
        double varianzaX = 0.0;
        double varianzaY = 0.0;
        for (int i = 0; i < pares; i++) {
            double dx = registros.get(i).getU() - mediaX;
            double dy = registros.get(i + 1).getU() - mediaY;
            covarianza += dx * dy;
            varianzaX += dx * dx;
            varianzaY += dy * dy;
        }
        if (varianzaX == 0.0 || varianzaY == 0.0) {
            return 0.0;
        }
        return covarianza / Math.sqrt(varianzaX * varianzaY);
    }

    public static Periodo periodo(List<Registro> registros) {
        // m = 2^32 tiene como unico factor primo al 2
        boolean mcd = mcd(LCG.C, LCG.M) == 1L;
        boolean factores = (LCG.A - 1L) % 2L == 0L;
        boolean cuatro = LCG.M % 4L != 0L || (LCG.A - 1L) % 4L == 0L;

        Set<Long> vistos = new HashSet<>();
        for (Registro registro : registros) {
            vistos.add(registro.getEstado());
        }
        boolean sinRepeticion = vistos.size() == registros.size();

        return new Periodo(mcd, factores, cuatro, sinRepeticion, registros.size());
    }

    private static long mcd(long a, long b) {
        while (b != 0L) {
            long resto = a % b;
            a = b;
            b = resto;
        }
        return a;
    }
}
