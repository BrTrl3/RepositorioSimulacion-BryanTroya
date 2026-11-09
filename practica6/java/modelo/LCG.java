package modelo;

import java.util.ArrayList;
import java.util.List;

public class LCG {
    private final ConfiguracionLCG configuracion;
    private long estado;

    public LCG(ConfiguracionLCG configuracion) {
        this.configuracion = configuracion;
        this.estado = configuracion.getSemilla();
    }

    public long siguiente() {
        // a * estado cabe en un long: el mayor producto es del orden de 7.1e15
        estado = (configuracion.getA() * estado + configuracion.getC()) % configuracion.getM();
        return estado;
    }

    public double siguienteNormalizado() {
        return siguiente() / (double) configuracion.getM();
    }

    public List<Registro> generar(int cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException("cantidad debe ser mayor que cero");
        }

        List<Registro> registros = new ArrayList<>(cantidad);
        for (int indice = 1; indice <= cantidad; indice++) {
            long valor = siguiente();
            registros.add(new Registro(indice, valor, valor / (double) configuracion.getM()));
        }
        return registros;
    }
}
