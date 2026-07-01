# Resultados Experimentales

## Configuración de los experimentos

Con el objetivo de comparar el desempeño de diferentes algoritmos de búsqueda y optimización para el cálculo de rutas en redes de comunicación, se realizaron experimentos utilizando una red generada automáticamente mediante el modelo de [Barabási-Albert](https://www.mdpi.com/2071-1050/17/3/1095)

Para obtener resultados estadísticamente representativos, la evaluación no se realizó sobre una única topología, sino sobre múltiples redes generadas con diferentes semillas aleatorias. En cada red se seleccionaron distintos pares origen-destino y se ejecutaron los tres algoritmos implementados:

- Dijkstra
- A*
- Optimización por Enjambre de Partículas (PSO)

La configuración utilizada fue la siguiente:

| Parámetro | Valor |
|-----------|------:|
| Número de redes evaluadas | 10 |
| Nodos por red | 50 |
| Enlaces por nodo | 3 |
| Casos por red | 20 |
| Total de casos evaluados | 200 |
| Corridas independientes de PSO por caso | 10 |

En total se ejecutaron **600 experimentos** (200 casos × 3 algoritmos), mientras que el algoritmo PSO realizó además múltiples ejecuciones independientes para reducir el efecto de la aleatoriedad inherente al método.

---

# Métricas evaluadas

Para cada algoritmo se registraron las siguientes métricas:

- Costo total de la ruta.
- Número de saltos.
- Tiempo de ejecución.
- Error porcentual respecto a la solución óptima obtenida mediante Dijkstra.

El error porcentual se calculó como

\[
Error=\frac{Costo_{algoritmo}-Costo_{Dijkstra}}{Costo_{Dijkstra}}\times100
\]

donde Dijkstra se utilizó como referencia al ser un algoritmo exacto para grafos con pesos positivos.

---

# Resultados obtenidos

| Algoritmo | Costo promedio | Tiempo promedio (ms) | Saltos promedio | Error promedio |
|-----------|---------------:|---------------------:|----------------:|---------------:|
| Dijkstra | 58.84 | 0.307 | 2.66 | 0.00 % |
| A* | 58.84 | 10.491 | 2.66 | 0.00 % |
| PSO | 59.17 | 14.891 | 2.60 | 0.44 % |

---

# Análisis de resultados

Los resultados muestran que tanto Dijkstra como A* encontraron exactamente las mismas rutas para todos los casos evaluados, obteniendo el mismo costo promedio y un error del 0 %. Esto confirma que ambas implementaciones producen soluciones óptimas bajo las condiciones del experimento.

El algoritmo Dijkstra presentó el menor tiempo promedio de ejecución (0.307 ms), convirtiéndose en el método más eficiente para el tamaño de red utilizado.

Por su parte, el algoritmo A* obtuvo exactamente la misma calidad de solución que Dijkstra, aunque con un tiempo promedio mayor. Esta diferencia se debe principalmente al cálculo de la heurística empleada durante la búsqueda, lo cual incrementa el tiempo total de ejecución en la implementación desarrollada.

El algoritmo PSO mostró un comportamiento consistente con el esperado para una metaheurística. A diferencia de Dijkstra y A*, PSO no garantiza encontrar siempre la solución óptima, sino que busca aproximaciones mediante un proceso iterativo inspirado en el comportamiento colectivo de enjambres.

En promedio, PSO obtuvo un costo de ruta de 59.17 frente al valor óptimo de 58.84, lo que representa un error medio de únicamente 0.44 %. Esto indica que el algoritmo fue capaz de encontrar rutas muy cercanas al óptimo en la mayoría de los casos.

Asimismo, el número promedio de saltos obtenido por PSO fue ligeramente inferior (2.60 frente a 2.66). Esto demuestra que minimizar el número de enlaces recorridos no implica necesariamente minimizar el costo total de la ruta, ya que el costo depende también de la latencia y el nivel de congestión asignados a cada enlace.

---

# Discusión

Los experimentos evidencian las diferencias fundamentales entre los algoritmos evaluados.

Dijkstra y A* pertenecen a la categoría de algoritmos exactos de búsqueda sobre grafos. Ambos garantizan encontrar la ruta óptima siempre que las condiciones del problema sean adecuadas.

Por el contrario, PSO corresponde a una técnica de optimización basada en inteligencia de enjambres. En lugar de explorar sistemáticamente todos los caminos posibles, genera soluciones candidatas y las mejora iterativamente mediante un proceso de cooperación entre partículas.

Aunque PSO presentó un tiempo de ejecución superior y un pequeño error respecto a la solución óptima, su desempeño fue notablemente cercano al de los algoritmos exactos, obteniendo rutas con una diferencia promedio inferior al 1 %.

Este comportamiento resulta especialmente relevante para problemas donde el espacio de búsqueda es muy grande o donde los algoritmos exactos dejan de ser computacionalmente viables, ya que las metaheurísticas permiten obtener soluciones de alta calidad con un costo computacional razonable.

---

# Conclusiones

A partir de los experimentos realizados pueden extraerse las siguientes conclusiones:

- Dijkstra obtuvo el mejor desempeño general, encontrando siempre la solución óptima con el menor tiempo de ejecución.

- A* alcanzó exactamente la misma calidad de solución que Dijkstra, confirmando el correcto funcionamiento de su implementación.

- PSO logró aproximarse notablemente a la solución óptima, presentando un error promedio de únicamente 0.44 %, lo que demuestra la capacidad de las técnicas de inteligencia de enjambres para resolver problemas de optimización sobre redes.

- El incremento del número de nodos y la evaluación sobre múltiples topologías permitieron realizar una comparación más representativa entre los algoritmos, evitando que los resultados dependieran de una única configuración de red.

En conjunto, los resultados muestran que las técnicas de búsqueda exacta continúan siendo la mejor alternativa para redes de tamaño moderado, mientras que los métodos bioinspirados como PSO constituyen una opción prometedora cuando se requieren soluciones aproximadas en espacios de búsqueda de mayor complejidad.
