# 📈 Práctica 2 - Modelos de Crecimiento Poblacional

**Materia:** Simulación
**Autor:** Bryan Troya

## 📖 1. Descripción del proyecto

Este proyecto implementa y **compara cuatro modelos de crecimiento poblacional**: determinístico, discreto, estocástico y continuo (resuelto numéricamente con el método de Euler).

El propósito es observar cómo evoluciona una población con los mismos parámetros iniciales (`P0 = 1000`, `r = 0.10`) bajo distintos enfoques matemáticos, y analizar el efecto de **discretizar el tiempo**, **agregar ruido aleatorio** y **aproximar la solución continua por pasos**.

La comparación se presenta en una **gráfica única** con las cuatro curvas superpuestas, lo que permite evidenciar las diferencias entre cada modelo de simulación.

## 🛠️ 2. Tecnologías utilizadas

| Tecnología | Uso |
| :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3.12-blue) | Lenguaje principal |
| ![NumPy](https://img.shields.io/badge/NumPy-2.5.3-green) | Cálculo exponencial y generación de ruido aleatorio normal |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-orange) | Gráfica comparativa de los cuatro modelos |

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

Ejecutar la simulación desde la carpeta `practica2/python`:

```bash
cd python
python main.py
```

**Parámetros utilizados** (definidos en `python/main.py`):

| Parámetro | Valor | Descripción |
| :--- | :--- | :--- |
| `P0` | 1000 | Población inicial |
| `r` | 0.10 | Tasa de crecimiento |
| `sigma` | 50 | Desviación estándar del ruido (modelo estocástico) |
| `tiempo` | 20 | Tiempo total de simulación |
| `dt` | 0.1 | Paso de integración (modelo continuo) |

Al ejecutar, se genera una **gráfica comparativa** con las curvas de los cuatro modelos:

| Modelo | Enfoque |
| :--- | :--- |
| **Determinístico** | Solución analítica exponencial: `P(t) = P0 · e^(r·t)` |
| **Discreto** | Incremento paso a paso: `P(n+1) = P(n) + r·P(n)` |
| **Estocástico** | Incremento con ruido aleatorio normal de media 0 y desviación `sigma` |
| **Continuo (Euler)** | Aproximación numérica de la EDP con paso `dt` |

> 🎲 El modelo estocástico usa ruido aleatorio, por lo que cada ejecución produce una curva distinta.

## 📁 5. Estructura del proyecto

```
practica2/
├── python/                      # Código fuente
│   ├── main.py                  # Punto de entrada y parámetros
│   ├── modelos/                 # 🧠 Modelos de crecimiento
│   │   ├── deterministico.py    #   Solución analítica exponencial
│   │   ├── discreto.py          #   Modelo discreto paso a paso
│   │   ├── estocastico.py       #   Modelo con ruido aleatorio
│   │   └── continuo.py          #   Modelo continuo por método de Euler
│   └── graficas/
│       └── graficas.py          #   Gráfica comparativa con Matplotlib
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo
```

## ℹ️ 6. Información adicional

### ✨ Características clave

- **Cuatro enfoques de simulación** en un solo proyecto, con la misma configuración inicial para compararlos directamente.
- **Método de Euler** implementado manualmente para la aproximación numérica del modelo continuo.
- **Ruido gaussiano** (`numpy.random.normal`) en el modelo estocástico, con la población restringida a valores no negativos.
- Gráfica clara con **leyenda, cuadrícula y etiquetas** para facilitar la interpretación.

### 🔍 Interpretación de resultados

- El modelo **determinístico** (exponencial analítica) sirve como referencia exacta.
- El modelo **discreto** se aproxima al determinístico cuando el paso es pequeño.
- El modelo **continuo con Euler** converge a la solución analítica al reducir `dt`.
- El modelo **estocástico** fluctúa alrededor de la tendencia, mostrando el impacto de la aleatoriedad en sistemas reales.

### 📄 Licencia

Proyecto académico para la materia de **Simulación**. Uso educativo.
