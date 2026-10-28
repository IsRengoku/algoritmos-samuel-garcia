# Laboratorio 3 — Tabla hash: consulta de guías en Rutas del Caribe

**Autor:** Samuel Andrés García Sierra

## Cómo reproducir el experimento

Requisitos: Python 3.12 y `matplotlib`.

```bash
# 1. Instalar la única dependencia externa (solo para las gráficas)
python -m pip install matplotlib

# 2. Ubicarse en la carpeta del laboratorio
cd laboratorios/lab3-estructuras-datos

# 3. Ejecutar las pruebas (imprime "Todas las pruebas pasaron.")
python pruebas.py

# 4. Ejecutar la medición (imprime las tablas de tiempos y regenera las gráficas)
python medicion.py
```

---

## Parte 1 — Implementación y verificación

Código: [estructuras.py](estructuras.py) · [pruebas.py](pruebas.py)

- `ListaEnlazada.insertar` crea el nodo, lo enlaza con la cabeza actual y lo vuelve la nueva cabeza: Θ(1).
- `ListaEnlazada.buscar` recorre desde la cabeza con un `while` y devuelve `None` si llega al final.
- `TablaHash.hash` usa el método de la división, `k mod m`.
- `TablaHash.insertar` y `TablaHash.buscar` calculan la casilla y delegan en la `ListaEnlazada` de esa casilla (encadenamiento). No se usa `dict`, `set` ni `hash()`.
- `TablaHash.factor_carga` devuelve `tamano / m`.

**Cómo se verificó.** `pruebas.py` usa `assert`:

| Caso | Qué se comprueba |
|---|---|
| Serie de la situación problema | búsqueda exitosa (`1000000024` → "en reparto") e infructuosa (`1000000099` → `None`) en lista y tabla |
| Estructuras vacías | toda búsqueda devuelve `None`; α = 0 |
| Inserción al inicio | la última guía insertada queda como cabeza |
| Colisión forzada, m = 7 | 10, 24 y 17 dan `hash == 3`; las tres se encuentran; la casilla 3 mide 3 (por `tamano` y contando nodos); las demás quedan vacías; la guía 3, que cae en la misma casilla, no existe |
| Factor de carga | `factor_carga() == 3 / 7` tras las tres inserciones |
| 30 colecciones aleatorias | n entre 1 y 500, m ∈ {1, 2, 7, 97, 101, 1009}, semilla 2026; para cada guía existente y para 50 inexistentes, lista y tabla devuelven lo mismo |

---

## Parte 2 — Medición

Código: [medicion.py](medicion.py)

**Cómo se midió.**

- Guías: enteros distintos de diez dígitos con `random.Random(2026 + n).sample(...)`. En cada n, la lista y la tabla se cargan con **las mismas** guías.
- Búsquedas: 200 guías inexistentes generadas con `generar_guias_inexistentes` (semilla 7).
- Tabla del experimento A: m primo más cercano a n / 2, para α ≈ 2. Experimento B: n = 20.000 y m primo más cercano a n / α.
- Control: antes de medir, para una muestra de 200 guías existentes se exige que lista, tabla y estado esperado coincidan, y que las 200 inexistentes devuelvan `None` en ambas.
- Cronómetro: `time.perf_counter()` envuelve **solo** el ciclo de búsquedas. Cada medición se repite 5 veces y se toma la menor.
- En la tabla, las 200 búsquedas se repiten 50 veces dentro de la ventana (`VUELTAS_TABLA`), porque 200 búsquedas de ~0,3 µs suman unos 60 µs, un tiempo comparable al ruido del reloj. El tiempo reportado sigue siendo por búsqueda.
- Equipo: Windows 11, Python 3.12. Los tiempos absolutos cambian entre corridas; la forma de las curvas no.

### Experimento A — Lista frente a tabla

![Tiempo medio por búsqueda vs. n](graficas/lista_vs_tabla.png)

En escala lineal la tabla queda pegada al eje; en log-log se ve que es plana:

![Tiempo medio por búsqueda vs. n, escala log-log](graficas/lista_vs_tabla_log.png)

| n | m | α | Lista (µs) | Tabla (µs) | Lista / tabla | Cadena más larga |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 47 | 2,13 | 5,37 | 0,519 | 10 | 5 |
| 500 | 251 | 1,99 | 26,49 | 0,404 | 66 | 7 |
| 1.000 | 499 | 2,00 | 40,79 | 0,435 | 94 | 6 |
| 5.000 | 2.503 | 2,00 | 297,50 | 0,372 | 800 | 8 |
| 10.000 | 4.999 | 2,00 | 538,14 | 0,428 | 1.257 | 8 |
| 20.000 | 10.007 | 2,00 | 1.434,17 | 0,421 | 3.410 | 10 |
| 50.000 | 24.989 | 2,00 | 5.100,15 | 0,366 | 13.931 | 9 |

