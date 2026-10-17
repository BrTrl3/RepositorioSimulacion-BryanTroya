# Práctica 3: Simulación de un Sistema de Líneas de Espera M/M/1

**Materia:** Simulación  
**Carrera:** Computación  
**Universidad Nacional de Loja**  
**Autor:** Bryan Troya

## 1. Descripción del proyecto

Esta práctica consiste en la simulación de un sistema de líneas de espera con un único servidor, modelado mediante la teoría de colas **M/M/1**. Se implementó una aplicación en **Python** que utiliza **SimPy** para simular eventos discretos, calcula las métricas teóricas, las compara con las métricas obtenidas experimentalmente y presenta los resultados mediante una interfaz web local desarrollada con **Streamlit**.

El objetivo es comprobar que una simulación de eventos discretos reproduce, de manera coherente, el comportamiento descrito por la teoría de colas, permitiendo visualizar la evolución de la cola, la distribución de los tiempos de espera y el desempeño del sistema bajo distintos escenarios.

## 2. Tecnologías utilizadas

| Tecnología | Uso dentro del proyecto |
|-------------|--------------------------|
| **Python**     | Lenguaje de programación principal. |
| **SimPy**      | Motor de simulación de eventos discretos (gestión del reloj, llegadas, recurso servidor y atención). |
| **NumPy**      | Generación de variables aleatorias exponenciales y cálculos estadísticos. |
| **Matplotlib** | Construcción de gráficas (evolución de la cola, histogramas y comparaciones entre escenarios). |
| **Streamlit**  | Interfaz gráfica web local en español, interactiva y sencilla. |
| **unittest**   | Pruebas automatizadas utilizando la biblioteca estándar de Python. |

## 3. Instalación

### 3.1. Requisitos previos

- **Python 3.12 o superior** (verificado con Python 3.12 y 3.14).
- **pip** actualizado.
- Conexión a internet **únicamente** para instalar las dependencias. Una vez instaladas, la aplicación funciona sin conexión.

Para comprobar tu versión de Python:

```bash
python --version
```

En Windows puedes usar el lanzador `py`: `py -3.12 -m venv .venv`

### 3.2. Clonar y acceder al proyecto

```bash
# Clonar el repositorio (si aún no lo tienes)
git clone https://github.com/BryanTroya/RepositorioSimulacion-BryanTroya.git

# Acceder a la carpeta de la práctica
cd RepositorioSimulacion-BryanTroya/practica3
```

## 4. Configuración y Uso

### 4.1. Crear y activar el entorno virtual

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Símbolo del sistema / CMD)**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

> **Importante:** Si el `.venv` ya existía con una versión distinta de Python, es recomendable eliminarlo y crear uno nuevo desde cero para evitar errores de dependencias.

Al activar correctamente, verás `(.venv)` al inicio de la línea de comandos. Para salir, usa `deactivate`.

### 4.2. Instalar dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**

```text
simpy==4.1.2
numpy==2.5.4
matplotlib==3.11.2
streamlit==1.66.0
```

### 4.3. Ejecutar las pruebas

Las pruebas se ejecutan con `unittest`, sin necesidad de instalar paquetes adicionales.

```bash
# Desde la raíz de practica3 con el entorno virtual activado
python -m unittest -v
```

También puedes usar descubrimiento explícito:

```bash
python -m unittest discover -s tests -t . -v
```

**Resultado esperado:** 20 pruebas ejecutadas, todas correctas (`OK`).

### 4.4. Iniciar la aplicación

```bash
streamlit run app.py
```

Streamlit mostrará una dirección local similar a:

```text
Local URL: http://localhost:8501
```

Abre esa URL en tu navegador. Para detener la aplicación, presiona `Ctrl + C` en la terminal.

### 4.5. Uso básico de la interfaz

1. **Panel de configuración (barra lateral):**
   - Seleccionar escenario: *Escenario 1*, *Escenario 2*, *Escenario 3* o *Comparar los tres escenarios*.
   - *Cantidad de clientes*: valor predeterminado 1000. A mayor cantidad, los resultados se acercan más a los valores teóricos.
   - *Semilla aleatoria*: valor predeterminado 42. Reutilizar la misma semilla garantiza reproducibilidad.
   - Pulsar **Iniciar simulación** para ejecutar el modelo.

2. **Resultados principales:** Tarjetas con utilización teórica, tiempo promedio de espera simulado (Wq), tamaño promedio de la cola simulado (Lq) y número de clientes atendidos.

3. **Tabla comparativa:** Muestra valores teóricos y simulados para cada escenario. Las columnas con sufijo *teórica* provienen de las fórmulas; el resto provienen de la simulación.

4. **Visualización:** Evolución del tamaño de la cola, histograma de tiempos de espera y, al comparar los tres escenarios, gráficas comparativas de Wq y Lq.

