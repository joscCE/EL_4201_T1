# EL_4201_T1 — Tarea 1: Circuitos Térmicos

Repositorio correspondiente a la **Tarea 1 de Circuitos Térmicos (EL4201)**.

El proyecto contiene las simulaciones realizadas en **PLECS**, los modelos térmicos de los semiconductores, scripts auxiliares en **Python**, las imágenes utilizadas en el informe y el documento final.

---

## Estructura del proyecto

```text
EL_4201_T1/
│
├── 00_modelo termico/
│   ├── C3D06060F.xml
│   └── IRFP4868PBF-ND.xml
│
├── 01_Simulacion/
│   ├── Tarea_1.plecs
│   ├── Tarea_1 punto 4.plecs
│   ├── Tarea_1_Punto_5.plecs
│   └── Comparacion_modelos.plecs
│
├── 02_scripts/
│   ├── capacitores.py
│   ├── foster_cauer.py
│   └── switch-losses.py
│
├── 03_Images/
│   └── Imágenes y resultados de las simulaciones
│
├── referencia.pdf
├── Tarea_1.pdf
└── README.md
```

---

# 1. Modelo térmico

La carpeta `00_modelo termico/` contiene los modelos térmicos utilizados por PLECS para representar los dispositivos semiconductores.

```text
00_modelo termico/
├── C3D06060F.xml
└── IRFP4868PBF-ND.xml
```

### `C3D06060F.xml`

Modelo térmico del diodo **C3D06060F**.

Se utiliza en las simulaciones para obtener el comportamiento térmico de la unión del diodo.

### `IRFP4868PBF-ND.xml`

Modelo térmico del MOSFET **IRFP4868PbF**.

Se utiliza para representar el comportamiento térmico del MOSFET dentro de PLECS.

> **Importante:** estos archivos son utilizados directamente por las simulaciones de PLECS. Si se mueve el proyecto a otra computadora, puede ser necesario volver a configurar la ruta de los modelos térmicos dentro de PLECS.

---

# 2. Simulaciones de PLECS

La carpeta `01_Simulacion/` contiene las simulaciones principales del proyecto.

```text
01_Simulacion/
├── Tarea_1.plecs
├── Tarea_1 punto 4.plecs
├── Tarea_1_Punto_5.plecs
└── Comparacion_modelos.plecs
```

Las simulaciones utilizan un convertidor con un MOSFET y un diodo, incluyendo los modelos térmicos de los semiconductores.

---

## `Tarea_1.plecs`

Es la simulación base del circuito utilizado en la tarea.

Incluye:

* Fuente DC.
* Inductor.
* Capacitor.
* Resistencia de carga.
* MOSFET.
* Diodo.
* Modelo térmico del MOSFET.
* Modelo térmico del diodo.
* Red térmica.
* Disipador.
* Mediciones eléctricas y térmicas.

Esta simulación sirve como punto de partida para analizar las temperaturas y pérdidas del circuito.

### Para ejecutarla

1. Abrir **PLECS**.
2. Abrir:

```text
01_Simulacion/Tarea_1.plecs
```

3. Verificar que los modelos térmicos estén correctamente asociados.
4. Ejecutar la simulación.
5. Revisar las señales disponibles en los scopes.

---

## `Tarea_1 punto 4.plecs`

Esta simulación corresponde al análisis térmico más completo del punto 4 de la tarea.

Además del circuito eléctrico, incluye elementos para analizar:

* Temperatura de unión del MOSFET.
* Temperatura de cápsula.
* Temperatura del disipador.
* Temperatura ambiente.
* Temperatura de unión del diodo.
* Flujo de calor.
* Pérdidas de conmutación.
* Pérdidas de los semiconductores.

También contiene varios bloques `Switch Loss Calculator` para obtener las pérdidas asociadas a la conmutación.

### Uso

Abrir en PLECS:

```text
01_Simulacion/Tarea_1 punto 4.plecs
```

Ejecutar la simulación y utilizar los diferentes scopes para observar la evolución de las variables térmicas y eléctricas.

---

## `Tarea_1_Punto_5.plecs`

Esta simulación se utiliza para el análisis del **punto 5**.

