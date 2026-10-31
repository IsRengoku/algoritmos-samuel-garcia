"""Mide insertion sort: python parte3_casos.py (sin argumentos)."""
import csv
from pathlib import Path
from statistics import mean
from time import perf_counter

import matplotlib
import matplotlib.pyplot as plt

from algoritmos import insertion_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso

matplotlib.use('Agg')

TAMANOS = (100, 200, 400, 800, 1600, 3200, 6400)
SEMILLAS = (42, 43, 44, 45, 46)
ESCENARIOS = {
    'A — Aleatorio': generar_aleatorio,
    'B — Casi ordenado': generar_casi_ordenado,
    'C — Inverso': lambda n, semilla: generar_inverso(n),
    'Control — Mejor caso': lambda n, semilla: list(range(n, 0, -1)),
}


def ejecutar() -> None:
    """Mide insertion sort en los cuatro escenarios y guarda la evidencia.

    Para cada tamaño, escenario y repetición genera la entrada antes del
    cronómetro, mide solo la llamada a insertion_sort y valida el
    resultado después. Guarda cada medición en
    resultados/parte3_mediciones.csv y las gráficas de las medias en
    graficas/parte3_comparaciones.png y graficas/parte3_tiempo.png.

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
        for nombre, generar in ESCENARIOS.items():
            for repeticion, semilla in enumerate(SEMILLAS, start=1):
                datos = generar(n, semilla)
                inicio = perf_counter()
                salida, comparaciones = insertion_sort(datos)
                segundos = perf_counter() - inicio
                if salida != esperado:
                    raise AssertionError(
                        f'Resultado incorrecto: {nombre}, n={n}'
                    )
                filas.append({
                    'escenario': nombre, 'n': n, 'repeticion': repeticion,
                    'semilla': semilla if nombre[0] in ('A', 'B') else '',
                    'comparaciones': comparaciones, 'segundos': segundos,
                })
        print(f'n={n}: cuatro entradas, cinco ejecuciones por entrada',
              flush=True)

    with (raiz / 'resultados' / 'parte3_mediciones.csv').open(
        'w', newline='', encoding='utf-8'
    ) as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)

    for campo, etiqueta in (
        ('comparaciones', 'Comparaciones entre elementos'),
        ('segundos', 'Tiempo de ejecución (s)'),
    ):
        figura, eje = plt.subplots(figsize=(9, 5))
        for nombre in ESCENARIOS:
            medias = [mean(
                fila[campo] for fila in filas
                if fila['escenario'] == nombre and fila['n'] == n
            ) for n in TAMANOS]
            eje.plot(TAMANOS, medias, marker='o', label=nombre,
                     linestyle='--' if nombre.startswith('Control') else '-')
        eje.set(
            xlabel='Cantidad de registros (n)', ylabel=etiqueta,
            title='Insertion sort descendente — media de cinco ejecuciones',
        )
        eje.grid(alpha=0.3)
        eje.legend()
        figura.tight_layout()
        sufijo = 'comparaciones' if campo == 'comparaciones' else 'tiempo'
        figura.savefig(raiz / 'graficas' / f'parte3_{sufijo}.png', dpi=160)
        plt.close(figura)
    print('CSV y gráficas guardados en resultados/ y graficas/.')


if __name__ == '__main__':
    ejecutar()
