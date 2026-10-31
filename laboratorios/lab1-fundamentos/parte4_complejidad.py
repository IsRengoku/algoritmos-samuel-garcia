"""Compara tiempos y extrapola: python parte4_complejidad.py.

Sin argumentos. Produce CSV de mediciones y estimaciones y una gráfica.
Las extrapolaciones no certifican el tiempo del sistema real.
"""
import csv
from math import log2
from pathlib import Path
from statistics import mean
from time import perf_counter

import matplotlib
import matplotlib.pyplot as plt

from algoritmos import insertion_sort, merge_sort
from datos import generar_aleatorio

matplotlib.use('Agg')

TAMANOS = (100, 200, 400, 800, 1600, 3200, 6400)
SEMILLAS = (42, 43, 44, 45, 46)
ALGORITMOS = {'insertion_sort': insertion_sort, 'merge_sort': merge_sort}
OBJETIVO = 1_200_000


def guardar_csv(ruta: Path, filas: list[dict]) -> None:
    """Guarda filas en un CSV sin redondear, para permitir auditoría.

    Args:
        ruta: archivo CSV de destino; se sobrescribe si existe.
        filas: registros a guardar; las claves de la primera fila
            definen las columnas.
    """
    with ruta.open('w', encoding='utf-8', newline='') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def ejecutar() -> None:
    """Compara ambos algoritmos sobre entradas idénticas y extrapola.

    Mide solo las llamadas a insertion_sort y merge_sort, alternando su
    orden en cada semilla. Guarda las mediciones en
    resultados/parte4_mediciones.csv, la gráfica en
    graficas/parte4_tiempo.png y la extrapolación a 1.200.000 registros
    en resultados/parte4_estimaciones.csv.

    Raises:
        AssertionError: si alguna salida no coincide con el orden
            descendente esperado.
    """
    raiz = Path(__file__).resolve().parent
    (raiz / 'resultados').mkdir(exist_ok=True)
    (raiz / 'graficas').mkdir(exist_ok=True)
    filas = []
    for n in TAMANOS:
        esperado = list(range(n, 0, -1))
        for repeticion, semilla in enumerate(SEMILLAS):
            datos = generar_aleatorio(n, semilla)
            # Alternar el orden evita el sesgo de ejecutar siempre uno primero.
            orden = list(ALGORITMOS.items())
            if repeticion % 2:
                orden.reverse()
            for nombre, algoritmo in orden:
                inicio = perf_counter()
                salida, comparaciones = algoritmo(datos)
                segundos = perf_counter() - inicio
                if salida != esperado:
                    raise AssertionError(
                        f'Resultado incorrecto: {nombre}, n={n}'
                    )
                filas.append({
                    'algoritmo': nombre, 'n': n, 'semilla': semilla,
                    'comparaciones': comparaciones, 'segundos': segundos,
                })
        print(f'n={n}: ambos algoritmos, cinco semillas', flush=True)
    guardar_csv(raiz / 'resultados' / 'parte4_mediciones.csv', filas)

    figura, eje = plt.subplots(figsize=(9, 5))
    for nombre in ALGORITMOS:
        tiempos = [
            mean(float(f['segundos']) for f in filas
                 if f['algoritmo'] == nombre and f['n'] == n)
            for n in TAMANOS
        ]
        eje.plot(TAMANOS, tiempos, marker='o', label=nombre)
    eje.set(
        xlabel='Tamaño de entrada (registros)',
        ylabel='Tiempo de ejecución (s)',
        title='Escenario A — media de cinco semillas por tamaño',
    )
    eje.grid(alpha=0.3)
    eje.legend()
    figura.tight_layout()
    figura.savefig(raiz / 'graficas' / 'parte4_tiempo.png', dpi=160)
    plt.close(figura)

    # Ajuste de un solo punto al mayor tamaño: estimación, no cota temporal.
    base = TAMANOS[-1]
    estimaciones = []
    for nombre in ALGORITMOS:
        tiempo = mean(float(f['segundos']) for f in filas
                      if f['algoritmo'] == nombre and f['n'] == base)
        factor = ((OBJETIVO / base) ** 2 if nombre == 'insertion_sort' else
                  OBJETIVO * log2(OBJETIVO) / (base * log2(base)))
        estimado = tiempo * factor
        estimaciones.append({
            'algoritmo': nombre, 'n_base': base, 'segundos_base': tiempo,
            'n_objetivo': OBJETIVO, 'factor': factor,
            'segundos_estimados': estimado, 'horas_estimadas': estimado / 3600,
            'segundos_doble_velocidad_ideal': estimado / 2,
        })
        print(f'{nombre}: base={tiempo:.6f} s; estimado={estimado:.3f} s '
              f'({estimado / 3600:.3f} h); '
              f'doble velocidad ideal={estimado / 2:.3f} s')
    guardar_csv(raiz / 'resultados' / 'parte4_estimaciones.csv', estimaciones)
    print('Gráfica y CSV de la Parte 4 guardados.')


if __name__ == '__main__':
    ejecutar()
