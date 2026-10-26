# 🦠 Práctica 4 - Simulación del Modelo SIR con Python y SimPy

**Materia:** Simulación  
**Carrera:** Computación  
**Universidad Nacional de Loja**  
**Autor:** Bryan Troya

## 1. Descripción del proyecto

Esta práctica implementa el **modelo SIR** (*Susceptibles, Infectados y Recuperados*) mediante una **simulación de eventos discretos por agentes** desarrollada en **Python** con **SimPy**.

Cada individuo de la población se representa como un agente con uno de tres estados posibles. En cada paso de tiempo los infectados buscan contactos, pueden contagiar a susceptibles y luego pueden recuperarse según las probabilidades configuradas. La simulación registra la evolución completa del sistema y genera:

- Un archivo **CSV** con el historial de la simulación, compatible con **NetLogo**.
- Una **gráfica PNG** con las curvas de susceptibles, infectados y recuperados.
- Un **resumen por consola** con el pico de infectados, el estado final y el tiempo de cómputo.

El objetivo es analizar cómo evoluciona una epidemia bajo distintos valores de transmisión (`beta`) y recuperación (`gamma`), verificando que se conserva la población y que los resultados son reproducibles mediante una semilla.

## 2. Tecnologías utilizadas

| Tecnología | Uso dentro del proyecto |
|-------------|--------------------------|
| **Python**     | Lenguaje de programación principal. |
| **SimPy**      | Motor de simulación de eventos discretos y avance del reloj por pasos. |
| **NumPy**      | Construcción de los arreglos numéricos para la gráfica. |
| **Matplotlib** | Generación de la gráfica de evolución del modelo SIR. |
| **csv**        | Exportación del historial en formato compatible con NetLogo. |
| **unittest**   | Pruebas automatizadas con la biblioteca estándar de Python. |
| **NetLogo**    | Herramienta complementaria para los modelos basados en agentes de la práctica. |

## 3. Instalación

### 3.1. Requisitos previos

- **Python 3.10 o superior**.
- **pip** actualizado.
- Conexión a internet **únicamente** para instalar las dependencias.

Para comprobar tu versión de Python:

```bash
python --version
```

### 3.2. Clonar y acceder al proyecto

```bash
# Clonar el repositorio (si aún no lo tienes)
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git

# Acceder a la carpeta de la práctica
cd RepositorioSimulacion-BryanTroya/practica4
```

### 3.3. Crear y activar el entorno virtual

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

### 3.4. Instalar dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**

```text
simpy>=4.1,<5
numpy>=1.24,<3
matplotlib>=3.7,<4
```

## 4. Configuración y Uso

### 4.1. Ejecución básica

Desde la carpeta `practica4`, con el entorno virtual activado:

```bash
python main.py
```

La ejecución predeterminada usa los valores de la guía y genera los resultados en las carpetas `datos/` y `graficas/`.

### 4.2. Parámetros predeterminados

| Parámetro | Valor | Descripción |
| :--- | :--- | :--- |
| `poblacion` | 100 | Cantidad total de agentes (`N`). |
| `infectados_iniciales` | 5 | Agentes infectados en `t = 0`. |
| `beta` | 0.30 | Probabilidad de contagio por contacto con un susceptible. |
| `gamma` | 0.10 | Probabilidad de recuperación de un infectado por paso. |
| `pasos` | 100 | Cantidad de pasos simulados. |
| `contactos_por_infectado` | 1 | Contactos elegidos por cada infectado en cada paso. |
| `semilla` | 42 | Semilla del generador aleatorio para reproducir resultados. |

Con estos valores la población inicial es `S = 95`, `I = 5`, `R = 0`. La relación `beta / gamma = 3` se usa como referencia teórica, no como un resultado exacto exigible a una corrida aleatoria.

### 4.3. Opciones de línea de comandos

| Opción | Descripción |
| :--- | :--- |
| `--poblacion` | Tamaño de la población. |
| `--infectados` | Infectados iniciales. |
| `--beta` | Probabilidad de contagio. |
| `--gamma` | Probabilidad de recuperación. |
| `--pasos` | Cantidad de pasos de simulación. |
| `--contactos` | Contactos por infectado en cada paso. |
| `--semilla` | Semilla del generador aleatorio. |
| `--salida` | Carpeta donde se escribe `resultados_python.csv`. |
| `--graficas` | Carpeta donde se escribe `sir_evolucion.png`. |

Para consultar todas las opciones disponibles:

```bash
python main.py --help
```

### 4.4. Archivos generados

| Archivo | Contenido |
| :--- | :--- |
| `datos/resultados_python.csv` | Encabezado y 101 registros, desde `t = 0` hasta `t = 100`. |
| `graficas/sir_evolucion.png` | Gráfica con las tres curvas de evolución. |