### Experimento B — Efecto del factor de carga

![Tiempo medio por búsqueda vs. α](graficas/tiempo_vs_alfa.png)

| α objetivo | m | α real | Tabla (µs) | Cadena más larga |
|---:|---:|---:|---:|---:|
| 0,25 | 79.999 | 0,25 | 0,292 | 4 |
| 0,5 | 40.009 | 0,50 | 0,277 | 5 |
| 1 | 19.997 | 1,00 | 0,317 | 8 |
| 2 | 10.007 | 2,00 | 0,373 | 10 |
| 4 | 4.999 | 4,00 | 0,473 | 16 |
| 6 | 3.331 | 6,00 | 0,673 | 15 |
| 8 | 2.503 | 7,99 | 1,289 | 20 |
| 10 | 1.999 | 10,01 | 1,680 | 21 |

---

## Parte 3 — Análisis

### 1. Costo teórico

En una lista enlazada, los elementos no están organizados de una manera que permita encontrar directamente una guía. Por esta razón, cuando buscamos una guía que no existe, es necesario recorrer todos los nodos para comprobar que no está almacenada. Como cada iteración del `while` tiene un costo constante y se realizan n iteraciones, la complejidad de esta operación es Θ(n).

En cambio, una tabla hash utiliza la operación `k mod m` para determinar en qué posición debería encontrarse una guía. Este cálculo y el acceso a la posición tienen un costo constante. Sin embargo, cuando se utiliza encadenamiento, también debemos recorrer la lista de elementos que hayan quedado almacenados en esa posición.

Si suponemos que las guías se distribuyen de manera uniforme, cada posición tendrá en promedio n / m elementos, valor que conocemos como el factor de carga α. Por lo tanto, el costo esperado de una búsqueda fallida es Θ(1 + α), donde el 1 representa el cálculo del hash y el acceso a la posición, mientras que α corresponde al recorrido de la cadena.

Es importante tener en cuenta que este resultado depende del supuesto de **hashing uniforme simple**, es decir, que cada guía tenga la misma probabilidad de ubicarse en cualquiera de las posiciones, independientemente de las demás.

Si todas las guías terminaran en una misma posición, tendríamos una lista de n elementos y la búsqueda volvería a tener complejidad Θ(n). Esto puede suceder, por ejemplo, cuando las claves presentan patrones relacionados con el tamaño de la tabla. Por eso, utilizar un número primo para m puede ayudar a reducir ciertos patrones de colisiones, aunque no garantiza por sí solo una distribución uniforme.

### 2. Comparación entre los resultados medidos y los esperados

Al comparar los resultados experimentales con el análisis teórico, podemos observar que el comportamiento de ambas estructuras se acerca a lo esperado.

Por ejemplo, cuando la cantidad de elementos pasa de 5.000 a 10.000, los resultados son los siguientes:

- **Lista enlazada:** el tiempo aumenta de 297,50 a 538,14 µs, lo que representa un incremento de 1,81 veces. Teóricamente, una complejidad Θ(n) indica que, al duplicar los elementos, el tiempo debería aumentar aproximadamente al doble. Por lo tanto, el resultado es bastante cercano a lo esperado.

- **Tabla hash:** el tiempo pasa de 0,372 a 0,428 µs, equivalente a un incremento de 1,15 veces. Aunque existe una pequeña diferencia, el comportamiento sigue siendo prácticamente constante y puede estar relacionado con las variaciones normales de las mediciones.

También resulta interesante observar que, al aumentar la cantidad de guías de 100 a 50.000, el tiempo de búsqueda en la tabla hash se mantiene aproximadamente entre 0,37 y 0,52 µs, sin mostrar una tendencia clara de crecimiento.

En el caso de la lista enlazada, el tiempo aumenta de forma aproximadamente lineal, aunque en los tamaños más grandes se presenta un crecimiento ligeramente mayor. Esto se puede observar en el costo por nodo, que pasa de aproximadamente 0,05 µs con 100 elementos a 0,10 µs con 50.000.

Una posible explicación es el comportamiento de la memoria caché. Cuando tenemos muchos nodos distribuidos en diferentes posiciones de memoria, acceder al siguiente elemento puede tardar más. Esto no cambia la complejidad Θ(n), pero sí puede aumentar el tiempo real de ejecución.

