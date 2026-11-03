# 🎓 Repositorio de Prácticas de Simulación

**Materia:** Simulación
**Autor:** Bryan Troya
**Universidad Nacional de Loja**

## 📖 Descripción del proyecto

Este repositorio reúne el desarrollo de las **prácticas de la asignatura de Simulación**, implementadas principalmente en **Python** (y en **Java** cuando la guía lo pide) con un enfoque modular, ordenado y documentado, siguiendo la arquitectura **MVC** cuando corresponde.

El objetivo es aplicar los fundamentos teóricos del curso mediante la implementación de modelos matemáticos, simulaciones y análisis de resultados, obteniendo soluciones funcionales, comprensibles y verificables. Las prácticas abarcan modelos probabilísticos, crecimiento poblacional, teoría de colas, simulación basada en agentes y generación de números pseudoaleatorios.

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
| :--- | :--- |
| **Python** | Lenguaje principal de todas las prácticas |
| **Java** | Implementación alternativa y comparación de resultados (prácticas 1 y 5) |
| **NumPy** | Cálculos numéricos y generación de variables aleatorias |
| **Matplotlib** | Visualización de resultados mediante gráficas |
| **SimPy** | Simulación de eventos discretos y simulación basada en agentes |
| **Streamlit** | Interfaz web interactiva para visualizar resultados |
| **NetLogo** | Modelado basado en agentes y lectura de resultados exportados |
| **csv** | Exportación de resultados |
| **unittest** | Pruebas automatizadas |

## ⚙️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git

# Acceder al proyecto
cd RepositorioSimulacion-BryanTroya
```

> **Nota:** Cada práctica es independiente y puede tener sus propias dependencias. Se recomienda revisar el `README.md` de cada práctica para ver sus instrucciones específicas de instalación y ejecución.

## 📁 Estructura del proyecto

```
RepositorioSimulacion-BryanTroya/
│
├── README.md            # Este documento
│
├── practica1/           # Práctica 1 (con su propio README)
├── practica2/           # Práctica 2 (con su propio README)
├── practica3/           # Práctica 3 (con su propio README)
├── practica4/           # Práctica 4 (con su propio README)
└── practica5/           # Práctica 5: LCG en Python y Java (con su propio README)
```

Cada práctica contiene su **código fuente**, sus **dependencias** y su **propia documentación detallada**.

## 📋 Contenido

| Práctica | Tema | Documentación |
| :--- | :--- | :--- |
| **Práctica 1** | Modelo de posibilidad de lluvia | [`practica1/README.md`](practica1/README.md) |
| **Práctica 2** | Modelos de crecimiento poblacional | [`practica2/README.md`](practica2/README.md) |
| **Práctica 3** | Simulación de cola M/M/1 | [`practica3/README.md`](practica3/README.md) |
| **Práctica 4** | Simulación del modelo SIR con agentes (Python + SimPy) | [`practica4/README.md`](practica4/README.md) |
| **Práctica 5** | Generador congruencial lineal: implementación MVC en Python y Java, comparación de secuencias, período y cambio de semilla | [`practica5/README.md`](practica5/README.md) |

> 💡 Para conocer los objetivos, la implementación, la ejecución y los resultados de cada práctica, consulta el `README.md` correspondiente.

## ℹ️ Información adicional

### 👤 Autor

**Bryan Troya**
Estudiante de la Carrera de Computación – Universidad Nacional de Loja
Asignatura: Simulación

### 💡 Recomendaciones

- Cada práctica es autónoma: entra a su carpeta y sigue las instrucciones de su propio `README.md`.
- Para las prácticas con dependencias externas, usa un entorno virtual antes de instalar los paquetes.
- Las prácticas con versión en Java requieren un **JDK 11 o superior** con `java` y `javac` en el `PATH`.
- Consulta la documentación específica de cada práctica para obtener detalles sobre su desarrollo e interpretación de resultados.

### 📄 Licencia

Proyecto académico para la asignatura de **Simulación**. Uso educativo.
