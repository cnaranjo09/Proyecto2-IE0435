# Proyecto2-IE0435
# Optimización de Rutas en Redes Simuladas mediante Particle Swarm Optimization (PSO)

## Descripción

Este proyecto implementa y compara distintos algoritmos para la búsqueda y optimización de rutas en redes de computadores simuladas representadas mediante grafos.

El objetivo principal es analizar el desempeño de la técnica de Inteligencia de Enjambres **Particle Swarm Optimization (PSO)** en la búsqueda de rutas eficientes entre un nodo origen y un nodo destino, comparándola con algoritmos clásicos de búsqueda como **Dijkstra** y **A\***.

Las redes utilizadas son simuladas y generadas mediante grafos ponderados, donde cada nodo representa un router y cada enlace posee atributos asociados como latencia, congestión y costo de transmisión.

---

# Objetivos

## Objetivo General

Desarrollar e implementar un sistema de optimización de rutas basado en Particle Swarm Optimization (PSO) y compararlo con algoritmos clásicos de búsqueda en grafos que representan redes de computadores simuladas.

## Objetivos Específicos

- Modelar redes de computadores como grafos ponderados.
- Implementar los algoritmos Dijkstra y A*.
- Implementar un algoritmo PSO adaptado al problema de búsqueda de rutas.
- Diseñar una función de costo basada en múltiples criterios.
- Comparar desempeño, calidad de solución y tiempo de ejecución.
- Analizar el comportamiento de los algoritmos bajo diferentes tamaños de red.

---

# Fundamento Teórico

## Redes como Grafos

Una red de computadores puede representarse como un grafo:

- Nodo → Router
- Arista → Enlace de comunicación

Cada enlace posee atributos tales como:

- Latencia
- Congestión
- Número de saltos
- Costo

Ejemplo:

```text
A ---- B ---- D
|      |
|      |
C ---- E
```

---

## Dijkstra

Algoritmo clásico para encontrar la ruta de menor costo entre dos nodos de un grafo ponderado.

Características:

- Garantiza solución óptima.
- Complejidad relativamente baja.
- Utilizado ampliamente en protocolos de enrutamiento.

---

## A*

Algoritmo heurístico de búsqueda informada.

Características:

- Utiliza una función heurística.
- Generalmente explora menos nodos que Dijkstra.
- Puede encontrar soluciones más rápidamente.

---

## Particle Swarm Optimization (PSO)

PSO es una técnica de Inteligencia de Enjambres inspirada en el comportamiento colectivo de:

- Bandadas de aves
- Bancos de peces

Cada partícula representa una solución candidata y explora el espacio de búsqueda utilizando:

- Experiencia propia
- Experiencia global del enjambre

En este proyecto cada partícula representará una ruta posible entre un nodo origen y un nodo destino.

---

# Arquitectura General

```text
             Generación de Red
                      │
                      ▼
             Grafo Ponderado
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    Dijkstra         A*           PSO
        │             │             │
        └─────────────┼─────────────┘
                      ▼
              Comparación
                      ▼
               Resultados
```

---

# Función Objetivo

El algoritmo PSO buscará minimizar una función de costo definida como:

```text
Costo =
α × Latencia +
β × Congestión +
γ × Saltos
```

Donde:

- α = peso de la latencia
- β = peso de la congestión
- γ = peso del número de saltos

Los pesos podrán modificarse para analizar distintos escenarios.

---

# Escenarios de Prueba

Se generarán diferentes redes utilizando NetworkX.

## Escenario 1

Red pequeña

```text
10 nodos
```

## Escenario 2

Red mediana

```text
50 nodos
```

## Escenario 3

Red grande

```text
100 nodos
```



---

# Métricas de Evaluación

Se analizarán las siguientes métricas:

## Costo Total

Costo acumulado de la ruta encontrada.

## Número de Saltos

Cantidad de nodos recorridos.

## Tiempo de Ejecución

Tiempo requerido para encontrar una solución.

## Escalabilidad

Comportamiento del algoritmo al aumentar el tamaño de la red.

## Calidad de Solución

Comparación entre la solución obtenida por PSO y la solución óptima encontrada por Dijkstra.

---

# Tecnologías Utilizadas

- Python 3.12+
- NetworkX
- NumPy
- Pandas
- Matplotlib

---

# Estructura del Proyecto

```text
Proyecto_PSO_Routing/
│
├── data/
│   └── graphs/
│
├── results/
│   ├── figures/
│   ├── tables/
│   └── logs/
│
├── reports/
│   ├── proposal.md
│   ├── progress_report.md
│   └── final_report.md
│
├── src/
│   ├── generate_graph.py
│   ├── dijkstra.py
│   ├── astar.py
│   ├── pso.py
│   ├── evaluation.py
│   └── main.py
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

# Instalación

## Clonar repositorio

```bash
git clone https://github.com/usuario/Proyecto_PSO_Routing.git

cd Proyecto_PSO_Routing
```

---

## Crear entorno virtual

### Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Instalar dependencias

```bash
pip install networkx numpy pandas matplotlib
```

---

# Ejecución

## Generar red

```bash
python src/generate_graph.py
```

---

## Ejecutar comparación de algoritmos

```bash
python src/main.py
```

---

# Resultados Esperados

Tabla comparativa:

| Algoritmo | Costo | Saltos | Tiempo (s) |
|------------|--------|---------|------------|
| Dijkstra | 00 | 00 | 0.000 |
| A* | 00 | 00 | 0.000 |
| PSO | 00 | 00 | 0.000 |

---


<!-- Este es un comentario oculto y no se verá en el README 

# Posibles Extensiones

- Inclusión de congestión dinámica.
- Topologías reales de Internet.
- Comparación con algoritmos genéticos.
- Implementación de Ant Colony Optimization (ACO).
- Redes definidas por software (SDN).
- Optimización multiobjetivo.
-->
---

# Resultados Esperados del Proyecto

Se espera demostrar:

- Viabilidad del uso de PSO en problemas de enrutamiento.
- Diferencias entre algoritmos clásicos e inteligencia de enjambres.
- Impacto del tamaño de la red en el desempeño.
- Ventajas y limitaciones de PSO en grafos.

---


