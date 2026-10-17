# Repositorio de Prácticas de Simulación

**Materia:** Simulación  
**Autor:** Bryan Troya  
**Universidad Nacional de Loja**

## 1. Descripción del proyecto

Este repositorio contiene el desarrollo de todas las prácticas realizadas durante el curso de **Simulación**. Cada práctica aborda distintos conceptos de modelado, análisis y simulación de sistemas, implementados en **Python** con un enfoque modular, ordenado, claro y debidamente documentado.

El propósito principal es aplicar los fundamentos teóricos vistos en clase mediante la implementación práctica de algoritmos, modelos de simulación y análisis de resultados, obteniendo soluciones funcionales, comprensibles y verificables.

## 2. Tecnologías utilizadas

| Tecnología | Uso |
|-------------|-----|
| **Python**     | Lenguaje principal para el desarrollo de todas las prácticas. |
| **SimPy**      | Motor de simulación de eventos discretos (utilizado en la Práctica 3). |
| **NumPy**      | Generación de variables aleatorias, cálculos numéricos y estadísticos (Práctica 3). |
| **Matplotlib** | Generación y visualización de gráficas (Práctica 3). |
| **Streamlit**  | Interfaz web local interactiva para la visualización de resultados (Práctica 3). |
| **unittest**   | Pruebas automatizadas para validar el correcto funcionamiento (Práctica 3). |

## 3. Instalación

Sigue estos pasos para clonar e instalar el repositorio en tu equipo:

```bash
# 1. Clonar el repositorio
git clone https://github.com/BryanTroya/RepositorioSimulacion-BryanTroya.git

# 2. Acceder a la carpeta del proyecto
cd RepositorioSimulacion-BryanTroya
```

> **Nota:** La **Práctica 3** cuenta con dependencias externas, por lo que se recomienda trabajar dentro de un entorno virtual. Las prácticas 1 y 2 únicamente requieren tener **Python 3.10 o superior** instalado.

## 4. Configuración y Uso

### 🔹 Práctica 1

```bash
# Ejecutar desde la raíz del repositorio
python practica1/main.py
```

### 🔹 Práctica 2

```bash
# Ejecutar desde la raíz del repositorio
python practica2/main.py
```

### 🔹 Práctica 3 – Simulación de Cola M/M/1

Esta práctica implementa un sistema de líneas de espera **M/M/1** con arquitectura **MVC**, pruebas automatizadas e interfaz web con **Streamlit**.

#### 4.1. Crear y activar el entorno virtual

**Linux / macOS**

```bash
cd practica3
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
cd practica3
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Símbolo del sistema / CMD)**

```bat
cd practica3
python -m venv .venv
.venv\Scripts\activate.bat
```

#### 4.2. Instalar dependencias

Con el entorno virtual activado, ejecuta:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 4.3. Ejecutar las pruebas

```bash
python -m unittest -v
```

#### 4.4. Iniciar la aplicación

```bash
streamlit run app.py
```

Una vez iniciada, abre en tu navegador la dirección que aparece en consola:

```
Local URL: http://localhost:8501
```

Para detener la aplicación, presiona `Ctrl + C` en la terminal.

## 5. Estructura del proyecto

```text
RepositorioSimulacion-BryanTroya/
│
├── GUIAreadme.md        # Guía para la elaboración del README
├── readmeejemplo.md     # Ejemplo de README tomado como referencia
├── README.md            # Documento principal del repositorio
│
├── practica1/
│   ├── README.md        # Documentación de la Práctica 1
│   └── main.py          # Código fuente de la Práctica 1
│
├── practica2/
│   ├── README.md        # Documentación de la Práctica 2
│   └── main.py          # Código fuente de la Práctica 2
│
└── practica3/
    ├── app.py                        # Punto de entrada de la aplicación Streamlit
    ├── requirements.txt              # Lista de dependencias con sus versiones
    ├── .gitignore                    # Archivos y carpetas ignorados por Git
    ├── README.md                     # Documentación detallada de la Práctica 3
    ├── ANALISIS_CUMPLIMIENTO_GUIA.md # Análisis de cumplimiento de la guía de la práctica
    ├── PROMPT MAESTRO PARA OPENCODE= PRÁCTICA 03 DE SIMULACIÓN MM1.md
    ├── REGLAS_EQUIPO.md              # Reglas de trabajo colaborativo
    │
    ├── controller/                   # Capa Controlador (MVC)
    │   ├── __init__.py
    │   └── simulation_controller.py
    │
    ├── model/                        # Capa Modelo (MVC)
    │   ├── __init__.py
    │   ├── metrics.py
    │   └── queue_model.py
    │
    ├── view/                         # Capa Vista (MVC)
    │   ├── __init__.py
    │   └── dashboard.py
    │
    ├── tests/                        # Pruebas automatizadas con unittest
    │   ├── __init__.py
    │   ├── test_metrics.py
    │   └── test_simulation.py
    │
    └── __pycache__/                  # Archivos compilados de Python (generados automáticamente)
```

## 6. Información adicional

### ✨ Características clave

- **Organización modular:** Cada práctica se encuentra completamente aislada con su propia documentación y código fuente.
- **Arquitectura MVC:** Implementada en la **Práctica 3**, garantizando una clara separación entre Modelo, Controlador y Vista.
- **Simulación real con eventos discretos:** Uso de **SimPy** para modelar el comportamiento dinámico de una cola M/M/1.
- **Reproducibilidad:** Control de aleatoriedad mediante `seed`, permitiendo obtener los mismos resultados al repetir una ejecución.
- **Comparación teórica vs simulada:** Cálculo de métricas teóricas y simuladas, presentadas en tablas y gráficas comparativas.
- **Gráficas interactivas:** Visualización de la evolución de la cola, distribución de tiempos de espera y comparaciones entre escenarios con **Matplotlib**.
- **Pruebas automatizadas:** Validación de fórmulas teóricas, consistencia de tiempos, capacidad del servidor, reproducibilidad y casos límite.
- **Interfaz intuitiva:** Dashboard en español desarrollado con **Streamlit**, pensado para facilitar su comprensión y exposición.

### 📋 Estado de las prácticas

| Práctica | Tema | Estado |
|-----------|------|--------|
| **Práctica 1** | Introducción a Simulación | ✅ Completada |
| **Práctica 2** | Fundamentos de Simulación | ✅ Completada |
| **Práctica 3** | Simulación de Cola M/M/1 con SimPy, NumPy, Matplotlib, Streamlit y MVC | ✅ Completada |

### 👤 Autor

**Bryan Troya**  
Estudiante de la Carrera de Computación – Universidad Nacional de Loja  
Asignatura: Simulación

### 💡 Recomendaciones

- Ejecuta las **Prácticas 1** y **2** directamente con Python, sin necesidad de entorno virtual.
- Para la **Práctica 3**, siempre activa el entorno virtual antes de instalar dependencias, ejecutar pruebas o iniciar la aplicación.
- Revisa el `README.md` específico de cada práctica para obtener información más detallada sobre su desarrollo, objetivos, resultados e interpretación.
- Para conocer a fondo el desarrollo de la Práctica 3, consulta: [`practica3/README.md`](practica3/README.md)

## 7. Flujo secuencial

**¿Qué hace → Tecnologías → Instalación → Configuración y Uso → Estructura del proyecto → Información adicional**