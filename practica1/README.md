# 🌧️ Práctica 1 - Modelo de Posibilidad de Lluvia

**Materia:** Simulación
**Autor:** Bryan Troya

## 📖 1. Descripción del proyecto

Este proyecto implementa un **modelo de simulación para estimar la posibilidad de lluvia** a partir de tres variables meteorológicas: humedad, nubosidad y temperatura.

El sistema calcula un índice de posibilidad de lluvia con la fórmula:

```
I = 0.5·H + 0.3·N + 0.2·Tf
```

donde `H` es la humedad relativa, `N` la nubosidad y `Tf` el factor de temperatura obtenido de una tabla con interpolación lineal.

El problema que resuelve es **comparar el comportamiento del modelo original (pesos fijos) contra un modelo ajustado con pesos aleatorios normalizados**, mostrando los resultados en una tabla por hora y en una gráfica comparativa, para analizar la sensibilidad del índice frente a la variación de los pesos.

## 🛠️ 2. Tecnologías utilizadas

| Tecnología | Versión | Uso |
| :--- | :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3.12-blue) | 3.12+ | Lenguaje principal |
| ![NumPy](https://img.shields.io/badge/NumPy-2.5.3-green) | 2.5.3 | Generación de pesos aleatorios y operaciones numéricas |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-orange) | 3.11.2 | Gráfica comparativa de índices |

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

Ejecutar la simulación desde la carpeta `practica1`:

```bash
python -m python.main
```

**Ejemplo de uso:**

Al ejecutar, el programa:

1. Genera **tres pesos aleatorios normalizados** (su suma es 1) para el modelo ajustado.
2. Calcula el índice para cada hora registrada (06:00 a 22:00) con el **modelo original** y el **modelo ajustado**.
3. Clasifica cada índice en un estado:

| Rango del índice | Estado |
| :--- | :--- |
| `I < 0.40` | Sin lluvia |
| `0.40 ≤ I < 0.60` | Baja posibilidad |
| `0.60 ≤ I < 0.75` | Lluvia probable |
| `I ≥ 0.75` | Lluvia |

4. Muestra la tabla de resultados en consola y una **gráfica comparativa** con los límites de clasificación.

> 🎲 Al usar pesos aleatorios, cada ejecución produce un ajuste distinto.

## 📁 5. Estructura del proyecto

```
practica1/
├── python/                  # Paquete principal (código fuente)
│   ├── main.py              # Punto de entrada de la simulación
│   ├── modelo/              # 🧠 Lógica de negocio (MVC)
│   │   ├── datos.py         #   Datos meteorológicos por hora (H, N, T)
│   │   └── modelo.py        #   Cálculo del índice, pesos y estados
│   ├── controlador/         # 🎮 Controlador (MVC)
│   │   └── controlador.py   #   Orquesta modelo y vista
│   └── vista/               # 🖥️ Presentación (MVC)
│       ├── vista.py         #   Salida por consola (tabla y pesos)
│       └── graficas.py      #   Gráfica comparativa con Matplotlib
├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

## ℹ️ 6. Información adicional

### ✨ Características clave

- Patrón **MVC** bien separado: datos, cálculo, control y presentación.
- **Ajuste aleatorio normalizado**: los pesos generados siempre suman 1 (se verifica en cada ejecución).
- **Interpolación lineal** del factor de temperatura para valores no presentes en la tabla.
- Gráfica con los **límites de clasificación** (0.40, 0.60, 0.75) para interpretar visualmente los estados.

### 🔍 Interpretación de resultados

La gráfica compara el índice del modelo original (línea con círculos) contra el ajustado (línea con cuadrados). Si las curvas se mueven entre regiones de clasificación, el estado de lluvia cambia para esa hora, lo que evidencia la **sensibilidad del modelo a los pesos** de cada variable.

### 📄 Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
