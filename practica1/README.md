# 🌧️ Práctica 1 - Modelo de Posibilidad de Lluvia

**Materia:** Simulación
**Autor:** Bryan Troya

## 📖 1. Descripción del proyecto

Este proyecto implementa un **modelo de simulación para estimar la posibilidad de lluvia** a partir de tres variables meteorológicas: humedad, nubosidad y temperatura.

El sistema calcula un índice de posibilidad de lluvia con la fórmula:

```
I = 0.5·H + 0.3·N + 0.2·Tf
```

donde `H` es la humedad normalizada, `N` la nubosidad normalizada y `Tf` el factor de temperatura obtenido de una tabla con interpolación lineal.

El problema que resuelve es **comparar el comportamiento del modelo original (pesos fijos) contra un modelo ajustado con pesos aleatorios normalizados**, mostrando los resultados en una tabla por hora, en gráficas y en un archivo CSV, para analizar la sensibilidad del índice frente a la variación de las variables y de los pesos.

La práctica se implementa en **Python** y en **Java**.

## 🛠️ 2. Tecnologías utilizadas

| Tecnología | Versión | Uso |
| :--- | :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3.12-blue) | 3.12+ | Lenguaje principal |
| ![NumPy](https://img.shields.io/badge/NumPy-2.5.3-green) | 2.5.3 | Generación de pesos aleatorios y operaciones numéricas |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-orange) | 3.11.2 | Gráficas comparativas y de influencia |
| Java | 11+ | Implementación alternativa del modelo |

> El proyecto sigue el patrón de arquitectura **MVC** (Modelo - Vista - Controlador).

## ⚙️ 3. Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git
cd RepositorioSimulacion-BryanTroya/practica1
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

## 🚀 4. Configuración y Uso

### Python

Ejecutar la simulación desde la carpeta `practica1`:

```bash
python -m python.main
```

Al ejecutar, el programa:

1. Genera **tres pesos aleatorios normalizados** (su suma es 1) para el modelo ajustado. La semilla es fija (`42`) para que los resultados sean reproducibles.
2. Calcula el índice para cada hora registrada (06:00 a 22:00) con el **modelo original** y el **modelo ajustado**.
3. Muestra una tabla con las columnas `H`, `N`, `Tf`, índice original, estado original, índice ajustado y estado ajustado.
4. Clasifica cada índice en un estado:

| Rango del índice | Estado |
| :--- | :--- |
| `I < 0.40` | Sin lluvia |
| `0.40 ≤ I < 0.60` | Baja posibilidad |
| `0.60 ≤ I < 0.75` | Lluvia probable |
| `I ≥ 0.75` | Lluvia |

5. Genera y guarda en `resultados/`:

| Archivo | Contenido |
| :--- | :--- |
| `01_comparacion.png` | Modelo original vs modelo ajustado con los límites de clasificación |
| `02_variables.png` | Comportamiento de `H`, `N` y `Tf` durante el día |
| `03_influencia_parametros.png` | Influencia de cada variable en el índice |
| `tabla_resultados.csv` | Tabla completa de resultados por hora |

> 🎲 La semilla fija hace reproducible el ajuste. Para obtener pesos distintos en cada ejecución, cambie `SEMILLA_POR_DEFECTO` en `python/modelo/modelo.py`.

### Java

Compilar y ejecutar desde la carpeta `practica1`:

```bash
javac -encoding UTF-8 -d java java/ModeloLluvia.java
java -cp java ModeloLluvia
```

Opcionalmente se pueden indicar los tres pesos del modelo ajustado:

```bash
java -cp java ModeloLluvia 0.40 0.40 0.20
```

La implementación en Java usa por defecto los pesos ajustados `0.40`, `0.40` y `0.20`, imprime la misma tabla por consola y genera `resultados/tabla_resultados_java.csv`.

## 📁 5. Estructura del proyecto

```
practica1/
├── python/                  # Paquete principal (código fuente Python)
│   ├── main.py              # Punto de entrada de la simulación
│   ├── modelo/              # 🧠 Lógica de negocio (MVC)
│   │   ├── datos.py         #   Datos meteorológicos por hora (H, N, T)
│   │   └── modelo.py        #   Cálculo del índice, pesos y estados
│   ├── controlador/         # 🎮 Controlador (MVC)
│   │   └── controlador.py   #   Orquesta modelo y vista
│   └── vista/               # 🖥️ Presentación (MVC)
│       ├── vista.py         #   Salida por consola (tabla y pesos)
│       ├── graficas.py      #   Gráficas con Matplotlib
│       └── reportes.py      #   Exportación de la tabla a CSV
├── java/
│   └── ModeloLluvia.java    # Implementación del modelo en Java
├── resultados/              # Gráficas y CSV generados al ejecutar
├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

## ℹ️ 6. Información adicional

### ✨ Características clave

- Patrón **MVC** bien separado: datos, cálculo, control y presentación.
- **Ajuste aleatorio normalizado**: los pesos generados siempre suman 1 (se verifica en cada ejecución).
- **Interpolación lineal** del factor de temperatura para valores no presentes en la tabla (por ejemplo, 15 °C y 17 °C).
- Tabla con las variables normalizadas `H` y `N`, tal como solicita la guía.
- Gráficas guardadas automáticamente en `resultados/` con los límites de clasificación.
- Implementación equivalente en **Java**, que también exporta su tabla a CSV.

### 🔍 Interpretación de resultados

La gráfica comparativa muestra el índice del modelo original (línea con círculos) contra el ajustado (línea con cuadrados). Si las curvas se mueven entre regiones de clasificación, el estado de lluvia cambia para esa hora, lo que evidencia la **sensibilidad del modelo a los pesos** de cada variable.

La gráfica de influencia muestra que el índice crece linealmente con cada variable, pero con pendiente distinta según su peso: la humedad tiene la mayor influencia (`0.5`), seguida de la nubosidad (`0.3`) y del factor de temperatura (`0.2`).

### 📄 Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