Por otra parte, en la segunda gráfica podemos analizar cómo influye el factor de carga α en el rendimiento de la tabla hash.

Cuando α se encuentra entre 0,25 y 1, los tiempos permanecen entre 0,28 y 0,32 µs. En este caso, el costo principal parece estar relacionado con el cálculo del hash y el acceso a la tabla.

A medida que aumenta el factor de carga, los tiempos también empiezan a crecer:

- Con α = 2, el tiempo es de 0,37 µs.
- Con α = 4, aumenta a 0,47 µs.
- Con α = 10, llega a 1,68 µs.

Estos resultados permiten observar el comportamiento esperado de Θ(1 + α), ya que existe un costo inicial prácticamente constante y otro que depende de la cantidad de elementos que debemos recorrer.

Aunque en el último tramo el crecimiento parece ser mayor de lo esperado para una relación lineal, esto podría estar relacionado con efectos de memoria caché u otros factores propios de la ejecución.

### 3. Colisiones en una tabla hash

Una colisión ocurre cuando dos o más claves diferentes generan la misma posición dentro de una tabla hash.

Por ejemplo, si tenemos una tabla de tamaño m = 7 y aplicamos la función `k mod m` a las guías 10, 24 y 17, obtenemos la posición 3 en los tres casos.

Esto demuestra que las colisiones pueden presentarse incluso cuando todavía existen posiciones disponibles en la tabla, debido a que diferentes claves pueden producir el mismo resultado.

Además, cuando almacenamos una cantidad considerable de elementos, la probabilidad de que dos coincidan en una misma posición aumenta. Este comportamiento se puede relacionar con la conocida paradoja del cumpleaños.

En el experimento B se observa una situación similar: aunque la tabla tenía 79.999 posiciones para almacenar 20.000 guías, la posición más ocupada llegó a contener cuatro elementos.

Para manejar estas colisiones existen diferentes alternativas, entre las que podemos destacar el encadenamiento y el direccionamiento abierto.

#### Encadenamiento

Este método consiste en almacenar una lista enlazada en cada posición de la tabla. Cuando varias guías generan el mismo índice, se agregan a la lista correspondiente.

En el ejemplo anterior, la posición 3 podría contener la cadena:

```text
17 → 24 → 10
```

Su principal ventaja es que resulta sencillo de implementar y permite almacenar más elementos que posiciones disponibles, es decir, trabajar con un factor de carga mayor que 1. Además, eliminar una guía consiste en retirar su nodo de la lista.

Como desventaja, necesita memoria adicional para almacenar los punteros y puede presentar un menor rendimiento cuando las listas son largas o los nodos se encuentran dispersos en memoria.

#### Direccionamiento abierto

A diferencia del encadenamiento, este método almacena todos los elementos directamente dentro del arreglo. Cuando una posición está ocupada, se busca otra disponible siguiendo una secuencia de sondeo.

Por ejemplo, utilizando sondeo lineal y una tabla inicialmente vacía, las guías quedarían distribuidas así:

- Guía 10: posición 3.
- Guía 24: posición 4.
- Guía 17: posición 5.

Una de sus ventajas es que no necesita punteros adicionales y los elementos permanecen dentro de una estructura de memoria contigua.

Sin embargo, requiere que el factor de carga sea menor que 1. Además, cuando la tabla empieza a llenarse, aumenta la cantidad de posiciones que debemos revisar y pueden formarse agrupaciones de elementos, lo que afecta el rendimiento. La eliminación también requiere un manejo especial para no interrumpir las búsquedas posteriores.

### 4. Tabla hash o árbol de búsqueda

Si necesitamos consultar una guía específica, la tabla hash es una alternativa eficiente. Sin embargo, cuando queremos buscar todas las guías que se encuentren dentro de un rango, su funcionamiento deja de ser tan conveniente.

Esto sucede porque la función `k mod m` no conserva el orden de los valores. Dos números consecutivos pueden quedar almacenados en posiciones distintas de la tabla.

Por esta razón, para encontrar todas las guías entre X y Y tendríamos que recorrer los n elementos, con un costo de Θ(n), o realizar búsquedas individuales para cada número del rango.

Esta última opción tampoco sería muy eficiente si el intervalo es demasiado amplio. Por ejemplo, podríamos tener un rango de un millón de números y solamente 50 guías registradas, lo que implicaría realizar una gran cantidad de búsquedas innecesarias.

Para este tipo de consultas, un árbol binario de búsqueda resulta más apropiado porque mantiene los elementos ordenados.

Su funcionamiento consiste en localizar primero el límite inferior del rango y después recorrer los elementos en orden hasta superar el límite superior, evitando las ramas que no contienen valores de interés.

