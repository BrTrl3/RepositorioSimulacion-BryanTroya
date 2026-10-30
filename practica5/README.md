# Practica 5 - Generador Congruencial Lineal (LCG) en Python y Java

**Materia:** Simulacion
**Carrera:** Computacion
**Universidad Nacional de Loja**
**Autor:** Bryan Troya

## 1. Descripcion del proyecto

Esta practica implementa un **Generador Congruencial Lineal (LCG)** con los parametros:

```text
x_(n+1) = (a * x_n + c) mod m
a = 1664525
c = 1013904223
m = 2^32 = 4294967296
semilla = 12345
```

El generador produce 10 000 valores, los normaliza en el intervalo `[0, 1)` mediante `u_n = x_n / m` y analiza:

- Los primeros 20 estados y valores normalizados.
- La media, desviacion estandar, minimo, maximo y frecuencia por deciles.
- La correlacion entre valores consecutivos.
- El periodo teorico mediante las condiciones de Hull-Dobell.
- El efecto de cambiar la semilla a `54321`.
- La equivalencia de la secuencia generada en **Python** y en **Java**.

La implementacion sigue una arquitectura **MVC**, de modo que el modelo no depende de la consola ni de las graficas, el controlador no dibuja y la vista no genera numeros.

## 2. Tecnologias utilizadas

| Tecnologia | Uso dentro del proyecto |
| :--- | :--- |
| **Python** | Implementacion principal del modelo, controlador y vistas. |
| **Java** | Implementacion equivalente para comparar la secuencia y verificar el manejo de enteros de 32 bits. |
| **Matplotlib** | Generacion de graficas PNG. |
| **csv** | Exportacion de valores, resumenes y comparaciones. |
| **unittest** | Pruebas automatizadas con la biblioteca estandar de Python. |
| **argparse** | Parametros de linea de comandos. |

## 3. Instalacion

### 3.1. Requisitos previos

- **Python 3.10 o superior**.
- **JDK 11 o superior** si se desea ejecutar la comparacion con Java.
- **pip** actualizado.

Comprobar las versiones:

```bash
python --version
java -version
javac -version
```

### 3.2. Clonar y acceder al proyecto

