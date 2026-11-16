# 🎯 Práctica 7 - Estimación de π mediante el método de Monte Carlo

**Materia:** Simulación
**Autor:** Bryan Troya

## 📖 1. Descripción del proyecto

Este proyecto aplica el **método de Monte Carlo** para aproximar el valor de π. Se generan `N` puntos aleatorios `(x, y)` en el cuadrado `[0,1) × [0,1)` y se cuentan los que caen dentro del cuarto de círculo de radio 1 (`x² + y² ≤ 1`):

```
π ≈ 4 · (Nc / N)
```

donde `Nc` es el número de puntos dentro del círculo y `N` el total de puntos generados.

El experimento se implementa en **Python y Java** con el **mismo generador congruencial lineal (LCG)** (`a = 1664525`, `c = 1013904223`, `m = 2³²`), de modo que con la misma semilla ambos programas producen exactamente la misma secuencia. Se ejecuta para `N = 1 000, 10 000, 100 000 y 1 000 000` y se comparan la estimación, el error absoluto y el tiempo de ejecución de cada lenguaje mediante cuadros estadísticos y gráficas.

## 🛠️ 2. Tecnologías utilizadas

| Tecnología | Versión | Uso |
| :--- | :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3.13-blue) | 3.13+ | Implementación principal y análisis |
| ![NumPy](https://img.shields.io/badge/NumPy-2.5.4-green) | 2.5.4 | Versión vectorizada y estadísticas |
| ![Pandas](https://img.shields.io/badge/Pandas-3.1.1-purple) | 3.1.1 | Cuadros estadísticos comparativos |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-orange) | 3.11.2 | Gráficas |
| ![Java](https://img.shields.io/badge/Java-11+-red) | JDK 11+ | Implementación cruzada |

> Ambas implementaciones siguen el patrón **MVC** (Modelo - Vista - Controlador).

## ⚙️ 3. Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git
cd RepositorioSimulacion-BryanTroya/practica7
```

2. Crear y activar el entorno virtual:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Verificar que el JDK esté instalado (`javac -version`).

## 🚀 4. Configuración y Uso

Desde la carpeta `practica7`, ejecutar ambas versiones y generar la comparación:

```bash
python -m python.main --java
```

| Opción | Valor por defecto | Descripción |
| :--- | :--- | :--- |
| `--java` | desactivado | Compila y ejecuta la versión Java antes del análisis |
| `--semilla` | `12345` | Semilla del LCG (la misma se pasa a Java) |
| `--repeticiones` | `5` | Repeticiones para promediar los tiempos |

La versión Java también puede ejecutarse por separado:

```bash
javac -encoding UTF-8 -d java/out java/src/Main.java java/src/modelo/*.java java/src/vista/*.java java/src/controlador/*.java
java -cp java/out Main 12345 5 resultados/java
```

El programa muestra los cuadros en consola y guarda en `resultados/`:

- Cuadros en CSV y todos juntos en `cuadros_estadisticos.md`.
- Gráficas en `resultados/graficas/`: dispersión de puntos, convergencia, error vs. N, tiempos y variabilidad con 30 semillas.

## 📁 5. Estructura del proyecto

```
practica7/
├── python/
│   ├── main.py                  # Punto de entrada (argumentos de línea de comandos)
│   ├── modelo/
│   │   ├── lcg.py               # Generador congruencial lineal
│   │   └── montecarlo.py        # Estimación de π, tiempos y réplicas
│   ├── controlador/
│   │   └── controlador.py       # Orquesta Python, Java, cuadros y gráficas
│   └── vista/
│       ├── consola.py           # Salida por consola
│       ├── reportes.py          # Cuadros estadísticos (Pandas, CSV, Markdown)
│       └── graficas.py          # Gráficas con Matplotlib
├── java/src/
│   ├── Main.java                # Punto de entrada Java
│   ├── modelo/                  # LCG.java, MonteCarlo.java
│   ├── controlador/             # MonteCarloController.java
│   └── vista/                   # Consola.java, ReporteCsv.java
├── resultados/                  # Salidas generadas (CSV, Markdown, PNG)
├── requirements.txt
└── README.md
```

## ℹ️ 6. Información adicional

### ✨ Características clave

- **Mismo LCG en ambos lenguajes**: la secuencia y el número de puntos dentro del círculo coinciden exactamente; el programa lo verifica en un cuadro.
- **Tiempos promediados** en varias repeticiones; en Java se hace una corrida de calentamiento para el compilador JIT.
- **Versión NumPy** vectorizada como referencia adicional de rendimiento.
- **Análisis con 30 semillas** para estudiar la variabilidad del estimador frente al error estándar teórico.

### 📄 Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
