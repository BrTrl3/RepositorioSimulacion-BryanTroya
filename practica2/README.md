# 📈 Práctica 2 - Modelos de Crecimiento Poblacional

**Materia:** Simulación
**Autor:** Bryan Troya

## 📖 1. Descripción del proyecto

Este proyecto implementa y **compara cuatro modelos de crecimiento poblacional**: determinístico, discreto, estocástico y continuo (resuelto numéricamente con el método de Euler).

La simulación parte del arreglo de datos indicado en la guía:

```python
DATOS = [1000, 1100, 1250, 1400, 1600, 1850, 2100]
```

El primer valor se usa como población inicial (`P0 = 1000`) y la serie completa se superpone en la gráfica como referencia de los datos observados. Además, se generan escenarios de **crecimiento y decrecimiento**, un análisis de la **influencia de `r`** y una comparación de **30 réplicas del modelo estocástico** para analizar el efecto de la aleatoriedad.

## 🛠️ 2. Tecnologías utilizadas

| Tecnología | Uso |
| :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3.12%2B-blue) | Lenguaje principal |
| ![NumPy](https://img.shields.io/badge/NumPy-2.x-green) | Cálculo exponencial, ruido aleatorio y promedio de réplicas |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-orange) | Gráficas comparativas de los modelos |

## ⚙️ 3. Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git
cd RepositorioSimulacion-BryanTroya/practica2
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

Ejecutar la simulación desde la carpeta `practica2`:

```bash
python main.py
```

También se puede ejecutar directamente desde la carpeta `python`:

```bash
cd python
python main.py
```

### Datos de entrada

| Dato | Valor |
| :--- | :--- |
| `DATOS` | `[1000, 1100, 1250, 1400, 1600, 1850, 2100]` |
| `P0` | `DATOS[0] = 1000` |
| `tiempo_datos` | `len(DATOS) - 1 = 6` |

### Parámetros de los escenarios

| Parámetro | Valor | Descripción |
| :--- | :--- | :--- |
| `r` | 0.10 | Tasa de crecimiento usada en la comparación y en el estocástico |
| `sigma` | 50 | Desviación estándar del ruido (modelo estocástico) |
| `tiempo` | 20 | Tiempo total de los escenarios de crecimiento/decrecimiento |
| `dt` | 0.1 | Paso de integración del modelo continuo |
| `replicas` | 30 | Número de ejecuciones del modelo estocástico |

### Gráficas generadas

Al ejecutar se muestran cuatro figuras:

| Gráfica | Contenido |
| :--- | :--- |
| **Comparación con datos** | Los cuatro modelos sobre el horizonte de `DATOS` y los datos reales como puntos negros |
| **Crecimiento y decrecimiento** | Dos subgráficas: `r = 0.10` (crecimiento) y `r = -0.05` (decrecimiento) |
| **Influencia de `r`** | Modelo determinístico con `r = 0.05`, `0.10`, `0.20` y `-0.05` |
| **Efecto de la aleatoriedad** | 30 réplicas estocásticas, su promedio y la curva determinística de referencia |

| Modelo | Enfoque |
| :--- | :--- |
| **Determinístico** | Solución analítica exponencial: `P(t) = P0 · e^(r·t)` |
| **Discreto** | Incremento paso a paso: `P(n+1) = P(n) + r·P(n)` |
| **Estocástico** | Incremento con ruido aleatorio normal de media 0 y desviación `sigma` |
| **Continuo (Euler)** | Aproximación numérica de `dP/dt = r·P` con paso `dt` |

> 🎲 El modelo estocástico usa ruido aleatorio, por lo que cada ejecución produce una curva distinta.

## 📁 5. Estructura del proyecto

```
practica2/
├── main.py                      # Lanzador opcional desde la raíz
├── python/                      # Código fuente
│   ├── main.py                  # Punto de entrada y parámetros
│   ├── modelos/                 # 🧠 Modelos de crecimiento
│   │   ├── deterministico.py    #   Solución analítica exponencial
│   │   ├── discreto.py          #   Modelo discreto paso a paso
│   │   ├── estocastico.py       #   Modelo con ruido aleatorio
│   │   └── continuo.py          #   Modelo continuo por método de Euler
│   └── graficas/
│       └── graficas.py          #   Gráficas comparativas con Matplotlib
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo
```

## ℹ️ 6. Información adicional

### ✨ Características clave

- **Cuatro enfoques de simulación** con la misma configuración inicial para compararlos directamente.
- **Uso del arreglo `DATOS` de la guía** como entrada y referencia de la comparación.
- **Escenarios de crecimiento y decrecimiento** para observar el efecto del signo de `r`.
- **Análisis de sensibilidad de `r`** con varias tasas de crecimiento.
- **Método de Euler** implementado manualmente para la aproximación numérica del modelo continuo.
- **Ruido gaussiano** (`numpy.random.normal`) en el modelo estocástico, con la población restringida a valores no negativos.
- **30 réplicas estocásticas** para visualizar la dispersión producida por la aleatoriedad.

### 🔍 Interpretación de resultados

- El modelo **determinístico** (exponencial analítica) sirve como referencia exacta.
- El modelo **discreto** se aproxima al determinístico cuando el paso es pequeño.
- El modelo **continuo con Euler** converge a la solución analítica al reducir `dt`.
- El modelo **estocástico** fluctúa alrededor de la tendencia determinística; al aumentar `sigma`, las réplicas se separan más entre sí.
- Con `r > 0` la población crece; con `r < 0` decrece; con `r = 0` permanece constante.
- Al comparar con `DATOS`, se observa que la serie real crece más rápido que el modelo con `r = 0.10`, lo que sugiere una tasa efectiva cercana a `0.12`.


## 📄 7. Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
