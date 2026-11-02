# Retroalimentación — Laboratorio 03: Estructuras de datos

**Estudiante:** Samuel Andrés García Sierra · **Laboratorio:** Laboratorio evaluativo 03 — Estructuras de datos
**Fecha límite:** 2026-11-01 23:59 · **Versión revisada:** commit `96e658c`

Muy buen trabajo: la implementación es limpia, las gráficas son claras y el informe se apoya en sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 19 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 23 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **97 / 100** |
| **Nota (0–5)** | **4.85** |

## 1. Corrección conceptual (19 / 20)
**Lo que hizo bien:**
- Explica bien la colisión con el ejemplo de 10, 24 y 17 con m = 7, y compara encadenamiento con direccionamiento abierto, con ventajas y costos de cada uno.
- Justifica por qué la tabla no sirve para rangos y qué ofrece el árbol de búsqueda.
- Recomienda una combinación (tabla hash más árbol balanceado) y declara que la estimación a 5.000.000 de envíos es una proyección, explicando su razonamiento.

**Lo que puede mejorar (y cómo corregirlo):**
- Para el árbol degenerado da la altura y las comparaciones de una sola búsqueda, pero no el trabajo total de insertar las 400.000 guías una a una.
  → *Cómo corregirlo:* piense cuántas comparaciones cuesta cada inserción cuando el árbol ya tiene k nodos en una sola fila, y súmelas para todas las guías.
- La estimación de la tabla sin redimensionar es útil, pero la de la lista podría decir con más claridad qué tanto pesa el efecto de la memoria caché que usted mismo menciona.
  → *Cómo corregirlo:* indique un rango (mínimo y máximo) en lugar de un solo valor y explique de dónde sale cada extremo.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Justifica el Θ(n) de la lista y el Θ(1 + α) de la tabla, nombra el supuesto de hashing uniforme y explica que si todas las guías caen en una casilla se vuelve a Θ(n).

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Ambas estructuras devuelven lo correcto en búsquedas exitosas e infructuosas; la colisión forzada con m = 7 y el factor de carga funcionan.
- La tabla reutiliza la lista enlazada y no usa `dict`, `set` ni `hash()`.
- Las pruebas cubren treinta colecciones aleatorias y casos extra (vacías, m inválido).
- Todas las funciones tienen *docstrings* con `Args` y `Returns` y *type hints*.

## 4. Calidad del análisis de las gráficas (23 / 25)
**Lo que hizo bien:**
- Ambas gráficas tienen título, ejes rotulados, y la primera muestra las dos curvas en los mismos ejes con leyenda. Cubren siete valores de n y ocho de α.
- Los valores que cita en el informe coinciden con lo que muestran las gráficas (por ejemplo, la lista cerca de 5.100 µs con 50.000 guías y la tabla cerca de 1,7 µs con α = 10).
- Calcula el factor de crecimiento entre 5.000 y 10.000 guías y lo contrasta con Θ(n) y Θ(1).

**Lo que puede mejorar (y cómo corregirlo):**
- Para α no calcula factores de crecimiento, solo describe la tendencia; la comparación con Θ(1 + α) queda más cualitativa.
  → *Cómo corregirlo:* tome dos valores de α de la segunda gráfica, calcule cuánto se multiplicó el tiempo y compárelo con lo que predice 1 + α.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- Siguió la estructura acordada (`laboratorios/lab3-estructuras-datos/`) con todos los archivos pedidos.
- El informe sigue el orden pedido, enlaza el código de cada parte, muestra las gráficas con rutas que funcionan y tiene instrucciones de reproducción.
- Hay cinco commits con mensajes descriptivos.

## ¿El código funciona?
Sí. Las pruebas pasan, ambas estructuras responden igual que una referencia y la medición corre completa y regenera las gráficas.