Permite estudiar cómo cambian las pérdidas y la temperatura del sistema al modificar parámetros de operación, principalmente:

* Ciclo de trabajo.
* Frecuencia de conmutación.
* Corriente.
* Voltaje.

La simulación incluye un `Switch Loss Calculator` y bloques para separar y visualizar las diferentes señales de pérdidas.

Los resultados obtenidos de estas simulaciones se utilizan para generar gráficas como:

```text
p5_perdidas_vs_duty.png
p5_perdidas_vs_frecuencia.png
p5_eficiencia_vs_duty.png
p5_eficiencia_vs_frecuencia.png
```

y las gráficas de pérdidas de los semiconductores para diferentes condiciones.

---

## `Comparacion_modelos.plecs`

Esta simulación se utiliza para comparar diferentes representaciones de un modelo térmico.

Se incluyen redes térmicas basadas en modelos:

* Foster.
* Cauer.

El objetivo es observar que diferentes representaciones pueden describir el mismo comportamiento térmico y comparar sus respuestas.

Los resultados de esta simulación se relacionan con las imágenes:

```text
comparacion_modelos.png
resultados_comparacion.png
```

---

# 3. Scripts de Python

La carpeta `02_scripts/` contiene cálculos auxiliares utilizados durante el desarrollo de la tarea.

```text
02_scripts/
├── capacitores.py
├── foster_cauer.py
└── switch-losses.py
```

Los scripts no son necesarios para ejecutar directamente las simulaciones de PLECS, pero se utilizan para obtener parámetros y realizar cálculos complementarios.

---

## `capacitores.py`

Calcula los valores de los capacitores térmicos a partir de los valores de:

* Resistencia térmica `R`.
* Constante de tiempo `τ`.

Utiliza la relación:

```text
C = τ / R
```

El script recibe los valores de las resistencias y constantes de tiempo y muestra los cuatro valores de capacitancia correspondientes.

### Ejecutar

Desde la carpeta `02_scripts/`:

```bash
python capacitores.py
```

No requiere librerías externas.

---

## `foster_cauer.py`

Convierte un modelo térmico **Foster** a una representación **Cauer**.

El script utiliza `SymPy` para realizar las operaciones simbólicas necesarias.

La entrada consiste en:

```text
R1, R2, ..., Rn
C1, C2, ..., Cn
```

correspondientes al modelo Foster.

El programa:

1. Construye la impedancia térmica del modelo Foster.
2. Obtiene la expresión simbólica de `Z(s)`.
3. Realiza la expansión necesaria para obtener la red Cauer.
4. Extrae las resistencias y capacitancias.
5. Muestra los resultados utilizando unidades prácticas.

Por ejemplo:

```text
R = [ ... ]
C = [ ... ]

foster_to_cauer(R, C)
```

### Dependencias

Se necesita `SymPy`:

```bash
pip install sympy
```

### Ejecutar

```bash
python foster_cauer.py
```

---

## `switch-losses.py`

Calcula las pérdidas de conmutación aproximadas del MOSFET para diferentes valores de:

* Voltaje de bus.
* Corriente de drenaje.

El script utiliza parámetros del **IRFP4868PbF**, incluyendo:

* Voltaje de compuerta.
* Voltaje de plateau.
* Resistencias de compuerta.
* Tiempos de conmutación.
* Carga de recuperación inversa.
* Capacitancias asociadas al efecto Miller.

Se generan matrices de:

```text
E_on
E_off
```

para las combinaciones de voltaje y corriente definidas en el script.

Los resultados se imprimen tanto en:

* `µJ`.
* Joules.
* Formato de listas compatible con MATLAB/PLECS.

### Dependencias

Se necesita `NumPy`:

```bash
pip install numpy
```

### Ejecutar

```bash
python switch-losses.py
```

---

# 4. Imágenes


Tomando en cuenta que el tamaño de las imagenes en el documento no es optimo, pero colocadas de esta forma por motivos de limitaciones en la extension del documento dejamos la carpeta `03_Images/` contiene las imágenes utilizadas para documentar los resultados. 

Algunas de las principales categorías son:

### Modelo térmico