El costo de esta operación es O(h + k), donde h representa la altura del árbol y k la cantidad de elementos encontrados.

No obstante, también debemos considerar que el rendimiento depende de cómo esté construido el árbol.

Si insertamos 400.000 guías ordenadas en un árbol binario sin balancear, cada nuevo elemento quedaría a la derecha del anterior. Esto produciría una estructura similar a una lista enlazada, con una altura de 399.999 y búsquedas que podrían necesitar aproximadamente 400.000 comparaciones.

Para evitar este problema, podemos utilizar árboles balanceados, como AVL o rojinegros, que mantienen una altura del orden de log₂(n).

En el caso de 400.000 elementos, log₂(400.000) es aproximadamente 19. Esto permite reducir considerablemente la cantidad de comparaciones necesarias frente a un árbol que no esté balanceado.

### 5. Recomendación para la jefa de operaciones

Teniendo en cuenta los resultados obtenidos, considero que la mejor alternativa sería combinar una tabla hash con un árbol de búsqueda balanceado, ya que cada estructura responde mejor a un tipo de consulta diferente.

La tabla hash se utilizaría para buscar una guía específica de manera rápida, mientras que el árbol permitiría realizar consultas por rangos sin necesidad de recorrer todos los registros.

Ambas estructuras podrían mantener referencias a los mismos envíos, evitando duplicar toda la información. Sin embargo, esta solución requiere memoria adicional para los índices y también implica actualizar ambas estructuras cuando se inserta o elimina un registro.

En el caso de la tabla hash, sería importante aumentar su capacidad conforme crezca la cantidad de envíos, procurando mantener un factor de carga cercano a 2. Para ello, se podría utilizar un tamaño primo adecuado y realizar un redimensionamiento cuando sea necesario.

#### Estimación del rendimiento con 5.000.000 de envíos

A partir de los resultados experimentales, podemos realizar una estimación aproximada del comportamiento que tendría cada estructura con cinco millones de registros. Es importante aclarar que estos valores son **proyecciones** y no mediciones reales.

**Lista enlazada**

En la medición de mayor tamaño, recorrer 50.000 elementos tomó aproximadamente 5.100 µs. Si dividimos este tiempo entre la cantidad de elementos, obtenemos un costo cercano a 0,10 µs por nodo.

Manteniendo esa proporción:

```text
5.000.000 × 0,10 µs = 500.000 µs ≈ 0,5 segundos
```

Por lo tanto, una búsqueda fallida podría tardar alrededor de medio segundo. Incluso podría ser mayor, considerando que en los experimentos el costo por nodo aumentó con el tamaño de la lista.

**Tabla hash con α ≈ 2**

En este caso, si aumentamos el tamaño de la tabla junto con la cantidad de elementos, el factor de carga se mantiene controlado.

Según los resultados del experimento, para α = 2 se obtuvo un tiempo cercano a 0,37 µs. Por esta razón, podríamos tomar como referencia un tiempo aproximado de 0,4 µs por búsqueda, posiblemente inferior a 1 µs si las condiciones de ejecución se mantienen similares.

**¿Qué pasaría si no aumentamos el tamaño de la tabla?**

Si mantenemos una tabla con solamente 25.000 posiciones para almacenar cinco millones de guías, el factor de carga sería:

```text
α = 5.000.000 / 25.000 = 200
```

Esto significa que cada posición tendría, en promedio, 200 elementos. Si tomamos como referencia el costo de 0,10 µs por nodo utilizado anteriormente, recorrer una cadena completa podría tardar aproximadamente:

```text
200 × 0,10 µs = 20 µs
```

Aunque seguiría siendo más rápido que recorrer una lista enlazada de cinco millones de elementos, ya no tendríamos el mismo rendimiento que con un factor de carga bajo.

Este último cálculo es solamente una aproximación, porque el costo por nodo en una tabla hash no necesariamente será igual al de una lista enlazada.

### Conclusión

A partir de los experimentos, podemos concluir que la tabla hash es mucho más conveniente para realizar búsquedas puntuales, siempre que se mantenga una buena distribución de las claves y se controle el factor de carga.

Sin embargo, para consultas por rangos, el árbol balanceado ofrece una ventaja importante al conservar los elementos ordenados.

Por esta razón, utilizar ambas estructuras de manera complementaria sería una buena decisión para un sistema que deba manejar millones de envíos y responder a diferentes tipos de consultas. Aunque implica un mayor consumo de memoria y algo más de trabajo al actualizar los datos, considero que es una inversión razonable frente a la mejora en los tiempos de respuesta.