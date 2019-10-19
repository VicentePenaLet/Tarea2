# Algoritmo Genetico

## Problema a Resolver

Este programa resuelve el problema de la mochila (Knapsack problem en ingles) no acotado. Este se refiere a un problema de optimización donde se desea maximizar el valor de elementos que se pueden incluir dentro de una mochila, sin superar el peso máximo que esta puede cargar.
De este modo, sea W un vector que contiene los pesos de los disntios objetos posibles, y V el vector que contiene los valores de estos elementos. Una solución al problema (no necesariamente optima) de dada por el vector S, siendo cada una de sus componentes la cantidad de elementos usada de cada tipo.
De este modo, el problema se reduce a maximizar la cantidad definida por el producto punto entre V y S, sujeto a que el producto punto entre W y S no supere el peso maximo.

En este caso un individuo coresponde a una machila, con una combinación de objetos (vector S).
Los genes del individuo estan representados por su vector de solucion (Vector S) un vector de tamaño fijo (El tamaño de la lista de objetos posibles).
La función de fitness utilizada corresponde a el valor total de los objetos de la mochila, esta se computa como el producto punto entre el vector S y el vector de Valores.

## Analisis de resultados

Se realizaron pruebas del algoritmo genetico para resolver el caso de la busqueda de string, y los resultados son las figuras 1, 2 y 3. Como se puede observar el algoritmo converge de manera mas rapida a medida que aumenta el tamaño de la población, sin embargo, cuando se llega  aun tamaño lo suficientemente bueno, la mejora resulta marginal, pero el tiempo de ejecución de cada generación resulta mayor. Respecto a la tasa de mutaciones esta debe tener un valor no muy alto, ni muy bajo, cuando el valor es demasiado bajo, no existe suficiente variabilidad para generar los caracteres que no existen en la población, por otro lado, si esta es demasiado alta se realizan cambios de manera muy rapida a los individuos buenos que no logran ser compensados por la selección.

![Resultados para palabra de largo 8](https://github.com/VicentePenaLet/Tarea2/blob/master/word_lenght_8_heatmap.png?raw=true)

Figura 1: Resultados para palabra de largo 8

![Resultados para palabra de largo 28](https://github.com/VicentePenaLet/Tarea2/blob/master/word_lenght_28_heatmap.png?raw=true)

Figura 2: Resultados para palabra de largo 28

![Resultados para palabra de largo 128](https://github.com/VicentePenaLet/Tarea2/blob/master/word_lenght_128_heatmap.png?raw=true)

Figura 3: Resultados para palabra de largo 128

Con esto en cuenta, se puede observar que el algoritmo efectivamente logra encontrar soluciones al problema, no existe una manera de verificar si la solucion obtenida es optima sin conocer a priori la solución ótpima, pero si se puede verificar que la solucion obtenida es suficientemente buena para los propositos requeridos. Con esto, el algoritmo genetico permite obtener soluciones a problemas de optimización que de otros mdoos serpian demasiado complejos de resolver. 