```text
foster_caurer.png
curva_impedancia_terminca_mosfet.png
comparacion_modelos.png
resultados_comparacion.png
```

### Temperaturas

```text
Ambiente_Temp.png
Pad_Temp.png
Disipador_Temp.png
FETD_Junction_Temp.png
Diode_Junction_Temp.png
resultado_thermo.png
```

### Pérdidas

```text
Perdidas_separadas.png
Potencia_Promedio.png
p5_perdidas_vs_duty.png
p5_perdidas_vs_frecuencia.png
```

### Punto 5

Se incluyen resultados para diferentes ciclos de trabajo y frecuencias:

```text
p5_d03_perdidas_semiconductores.png
p5_d06_perdidas_semiconductores.png
p5_d08_perdidas_semiconductores.png

p5_f03khz_perdidas_semiconductores.png
p5_f06khz_perdidas_semiconductores.png
p5_f12khz_perdidas_semiconductores.png
```

Estas imágenes corresponden a los resultados obtenidos a partir de las simulaciones de PLECS.

---


# 5. Requisitos

Para utilizar completamente el proyecto se necesita:

### PLECS

Se requiere **PLECS** para abrir y ejecutar los archivos:

```text
.plecs
```

### Python

Se recomienda Python 3.

Las dependencias utilizadas por los scripts son:

```bash
pip install numpy sympy
```

---

# 7. Uso recomendado

Si se desea reproducir el trabajo desde cero, se recomienda seguir este orden:

### 1. Revisar los modelos térmicos

Comprobar los archivos:

```text
00_modelo termico/
```

y verificar que los modelos puedan ser utilizados por PLECS.

### 2. Ejecutar la simulación base

Abrir:

```text
01_Simulacion/Tarea_1.plecs
```

y comprobar que el circuito funciona correctamente.

### 3. Ejecutar el análisis térmico

Abrir:

```text
01_Simulacion/Tarea_1 punto 4.plecs
```

y analizar las temperaturas y pérdidas.

### 4. Revisar los cálculos auxiliares

Ejecutar los scripts de Python:

```bash
cd 02_scripts

python capacitores.py
python foster_cauer.py
python switch-losses.py
```

Los resultados pueden utilizarse para comprobar o generar parámetros utilizados en las simulaciones.

### 5. Comparar modelos térmicos

Abrir:

```text
01_Simulacion/Comparacion_modelos.plecs
```

para comparar las representaciones Foster y Cauer.

### 6. Ejecutar el punto 5

Abrir:

```text
01_Simulacion/Tarea_1_Punto_5.plecs
```

y modificar las condiciones de operación necesarias para obtener los resultados del punto 5.

---

# 8. Resumen

| Carpeta/archivo                           | Función                                 |
| ----------------------------------------- | --------------------------------------- |
| `00_modelo termico/`                      | Modelos térmicos de los semiconductores |
| `01_Simulacion/Tarea_1.plecs`             | Simulación base del circuito            |
| `01_Simulacion/Tarea_1 punto 4.plecs`     | Análisis térmico y pérdidas             |
| `01_Simulacion/Tarea_1_Punto_5.plecs`     | Análisis del punto 5                    |
| `01_Simulacion/Comparacion_modelos.plecs` | Comparación Foster/Cauer                |
| `02_scripts/capacitores.py`               | Cálculo de capacitancias térmicas       |
| `02_scripts/foster_cauer.py`              | Conversión de Foster a Cauer            |
| `02_scripts/switch-losses.py`             | Cálculo de pérdidas de conmutación      |
| `03_Images/`                              | Resultados gráficos e imágenes          |
| `Tarea_1.pdf`                             | Informe de la tarea                     |
| `referencia.pdf`                          | Documento de referencia                 |

---

## Notas

* Las simulaciones fueron desarrolladas utilizando **PLECS**.
* Los scripts de Python se utilizan como herramientas auxiliares para obtener parámetros y realizar cálculos.
* Los archivos `.xml` de la carpeta `00_modelo termico/` deben permanecer disponibles para que PLECS pueda cargar correctamente los modelos de los dispositivos.
* Se recomienda mantener la estructura de carpetas del proyecto para evitar problemas con las rutas de los modelos.