```bash
git clone https://github.com/BrTrl3/RepositorioSimulacion-BryanTroya.git
cd RepositorioSimulacion-BryanTroya/practica5
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

**Windows (Simbolo del sistema / CMD)**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3.4. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**

```text
matplotlib>=3.7,<4
```

## 4. Configuracion y uso

### 4.1. Ejecucion basica

Desde la carpeta `practica5`, con el entorno virtual activado:

```bash
python main.py
```

La ejecucion predeterminada:

1. Genera 10 000 valores con semilla `12345`.
2. Genera una segunda secuencia con semilla `54321`.
3. Calcula las estadisticas y el analisis de periodo.
4. Compila y ejecuta Java automaticamente si `javac` y `java` estan disponibles.
5. Exporta los resultados a `resultados/`.
6. Genera cuatro graficas PNG.

### 4.2. Parametros de linea de comandos

| Parametro | Valor por defecto | Descripcion |
| :--- | :--- | :--- |
| `--semilla` | `12345` | Semilla principal. |
| `--semilla-alternativa` | `54321` | Semilla para la comparacion. |
| `--cantidad` | `10000` | Cantidad de valores a generar. |
| `--salida` | `resultados/` | Directorio de salida. |
| `--sin-java` | desactivado | Omite la compilacion y ejecucion de Java. |
| `--sin-graficas` | desactivado | Omite la generacion de graficas PNG. |

Ejemplos:

```bash
python main.py --semilla 12345 --cantidad 10000
python main.py --sin-java
python main.py --sin-java --sin-graficas
python main.py --salida resultados_extra --cantidad 5000
```

### 4.3. Ejecucion manual de Java

Si se desea ejecutar solo la implementacion Java:

```bash
javac -encoding UTF-8 -d java java/modelo/LCG.java java/controlador/LCGController.java java/vista/Consola.java java/Main.java
java -cp java Main --seed 12345 --count 10000 --output resultados/java_lcg_12345.csv
```

Tambien se puede consultar la ayuda:

```bash
java -cp java Main --help
```

> **Importante:** En Java se usa `long` y la mascara `& 0xFFFFFFFF`. No se debe usar `int`, porque el desbordamiento con signo produciria una secuencia distinta. Ademas, la salida numerica se formatea con `Locale.US` o con `Double.toString()` para evitar comas decimales.

### 4.4. Ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

**Resultado esperado:** 14 pruebas ejecutadas, todas correctas (`OK`).

### 4.5. Salidas generadas

| Archivo | Contenido |
| :--- | :--- |
| `resultados/valores_python_12345.csv` | Estados y valores `u_n` de la secuencia principal. |
| `resultados/valores_python_54321.csv` | Estados y valores `u_n` de la secuencia alternativa. |
| `resultados/primeros_20_python.csv` | Primeros 20 valores de Python. |
| `resultados/resumen.csv` | Media, desviacion, minimo, maximo, correlacion y frecuencias. |
| `resultados/periodo.csv` | Condiciones de Hull-Dobell y prueba de periodo. |
| `resultados/comparacion_semillas.csv` | Comparacion de las dos semillas. |
| `resultados/java_lcg_12345.csv` | Salida generada por Java. |
| `resultados/comparacion_python_java.csv` | Comparacion de los primeros 20 valores Python/Java. |
| `resultados/secuencia.png` | Primeros 300 valores de la secuencia. |
| `resultados/dispersion.png` | Pares consecutivos `(u_n, u_n+1)`. |
| `resultados/histograma.png` | Histograma de los 10 000 valores. |
| `resultados/comparacion_semillas.png` | Primeras 100 salidas con las dos semillas. |

La carpeta `resultados/` se genera localmente y esta incluida en `.gitignore`.

## 5. Estructura del proyecto

```text
practica5/
├── main.py
├── model/
│   ├── __init__.py
│   ├── lcg.py
│   └── analysis.py
├── controller/
│   ├── __init__.py
│   └── lcg_controller.py
├── view/
│   ├── __init__.py
│   ├── consola.py
│   ├── graficas.py
│   └── reportes.py
├── tests/
│   ├── __init__.py
│   └── test_lcg.py
├── java/
│   ├── Main.java
│   ├── modelo/
│   │   └── LCG.java
│   ├── controlador/
│   │   └── LCGController.java
│   └── vista/
│       └── Consola.java
├── requirements.txt
├── .gitignore
└── README.md
```

| Modulo | Responsabilidad |
| :--- | :--- |
| `main.py` | Punto de entrada y conexion entre controlador y vistas. |
| `model/lcg.py` | Parametros, validaciones, estado y generacion de la secuencia. |
| `model/analysis.py` | Estadisticas, Hull-Dobell, deteccion de periodo y comparaciones. |
| `controller/lcg_controller.py` | Orquesta la generacion, compilacion/ejecucion de Java y lectura de resultados. |
| `view/consola.py` | Presenta tablas y resumenes en la terminal. |
| `view/graficas.py` | Construye las graficas con Matplotlib. |
| `view/reportes.py` | Exporta los CSV. |
| `tests/test_lcg.py` | Verifica valores, validaciones, estadisticas, periodo y CSV. |

## 6. Informacion adicional

### 6.1. Primeros 20 valores

| n | Estado `x_n` | Valor normalizado `u_n` |
| ---: | ---: | ---: |
| 1 | 87628868 | 0.0204026857 |
| 2 | 71072467 | 0.0165478482 |
| 3 | 2332836374 | 0.5431557945 |
| 4 | 2726892157 | 0.6349040561 |
| 5 | 3908547000 | 0.9100295138 |
| 6 | 483019191 | 0.1124616691 |
| 7 | 2129828778 | 0.4958894053 |
| 8 | 2355140353 | 0.5483488443 |
| 9 | 2560230508 | 0.5961001171 |
| 10 | 3364893915 | 0.7834504161 |
| 11 | 171172990 | 0.0398543174 |
| 12 | 3194601925 | 0.7438012224 |
| 13 | 4148119648 | 0.9658093676 |
| 14 | 316399679 | 0.0736675409 |
| 15 | 3004788882 | 0.6996069294 |
| 16 | 1976948425 | 0.4602941743 |
| 17 | 1702883732 | 0.3964835154 |
| 18 | 4121112547 | 0.9595212869 |
| 19 | 1744294886 | 0.4061253010 |
| 20 | 4092090893 | 0.9527641565 |

La implementacion Java produce exactamente los mismos estados. La comparacion automatica verifica las 10 000 filas y reporta `0` diferencias.

### 6.2. Estadisticas de la secuencia principal

| Metrica | Valor |
| :--- | ---: |
| Cantidad | 10 000 |
| Media | 0.49876985 |
| Desviacion estandar | 0.28811763 |
| Minimo | 0.0000590826 |
| Maximo | 0.9999259654 |
| Correlacion lag 1 | -0.01531333 |

| Intervalo | Frecuencia |
| :--- | ---: |
| `[0.0, 0.1)` | 1 016 |
| `[0.1, 0.2)` | 993 |
| `[0.2, 0.3)` | 1 049 |
| `[0.3, 0.4)` | 940 |
| `[0.4, 0.5)` | 949 |
| `[0.5, 0.6)` | 1 063 |
| `[0.6, 0.7)` | 1 014 |
| `[0.7, 0.8)` | 1 016 |
| `[0.8, 0.9)` | 984 |
| `[0.9, 1.0)` | 976 |

La media se aproxima a `0.5`, la desviacion estandar se aproxima a `1/sqrt(12) = 0.288675` y las frecuencias por decil son cercanas a 1 000. La correlacion lag 1 es muy baja, lo que indica ausencia de una relacion lineal fuerte entre valores consecutivos, aunque esto no demuestra independencia estadistica.

### 6.3. Analisis del periodo

Para que un LCG tenga periodo completo `m`, las condiciones de Hull-Dobell son:

1. `mcd(c, m) = 1`.
2. Todo factor primo de `m` divide a `a - 1`.
3. Si `m` es divisible por 4, entonces `a - 1` es divisible por 4.

Con los parametros de la practica:

| Condicion | Resultado |
| :--- | :--- |
| `mcd(1013904223, 4294967296) = 1` | Cumple |
| `2` divide a `1664524` | Cumple |
| `1664524 mod 4 = 0` | Cumple |

Por lo tanto, el periodo maximo teorico es:

```text
m = 2^32 = 4 294 967 296
```

La muestra de 10 000 valores no contiene repeticiones. Para no recorrer miles de millones de estados, el programa comprueba la ausencia de repeticiones en la muestra y valida la deteccion de ciclo con un LCG pequeno:

```text
a = 5, c = 3, m = 16, semilla = 1
mu = 0
lambda = 16
```

La deteccion practica de ciclo se implementa con el algoritmo de Floyd, que usa dos punteros y no requiere almacenar todos los estados.

### 6.4. Comparacion de semillas

| n | `u` con semilla 12345 | `u` con semilla 54321 | Diferencia absoluta |
| ---: | ---: | ---: | ---: |
| 1 | 0.0204026857 | 0.2883033669 | 0.2679006811 |
| 2 | 0.0165478482 | 0.3977943386 | 0.3812464904 |
| 3 | 0.5431557945 | 0.8575955289 | 0.3144397344 |
| 4 | 0.6349040561 | 0.4338794921 | 0.2010245640 |
| 5 | 0.9100295138 | 0.4976655729 | 0.4123639408 |
| 6 | 0.1124616691 | 0.0238184889 | 0.0886431802 |
| 7 | 0.4958894053 | 0.7063563173 | 0.2104669120 |
| 8 | 0.5483488443 | 0.9850727303 | 0.4367238861 |
| 9 | 0.5961001171 | 0.4225403676 | 0.1735597495 |
| 10 | 0.7834504161 | 0.2414156541 | 0.5420347620 |

La semilla `54321` no aparece dentro de los primeros 10 000 estados generados con semilla `12345`. Teoricamente, cambiar la semilla selecciona otra ventana de la misma secuencia, no una secuencia estadisticamente independiente.

### 6.5. Comparacion Python/Java

| Aspecto | Python | Java |
| :--- | :--- | :--- |
| Tipo entero | Precisión arbitraria | `long` de 64 bits |
| Reduccion modulo `2^32` | `% (2**32)` | `& 0xFFFFFFFFL` |
| Primer valor | 87628868 | 87628868 |
| Primer `u` | 0.0204026857 | 0.0204026857 |
| Filas coincidentes | 10 000 de 10 000 | 10 000 de 10 000 |

El uso de `long` es seguro porque `a * x` es aproximadamente `7.1 x 10^15`, inferior al maximo de un `long`. Si se usara `int`, el resultado se desbordaria y podria volverse negativo.

### 6.6. Arquitectura MVC

| Capa | Archivos | Responsabilidad |
| :--- | :--- | :--- |
| Modelo | `model/lcg.py`, `model/analysis.py` | Genera la secuencia y calcula estadisticas, periodo y comparaciones. No imprime ni dibuja. |
| Controlador | `controller/lcg_controller.py` | Valida parametros, coordina la generacion y ejecuta Java cuando esta disponible. |
| Vista | `view/consola.py`, `view/graficas.py`, `view/reportes.py` | Presenta resultados, genera graficas y exporta CSV. |

La version Java mantiene la misma separacion:

| Capa | Archivos |
| :--- | :--- |
| Modelo | `java/modelo/LCG.java` |
| Controlador | `java/controlador/LCGController.java` |
| Vista | `java/vista/Consola.java` |
| Entrada | `java/Main.java` |

### 6.7. Preguntas de control

1. **Por que el periodo maximo es `2^32`?**  
   Porque el estado es un entero de 32 bits y solo existen `2^32` estados posibles. Con Hull-Dobell el generador recorre todos antes de repetir.

2. **Que ocurre si en Java se usa `int`?**  
   La multiplicacion se desborda con signo y la secuencia deja de coincidir con Python. Debe usarse `long` y aplicar la mascara de 32 bits.

3. **Por que se normaliza `u_n = x_n / m`?**  
   Para transformar el estado entero en un valor en `[0, 1)`, apto para simulaciones y comparaciones con distribuciones uniformes.

4. **Que significa una correlacion lag 1 cercana a cero?**  
   Que no hay una dependencia lineal fuerte entre un valor y el siguiente. No garantiza independencia ni ausencia de patrones en dimensiones superiores.

5. **Sirve este LCG para criptografia?**  
   No. Es predecible: conociendo los parametros y un estado se puede reconstruir toda la secuencia. Para seguridad se requieren generadores criptograficos.

### 6.8. Conclusiones

- Python y Java generan exactamente la misma secuencia cuando Java usa `long` y mascara de 32 bits.
- Los valores normalizados se distribuyen de forma aproximadamente uniforme en `[0, 1)`.
- La media y la desviacion estandar se acercan a los valores teoricos de una uniforme.
- Las frecuencias por decil son razonablemente equilibradas y la correlacion lag 1 es baja.
- El generador cumple Hull-Dobell y alcanza un periodo maximo teorico de `2^32`.
- Cambiar la semilla produce otra ventana de la misma secuencia, por lo que no debe interpretarse como una fuente independiente de aleatoriedad.
- Un periodo largo no garantiza buena calidad estadistica; en aplicaciones reales conviene complementar con pruebas espectrales y de equidistribucion.

### 6.9. Limitaciones

- El LCG es deterministico y completamente predecible si se conocen sus parametros.
- La ausencia de repeticiones en 10 000 valores no demuestra por si sola que el periodo sea `2^32`; la conclusion se apoya en Hull-Dobell.
- La correlacion lag 1 solo detecta dependencia lineal de primer orden.
- No se realizan pruebas de uniformidad formales como chi-cuadrado o Kolmogorov-Smirnov.
- El LCG no es adecuado para criptografia ni para simulaciones que exijan independencia multidimensional estricta.

### 6.10. Declaracion del uso de inteligencia artificial

- **Herramienta utilizada:** OpenCode, asistente de programacion basado en IA.
- **Uso dado:** Apoyo en estructura MVC, implementacion Python/Java, redaccion de pruebas, documentacion y revision de resultados.
- **Supervision humana:** El codigo y los resultados deben ejecutarse y verificarse antes de la entrega.
- **Integridad:** Los valores mostrados en este README provienen de la ejecucion real del programa.

### Licencia

Proyecto academico para la materia de **Simulacion**. Uso educativo.