5. **Datos de clientes:** Sección desplegable con la tabla individual de cada cliente (llegada, inicio de servicio, espera, servicio, salida y tiempo en el sistema). Se muestran como máximo los primeros 200 clientes.

## 5. Estructura del proyecto

```text
practica3/
│
├── app.py                        # Punto de entrada de Streamlit
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                    # Archivos a ignorar por Git
├── README.md                     # Documentación de la práctica
├── ANALISIS_CUMPLIMIENTO_GUIA.md # Análisis de cumplimiento de la guía
├── PROMPT MAESTRO PARA OPENCODE= PRÁCTICA 03 DE SIMULACIÓN MM1.md
├── REGLAS_EQUIPO.md              # Reglas de trabajo colaborativo
│
├── controller/                   # Capa Controlador (MVC)
│   ├── __init__.py
│   └── simulation_controller.py  # Escenarios, validación y tabla comparativa
│
├── model/                        # Capa Modelo (MVC)
│   ├── __init__.py
│   ├── metrics.py                # Métricas teóricas y validación de tasas
│   └── queue_model.py            # Simulación de eventos discretos con SimPy
│
├── view/                         # Capa Vista (MVC)
│   ├── __init__.py
│   └── dashboard.py              # Encabezado, controles, tablas y gráficas
│
├── tests/                        # Pruebas automatizadas
│   ├── __init__.py
│   ├── test_metrics.py           # Pruebas de métricas teóricas
│   └── test_simulation.py        # Pruebas de simulación, controlador y arquitectura MVC
│
└── __pycache__/                  # Archivos compilados (generados automáticamente)
```

## 6. Información adicional

### 6.1. Descripción del modelo M/M/1

- **Primera M:** Tiempos entre llegadas con distribución exponencial (proceso de Poisson).
- **Segunda M:** Tiempos de servicio con distribución exponencial.
- **1:** Un único servidor.
- **Disciplina FIFO:** Primero en llegar, primero en ser atendido.
- **Unidad de tiempo consistente:** Llegadas y servicios usan la misma unidad (ej., minutos).

Cada cliente registra: `customer_id`, `arrival_time`, `service_start`, `waiting_time`, `service_duration`, `departure_time` y `system_time`.

### 6.2. Parámetros y escenarios obligatorios

| Parámetro | Significado |
|------------|-------------|
| `lambda_rate` (λ) | Tasa media de llegada (clientes por unidad de tiempo) |
| `mu_rate` (μ)     | Tasa media de servicio (clientes por unidad de tiempo) |
| `num_customers`   | Cantidad de clientes generados por ejecución |
| `seed`            | Semilla del generador aleatorio para reproducir resultados |

| Escenario | λ   | μ   | Característica        | ρ = λ/μ |
|------------|-----|-----|------------------------|----------|
| 1          | 2.0 | 3.0 | Sistema estable       | 0.667    |
| 2          | 2.5 | 3.0 | Mayor utilización     | 0.833    |
| 3          | 2.9 | 3.0 | Cerca de la saturación| 0.967    |

### 6.3. Fórmulas de las métricas teóricas

Calculadas en `model/metrics.py`, únicamente cuando λ < μ:

| Métrica | Fórmula |
|----------|---------|
| Utilización del servidor (ρ) | `ρ = λ / μ` |
| Clientes promedio en el sistema (L) | `L = λ / (μ − λ)` |
| Clientes promedio en la cola (Lq) | `Lq = λ² / (μ · (μ − λ))` |
| Tiempo promedio en el sistema (W) | `W = 1 / (μ − λ)` |
| Tiempo promedio en la cola (Wq) | `Wq = λ / (μ · (μ − λ))` |
| Condición de estabilidad | `λ < μ` |

### 6.4. Arquitectura MVC

| Módulo | Responsabilidad |
|--------|-----------------|
| `app.py` | Punto de entrada. Conecta vista y controlador. |
| `model/queue_model.py` | Simulación con SimPy, generación de clientes e integración temporal de cola/servidor. |
| `model/metrics.py` | Cálculo de métricas teóricas y validación de tasas. |
| `controller/simulation_controller.py` | Define escenarios, valida parámetros, ejecuta modelo y prepara tabla comparativa. |
| `view/dashboard.py` | Renderiza encabezado, panel, tarjetas, tablas, gráficas y sección educativa. |
| `tests/` | Pruebas unitarias: métricas, simulación, controlador y separación MVC. |

**Principios:** El modelo no depende de Streamlit. El controlador no dibuja. La vista no simula. Esta separación se valida en `tests/test_simulation.py`.

### 6.5. Decisiones de simulación

