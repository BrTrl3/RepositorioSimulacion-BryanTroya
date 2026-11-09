# 📊 Práctica 6 - Validación Estadística de Números Pseudoaleatorios

**Materia:** Simulación
**Autor:** Bryan Troya

## 📖 1. Descripción del proyecto

Este proyecto evalúa la calidad estadística de secuencias de números **pseudoaleatorios** generadas con el método congruencial lineal (LCG), mediante dos pruebas de bondad de ajuste:

```
H0: X ~ U(0,1)      H1: X no sigue U(0,1)      α = 0.05
```

- **Chi-cuadrado:** compara las frecuencias observadas con las esperadas en 10 intervalos.
- **Kolmogorov-Smirnov:** compara la distribución acumulada empírica con la teórica.

El propósito es **determinar si los valores generados son compatibles con una distribución uniforme en [0, 1]** y comparar el comportamiento de distintas configuraciones del generador. Además, se estima π con el generador para comparar los tiempos de ambos lenguajes.

La práctica se implementa en **Python** y en **Java**.

## 🛠️ 2. Tecnologías utilizadas

| Tecnología | Versión | Uso |
| :--- | :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3.10+-blue) | 3.10+ | Lenguaje principal |
| ![NumPy](https://img.shields.io/badge/NumPy-1.24+-green) | 1.24+ | Operaciones numéricas |
| ![Pandas](https://img.shields.io/badge/Pandas-2.0+-purple) | 2.0+ | Tablas y archivos CSV |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-orange) | 3.7+ | Gráficas |
| Java (JDK) | 11+ | Implementación equivalente |
| unittest | estándar | Pruebas automatizadas |

> El proyecto sigue el patrón de arquitectura **MVC** (Modelo - Vista - Controlador) tanto en Python como en Java.

## ⚙️ 3. Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git
cd RepositorioSimulacion-BryanTroya/practica6
```

2. Crear y activar el entorno virtual:

```bash
# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Verificar que Java esté instalado (necesario para la versión Java y la comparación):

```bash
java -version
javac -version
```

## 🚀 4. Configuración y Uso

### Python

Ejecutar desde la carpeta `practica6`:

```bash
python python/main.py
```

Al ejecutar, el programa aplica las pruebas a cada configuración del generador, compila y ejecuta automáticamente la versión Java (si está instalada), compara ambos lenguajes, muestra los resultados por consola y guarda los archivos en `resultados/`.

Opciones disponibles:

| Opción | Por defecto | Descripción |
| :--- | :--- | :--- |
| `--cantidad` | `10000` | Cantidad de valores por configuración |
| `--intervalos` | `10` | Intervalos de la prueba Chi-cuadrado |
| `--salida` | `resultados/` | Carpeta de salida |
| `--sin-java` | — | No ejecuta la versión Java |
| `--sin-graficas` | — | No genera las gráficas |

### Java

Compilar y ejecutar desde la carpeta `practica6`:

```bash
javac -encoding UTF-8 -d java -sourcepath java java/Main.java
java -cp java Main
```

Opciones disponibles: `--count`, `--bins`, `--output-dir` y `--help`.

### Pruebas

```bash
python -m unittest discover -s python/tests -t python -v
```

## 📁 5. Estructura del proyecto

```
practica6/
├── python/                       # Implementación en Python (MVC)
│   ├── main.py                   #   Punto de entrada
│   ├── model/                    #   🧠 Modelo
│   │   ├── lcg.py                #     Generador y configuraciones
│   │   ├── pruebas.py            #     Chi-cuadrado y Kolmogorov-Smirnov
│   │   ├── montecarlo.py         #     Estimación de π
│   │   └── comparacion.py        #     Comparación Python vs Java
│   ├── controller/               #   🎮 Controlador
│   │   └── practica_controller.py #    Orquesta el modelo y la versión Java
│   ├── view/                     #   🖥️ Vista
│   │   ├── consola.py            #     Salida por consola
│   │   ├── graficas.py           #     Gráficas con Matplotlib
│   │   └── reportes.py           #     Exportación a CSV con Pandas
│   └── tests/                    #   Pruebas automatizadas
├── java/                         # Implementación en Java (MVC)
│   ├── Main.java                 #   Punto de entrada
│   ├── modelo/                   #   LCG, pruebas y estimación de π
│   ├── controlador/              #   PracticaController
│   └── vista/                    #   Consola y ReporteCsv
├── resultados/                   # Gráficas y CSV generados al ejecutar
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                    # Archivos ignorados por Git
└── README.md                     # Este archivo
```

## ℹ️ 6. Información adicional

### ✨ Características clave

- Patrón **MVC** separado en Python y en Java.
- Estadísticos y valores p calculados con la misma implementación en ambos lenguajes.
- Seis configuraciones del generador para comparar su comportamiento.
- Comparación automática Python vs Java en `resultados/`.
- Gráficas guardadas automáticamente en `resultados/`.

### 📄 Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
