# Proyecto: Egg Dropping (DaC vs Programación Dinámica)

Comparación experimental entre una solución **recursiva tipo Divide and Conquer sin memoización** y una solución **bottom-up por programación dinámica** para el problema de los huevos y los pisos (mínimo de intentos en el peor caso).

## Estructura del proyecto

```
Proyecto2_ADA/
├── main.py           # Punto de entrada (dac | dp | all | compare)
├── test_cases.py     # Las 30 entradas de prueba fijas (compartidas)
├── egg_drop_dac.py   # Algoritmo DaC, benchmark, CSV y gráficas
├── egg_drop_dp.py    # Algoritmo DP, benchmark, CSV y gráficas
├── compare_output.py # Gráfica comparativa DaC vs DP (tiempos)
├── outputs/          # Se crea al ejecutar (CSV e imágenes PNG)
└── README.md         # Este archivo
```

## Requisitos

- Python 3.10 o superior recomendado.
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar

Desde la carpeta del proyecto (`Proyecto2_ADA`):

| Comando | Descripción |
|---------|-------------|
| `python main.py dac` | Ejecuta solo el enfoque recursivo DaC: genera `outputs/dac_results.csv` y las figuras `dac_timing.png`, `dac_recursive_calls.png`. |
| `python main.py dp` | Ejecuta solo la DP bottom-up: `outputs/dp_results.csv`, `dp_timing.png`, `dp_operations.png`. |
| `python main.py all` | Ejecuta DaC y DP, todas las gráficas y **`dac_vs_dp_timing.png`** (comparativa de tiempos). |
| `python main.py compare` | Solo regenera **`dac_vs_dp_timing.png`** leyendo `dac_results.csv` y `dp_results.csv` (debes haber corrido antes `dac` y `dp`, o `all`). |

Carpeta de salida personalizada:

```bash
python main.py all -o C:\ruta\a\mis_resultados
```

También puedes ejecutar cada módulo de forma aislada (equivalente a `dac` o `dp` con salida por defecto en `outputs/`):

```bash
python egg_drop_dac.py
python egg_drop_dp.py
```

## Entradas de prueba

Los 30 pares `(huevos, pisos)` están definidos en `test_cases.py` y **no deben modificarse** si se quiere mantener la comparabilidad entre DaC y DP y con otros entregables del curso.

## Salidas

### DaC (`egg_drop_dac.py`)

- **CSV** `dac_results.csv`: columnas `eggs`, `floors`, `optimal_trials`, `time_ns`, `time_ms`, `recursive_calls`.
- **Gráficas**: tiempo (ms, mediana) vs pisos por serie de huevos (2, 3, 4); y llamadas recursivas vs pisos.

### DP (`egg_drop_dp.py`)

- **CSV** `dp_results.csv`: columnas `eggs`, `floors`, `optimal_trials`, `time_ns`, `time_ms`, `dp_operations`.
- **Gráficas**: tiempo vs pisos; operaciones DP (evaluaciones del bucle de transición) vs pisos.

### Comparativa (`compare_output.py` vía `main.py all` o `compare`)

- **`dac_vs_dp_timing.png`**: tres paneles (2, 3 y 4 huevos), eje X = pisos, eje Y = tiempo mediano (ms), curvas **DaC** y **DP** en el mismo gráfico por panel.

La medición usa `time.perf_counter_ns()`, varias repeticiones por caso y **mediana** del tiempo; hay una corrida de calentamiento por caso antes de medir.

## Divide and Conquer (recursivo, sin memoización)

Se aplica la recurrencia clásica: para cada piso de prueba `x`, el peor caso es `1 + max(resolver si se rompe, resolver si no se rompe)`; se minimiza sobre `x`. Los casos base cubren 0/1 pisos y un solo huevo.

Este enfoque se puede presentar como **descomposición recursiva** del espacio de decisiones (subproblemas con menos huevos o menos pisos). Sin embargo, **los mismos subproblemas aparecen muchas veces**: hay **subproblemas traslapados**, por lo que la recursión pura repite trabajo de forma exponencial en el peor caso respecto a parámetros razonables de `e` y `f`. La complejidad exacta en forma cerrada es engorrosa de expresar; en la práctica el árbol de llamadas explota rápido al crecer `f` (por eso en el reporte conviene contrastar con DP).

## Programación dinámica (bottom-up)

**Estado:** `dp[e][f]` = mínimo de intentos en el peor caso con `e` huevos y `f` pisos.

**Casos base** (coherentes con el código): una fila para un huevo (`dp[1][j] = j`), pisos 0 y 1 acotados en la construcción de la tabla.

**Transición:** para cada `x` de 1 a `f`, `peor = 1 + max(dp[e-1][x-1], dp[e][f-x])`; `dp[e][f] = min_x peor`.

Al rellenar la tabla en orden creciente de `e` y `f`, cada subproblema se calcula **una vez** y se reutiliza: se evita el retrabajo de la versión recursiva sin memoización.

**Complejidad:** tiempo aproximado **O(E · F²)** con la tabla clásica (tres bucles anidados); espacio **O(E · F)** para la matriz (sin optimizaciones de espacio adicionales).

## Fuentes 

- [Divide and Conquer vs Dynamic Programming (Baeldung)](https://www.baeldung.com/cs/divide-and-conquer-vs-dynamic-programming)
- [Egg Dropping Puzzle (GeeksforGeeks)](https://www.geeksforgeeks.org/dsa/egg-dropping-puzzle-dp-11/)
- [Egg dropping (Brilliant)](https://brilliant.org/wiki/egg-dropping/)
- [Sedgewick, Wayne: Algorithm Design (COS 226, Princeton, PDF)](https://www.cs.princeton.edu/courses/archive/fall21/cos226/lectures/AlgorithmDesign.pdf)
- [Super Egg Drop (LeetCode)](https://leetcode.com/problems/super-egg-drop/) (contexto y variantes del problema)
