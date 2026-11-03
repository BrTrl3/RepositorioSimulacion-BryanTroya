# 🎲 Práctica 5 - Generador Congruencial Lineal (LCG) en Python y Java

**Materia:** Simulación
**Autor:** Bryan Troya

## 📖 1. Descripción del proyecto

Este proyecto implementa un **Generador Congruencial Lineal (LCG)**, un método para generar números **pseudoaleatorios**, con la relación:

```
X(n+1) = (a · X(n) + c) mod m
U(n)   = X(n) / m
```

usando los parámetros de la guía: `a = 1664525`, `c = 1013904223`, `m = 2^32` y semilla `12345`.

El propósito es **implementar el mismo algoritmo en Python y en Java y comprobar que ambos producen la misma secuencia**. El programa genera 10 000 valores, compara las primeras observaciones de ambos lenguajes, grafica la secuencia, analiza el período y compara los resultados al cambiar la semilla.

La práctica se implementa en **Python** y en **Java**.

## 🛠️ 2. Tecnologías utilizadas

| Tecnología | Versión | Uso |
| :--- | :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3.10+-blue) | 3.10+ | Lenguaje principal |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-orange) | 3.7+ | Gráficas de la secuencia |
| Java (JDK) | 11+ | Implementación equivalente del generador |
| unittest | estándar | Pruebas automatizadas |

> El proyecto sigue el patrón de arquitectura **MVC** (Modelo - Vista - Controlador) tanto en Python como en Java.

## ⚙️ 3. Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git
cd RepositorioSimulacion-BryanTroya/practica5
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

Ejecutar desde la carpeta `practica5`:

```bash
python main.py
```

Al ejecutar, el programa genera las secuencias, compila y ejecuta automáticamente la versión Java (si está instalada), muestra los resultados por consola y guarda los archivos en `resultados/`.

Opciones disponibles:

| Opción | Por defecto | Descripción |
| :--- | :--- | :--- |
| `--semilla` | `12345` | Semilla principal |
| `--semilla-alternativa` | `54321` | Semilla para la comparación |
| `--cantidad` | `10000` | Cantidad de valores a generar |
| `--salida` | `resultados/` | Carpeta de salida |
| `--sin-java` | — | No ejecuta la versión Java |
| `--sin-graficas` | — | No genera las gráficas |

Ejemplo:

```bash
python main.py --semilla 999 --cantidad 5000
```

### Java

Compilar y ejecutar desde la carpeta `practica5`:

```bash
javac -encoding UTF-8 -d java java/Main.java java/modelo/*.java java/controlador/*.java java/vista/*.java
java -cp java Main
```

Opciones disponibles: `--seed`, `--alt-seed`, `--count`, `--output` y `--help`.

```bash
java -cp java Main --seed 12345 --count 10000
```

### Pruebas

```bash
python -m unittest discover -s tests -v
```

## 📁 5. Estructura del proyecto

```
practica5/
├── main.py                  # Punto de entrada (Python)
├── model/                   # 🧠 Modelo (MVC)
│   ├── lcg.py               #   Generador congruencial lineal
│   └── analysis.py          #   Estadísticas, período y comparaciones
├── controller/              # 🎮 Controlador (MVC)
│   └── lcg_controller.py    #   Orquesta el modelo, la vista y la versión Java
├── view/                    # 🖥️ Vista (MVC)
│   ├── consola.py           #   Salida por consola
│   ├── graficas.py          #   Gráficas con Matplotlib
│   └── reportes.py          #   Exportación a CSV
├── java/                    # Implementación en Java (MVC)
│   ├── Main.java            #   Punto de entrada
│   ├── modelo/              #   LCG, Registro y Analisis
│   ├── controlador/         #   LCGController
│   └── vista/               #   Consola y ReporteCsv
├── tests/                   # Pruebas automatizadas
├── resultados/              # Gráficas y CSV generados al ejecutar
├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

## ℹ️ 6. Información adicional

### ✨ Características clave

- Patrón **MVC** separado en Python y en Java.
- La misma secuencia en ambos lenguajes: en Java se usa `long` con máscara de 32 bits para evitar desbordamientos.
- Comparación automática Python vs Java en `resultados/comparacion_python_java.csv`.
- Gráficas guardadas automáticamente en `resultados/`.
- Parámetros configurables por línea de comandos.

### 📄 Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