Con la configuración predeterminada y semilla 42, una ejecución de ejemplo produce un pico de **33 infectados en `t = 16`** y un estado final de **`S = 10`, `I = 0`, `R = 90`**. Al repetir la ejecución con la misma semilla se obtienen exactamente los mismos resultados.

## 5. Estructura del proyecto

```text
practica4/
│
├── main.py                       # Punto de entrada y opciones de línea de comandos
├── config.py                     # Valores predeterminados y validación de parámetros
├── requirements.txt              # Dependencias del proyecto
├── APE 4-Bryan-Troya.pdf         # Informe de la práctica
├── README.md                     # Documentación de la práctica
│
├── modelo/                       # Lógica del modelo SIR
│   ├── __init__.py
│   ├── poblacion.py              # Estados, creación y conteo de la población
│   └── transiciones.py           # Contagios y recuperaciones por paso
│
├── simulacion/                   # Motor de simulación
│   ├── __init__.py
│   └── motor.py                  # Pasos temporizados con SimPy y validación
│
├── resultados/                   # Salidas de la simulación
│   ├── __init__.py
│   ├── exportador.py             # Exportación del CSV para NetLogo
│   └── graficas.py               # Gráfica de evolución con Matplotlib
│
├── pruebas/                      # Pruebas automatizadas
│   ├── __init__.py
│   └── test_sir.py               # Pruebas del modelo, motor y exportación
│
├── datos/                        # CSV y modelos NetLogo
└── graficas/                     # Gráfica generada
```

## 6. Modelo y reglas de simulación

- Cada agente tiene uno de tres estados: **susceptible**, **infectado** o **recuperado**.
- Los `infectados_iniciales` se seleccionan aleatoriamente entre los `N` agentes.
- En cada paso, cada infectado del estado anterior elige `k` contactos **distintos** entre los demás agentes.
- Si un contacto era susceptible, se contagia con probabilidad `beta`.
- Cada infectado original se recupera con probabilidad `gamma`.
- Los cambios se escriben en una **copia del estado** y se aplican de forma **simultánea**: un nuevo infectado no contagia ni se recupera hasta el paso siguiente.
- Un agente contagiado por varios infectados se cuenta **una sola vez**.
- Siempre se verifica que `N = S + I + R`; los susceptibles no aumentan y los recuperados no disminuyen.
- No hay nacimientos, muertes ni reinfecciones.
- La simulación continúa registrando hasta `t = 100` aunque ya no existan infectados.
- La selección de un solo contacto por infectado (`k = 1`) es una decisión explícita, ya que la guía no especifica la cantidad de contactos. Se mantiene para la corrida evaluada.

## 7. CSV para NetLogo

El contrato de datos es el siguiente:

```csv
tiempo,susceptibles,infectados,recuperados
0,95,5,0
```

El archivo se escribe en **UTF-8**, separado por comas, con encabezado y cuatro columnas enteras, sin índice adicional.

Para copiar el CSV a la carpeta del modelo NetLogo o generarlo directamente allí:

```bash
python main.py --salida "/ruta/al/proyecto/netlogo"
```

NetLogo debe saltar el encabezado y leer las columnas en ese orden. El CSV contiene todo lo necesario para graficar las tres series; el PNG no se importa. Este proyecto no crea ni modifica archivos NetLogo.

## 8. Pruebas automatizadas

Las pruebas se ejecutan con `unittest`, sin necesidad de instalar paquetes adicionales:

```bash
python -m unittest discover -s pruebas -v
```

**Resultado esperado:** 17 pruebas ejecutadas, todas correctas (`OK`).

Se verifican, entre otros aspectos:

- Condición inicial `S = 95`, `I = 5`, `R = 0`.
- Validación de parámetros inválidos y tipos incorrectos.
- Contagios, recuperaciones y actualización simultánea del estado.
- Reproducibilidad con la misma semilla.
- Conservación de la población en todos los registros.
- Generación correcta de los 101 registros y del CSV con formato NetLogo.
- Comportamiento sin infectados, con cero pasos y con extinción de la infección.
- Error controlado cuando SimPy no está instalado.

## 9. Limitaciones del modelo

- **Variabilidad aleatoria:** los resultados cambian entre ejecuciones con semillas distintas.
- **Un contacto por infectado:** se mantiene la decisión de `k = 1`; con más contactos la propagación sería más rápida.
- **Tiempo discreto:** los contagios y recuperaciones se evalúan por pasos, no de forma continua.
- **Sin estructura espacial:** cualquier agente puede ser elegido como contacto, sin redes ni vecindarios.
- **Sin demografía ni reinfección:** no se consideran nacimientos, muertes ni pérdida de inmunidad.
- **Comparación con ecuaciones diferenciales:** el modelo por agentes no resuelve directamente las ecuaciones del SIR; `beta / gamma = 3` es solo una referencia teórica.

### 📄 Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
