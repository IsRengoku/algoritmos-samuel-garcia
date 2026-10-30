# Retroalimentación — Laboratorio 2: Dividir y vencer

**Estudiante:** Samuel Andrés García Sierra · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-10-30 23:59 · **Versión revisada:** commit `9b9569d`

Excelente trabajo: entrega completa, correcta y muy bien argumentada.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 20 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 25 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **100 / 100** |
| **Nota (0–5)** | **5.00** |

## 1. Corrección conceptual (20 / 20)
**Lo que hizo bien:**
- Identificó que divide y vencerás empieza a ganar entre n = 10 y n = 50, con los datos de su tabla, y explicó por qué la fuerza bruta gana con pocos datos (costos fijos de las llamadas recursivas).
- Comparó con el máximo de un arreglo: combinar cuesta una sola comparación, la recurrencia da `Θ(n)` y dividir no mejora nada. Explicó bien cuándo sí conviene dividir.
- Recomendó divide y vencerás y estimó el tiempo para 1.000.000 de registros declarándolo como estimación, escalando según el crecimiento de cada algoritmo y no de forma lineal.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Planteó `T(n) = 2T(n/2) + Θ(n)` explicando de dónde sale cada término.
- Resolvió con el método maestro, comparando `f(n)` con `n^(log₂ 2)` y verificando que aplica el caso 2.
- Justificó el `Θ(n²)` de la fuerza bruta con la suma `n(n+1)/2` y aclaró por qué acumular la suma evita llegar a `Θ(n³)`.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Las tres funciones dan la suma correcta en todos los casos pedidos (serie de ocho días, un elemento, negativos, positivos, tramo cruzado) y coinciden en las listas aleatorias.
- `subarreglo_maximo` resuelve los tres casos sin llamar a la fuerza bruta, y ninguna función modifica la lista recibida.
- Todas las funciones tienen *type hints* y *docstrings* con `Args` y `Returns`, y hay dos líneas en blanco entre ellas.
- Las pruebas comprueban además que la lista no cambia y que lo reportado realmente suma lo que dice.

## 4. Calidad del análisis de las gráficas (25 / 25)
**Lo que hizo bien:**
- La gráfica tiene título, ambos ejes rotulados, leyenda y las dos curvas en los mismos ejes, con ocho tamaños (dos menores de 100 y uno de 8000).
- Los valores del informe coinciden con lo que se lee en la gráfica (fuerza bruta cerca de 2,9 s y divide y vencerás casi pegado al eje en n = 8000).
- Calculó el factor al duplicar `n` para ambos algoritmos (×4,36 y ×2,11 en 4000 → 8000) y lo contrastó correctamente con `Θ(n²)` y `Θ(n log n)`.
- Agregó una gráfica log-log y una tabla que ayudan a leer los tamaños pequeños, y repitió cada medición cinco veces.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- El informe sigue el orden pedido, con su nombre, instrucciones de reproducción, enlaces al código en cada parte y las gráficas visibles.
- Tiene cinco commits descriptivos sobre el laboratorio.
- La carpeta del laboratorio está en `laboratorios/lab2-divide-y-vencer/`, ubicación válida, con todos los archivos del entregable.

## ¿El código funciona?
Sí. Las pruebas pasan sin errores, ambos algoritmos devuelven la misma suma en todos los tamaños y la medición genera las dos gráficas sin problemas.