- **Cantidad fija de clientes:** Se generan exactamente `num_customers` y la simulación avanza hasta que todos terminen su servicio.
- **Intervalo de observación [0, T]:** `T` es el instante en que el último cliente termina su servicio. Sobre este intervalo se calculan Lq y la utilización experimental.
- **Tamaño promedio de la cola (Lq):** Medición temporal mediante integración del número de clientes esperando a lo largo del tiempo (área / T), actualizada con eventos reales.
- **Utilización experimental:** Área de tiempo ocupado / T.
- **Aleatoriedad reproducible:** Cada ejecución usa `numpy.random.default_rng(seed)`. Al comparar los tres escenarios se mantiene la misma semilla y cantidad de clientes.
- **Consistencia:** `waiting_time = service_start - arrival_time`, `system_time = departure_time - arrival_time`. El servidor nunca atiende a dos clientes simultáneamente.

### 6.6. Gráficas obligatorias

- Evolución del tamaño de la cola durante la simulación (con referencia teórica de Lq cuando aplica).
- Histograma de los tiempos de espera con líneas de referencia (Wq teórica y promedio simulado).
- Comparación del tiempo promedio de espera simulado entre los tres escenarios.
- Comparación del tamaño promedio de la cola simulado entre los tres escenarios.

### 6.7. Pruebas implementadas

Se verifican: fórmulas teóricas para λ=2.0, μ=3.0; utilización = λ/μ; rechazo de sistema inestable (λ≥μ); generación correcta de clientes; todos atendidos; coherencia de tiempos; capacidad del servidor = 1; reproducibilidad con misma semilla; valores no negativos/coherentes; ejecución correcta de los tres escenarios obligatorios y validación de parámetros inválidos.

### 6.8. Limitaciones del modelo

- **Variabilidad aleatoria:** Resultados varían entre ejecuciones. Más clientes → mayor aproximación a la teoría.
- **Periodo transitorio:** La simulación parte con servidor vacío, lo que suele dar promedios ligeramente inferiores a los teóricos en estado estacionario.
- **Cerca de saturación (ρ→1):** Mayor sensibilidad al azar; se requieren simulaciones largas.
- **Delimitación:** Promedios temporales calculados en `[0,T]`. Otras delimitaciones pueden dar resultados ligeramente distintos.
- **Alcance:** No considera cola con capacidad finita, prioridades, múltiples servidores, abandono ni tiempos no exponenciales.

> **Importante:** No se exige coincidencia exacta con la teoría. Se busca coherencia y aproximación razonable cuando el número de clientes es suficiente.

### 6.9. Uso de Git y recomendaciones colaborativas

- **No subir al repositorio:** `.venv/`, `venv/`, `env/`, `__pycache__/`, archivos `.pyc`, cachés, temporales ni archivos locales.
- **Sí incluir:** código fuente, pruebas, `requirements.txt`, `.gitignore` y `README.md`.
- **Flujo sugerido:** Trabajar con ramas individuales (`feature/nombre_integrante`), integrar a `develop` y luego a `main` según acuerdo del grupo.
- **Buenas prácticas:** Revisar `git status`/`git diff` antes de cada commit. No subir secretos ni datos personales.
- **IA documentada:** La asistencia de IA debe registrarse en este README, no como autor de commits.

### 6.10. Declaración del uso de inteligencia artificial

- **Herramienta utilizada:** [OpenCode](https://opencode.ai), asistente de programación basado en IA, ejecutado en terminal.
- **Uso dado:** Apoyo en estructuración (MVC), implementación (modelo SimPy, métricas, controlador, vista Streamlit/Matplotlib), redacción de pruebas, redacción de este README y revisión/corrección de errores.
- **Supervisión humana:** Los integrantes deben comprender cada archivo, ejecutar pruebas, verificar que resultados provienen de ejecución real y validar valores antes de presentar.
- **Integridad:** Ningún resultado fue inventado. Todo dato mostrado se calcula al ejecutar la aplicación.
- **Prompt principal:** Transcrito íntegramente en el **Anexo A**.

## 7. Flujo secuencial

**¿Qué hace → Tecnologías → Instalación → Configuración y Uso → Estructura del proyecto → Información adicional**

---

## Anexo A. Prompt maestro utilizado con la IA

> El siguiente texto corresponde al prompt maestro completo entregado a OpenCode para generar este proyecto. Su contenido se conserva íntegramente para garantizar trazabilidad del uso de IA.

<!-- PROMPT_MAESTRO_INICIO -->

*(Se omite aquí la transcripción completa del prompt maestro por brevedad, ya que se encuentra disponible en el archivo `PROMPT MAESTRO PARA OPENCODE= PRÁCTICA 03 DE SIMULACIÓN MM1.md` ubicado en esta misma carpeta. Dicho archivo contiene el prompt íntegro utilizado durante el desarrollo.)*

<!-- PROMPT_MAESTRO_FIN -->