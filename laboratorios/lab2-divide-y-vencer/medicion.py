"""Experimento: tiempo de ejecucion de fuerza bruta vs. divide y venceras."""

import random
import time
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo  # noqa: E402

SEMILLA = 2026
TAMANOS = [10, 50, 100, 500, 1000, 2000, 4000, 8000]
REPETICIONES = 5
VALOR_MINIMO = -100
VALOR_MAXIMO = 100

CARPETA_GRAFICAS = Path(__file__).parent / "graficas"
COLOR_FUERZA_BRUTA = "#eb6834"
COLOR_DIVIDE_Y_VENCERAS = "#2a78d6"
COLOR_TEXTO = "#52514e"


def generar_datos(n: int, generador: random.Random) -> list[int]:
    """Genera una serie de n variaciones enteras entre -100 y 100.

    Args:
        n: cantidad de dias de la serie.
        generador: generador pseudoaleatorio con semilla fija.

    Returns:
        Lista de n enteros en el rango [VALOR_MINIMO, VALOR_MAXIMO].
    """
    return [generador.randint(VALOR_MINIMO, VALOR_MAXIMO) for _ in range(n)]


def cronometrar(
    algoritmo: Callable[[], tuple[int, int, float]], repeticiones: int
) -> tuple[float, float]:
    """Mide el tiempo de una llamada al algoritmo varias veces.

    Solo la llamada queda dentro de la ventana de perf_counter().

    Args:
        algoritmo: funcion sin argumentos que ejecuta el algoritmo.
        repeticiones: cuantas veces se repite la medicion.

    Returns:
        Una tupla (tiempo_minimo, suma) con el menor tiempo observado en
        segundos y la suma maxima que devolvio el algoritmo.
    """
    mejor_tiempo = float("inf")
    suma = 0.0
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = algoritmo()
        transcurrido = time.perf_counter() - inicio
        if transcurrido < mejor_tiempo:
            mejor_tiempo = transcurrido
        suma = resultado[2]
    return mejor_tiempo, suma


def medir() -> tuple[list[float], list[float]]:
    """Ejecuta el experimento para todos los tamanos de TAMANOS.

    Usa la misma lista para ambos algoritmos en cada tamano y verifica
    que ambos devuelvan la misma suma.

    Returns:
        Una tupla (tiempos_fuerza_bruta, tiempos_divide_y_venceras) en
        segundos, en el mismo orden que TAMANOS.
    """
    generador = random.Random(SEMILLA)
    tiempos_bruta: list[float] = []
    tiempos_dyv: list[float] = []

    print(f"{'n':>6} | {'fuerza bruta (s)':>16} | {'divide y v. (s)':>15}"
          f" | {'bruta/dyv':>9} | suma")
    print("-" * 66)
    for n in TAMANOS:
        valores = generar_datos(n, generador)
        tiempo_bruta, suma_bruta = cronometrar(
            lambda: subarreglo_fuerza_bruta(valores), REPETICIONES
        )
        tiempo_dyv, suma_dyv = cronometrar(
            lambda: subarreglo_maximo(valores, 0, len(valores) - 1),
            REPETICIONES,
        )
        assert suma_bruta == suma_dyv, (
            f"n={n}: fuerza bruta={suma_bruta}, divide y venceras={suma_dyv}"
        )
        tiempos_bruta.append(tiempo_bruta)
        tiempos_dyv.append(tiempo_dyv)
        print(f"{n:>6} | {tiempo_bruta:>16.6f} | {tiempo_dyv:>15.6f}"
              f" | {tiempo_bruta / tiempo_dyv:>9.2f} | {suma_bruta}")
    return tiempos_bruta, tiempos_dyv


def imprimir_factores(
    tiempos_bruta: list[float], tiempos_dyv: list[float]
) -> None:
    """Imprime cuanto se multiplica el tiempo cuando n se duplica.

    Args:
        tiempos_bruta: tiempos de la fuerza bruta, alineados con TAMANOS.
        tiempos_dyv: tiempos de divide y venceras, alineados con TAMANOS.
    """
    print("\nFactor de crecimiento al duplicar n:")
    for k in range(1, len(TAMANOS)):
        if TAMANOS[k] == 2 * TAMANOS[k - 1]:
            factor_bruta = tiempos_bruta[k] / tiempos_bruta[k - 1]
            factor_dyv = tiempos_dyv[k] / tiempos_dyv[k - 1]
            print(f"  {TAMANOS[k - 1]:>5} -> {TAMANOS[k]:>5}: "
                  f"fuerza bruta x{factor_bruta:.2f}, "
                  f"divide y venceras x{factor_dyv:.2f}")


def graficar(
    tiempos_bruta: list[float],
    tiempos_dyv: list[float],
    escala_log: bool,
    archivo: Path,
) -> None:
    """Dibuja tiempo vs. tamano de entrada para ambos algoritmos.

    Args:
        tiempos_bruta: tiempos de la fuerza bruta, alineados con TAMANOS.
        tiempos_dyv: tiempos de divide y venceras, alineados con TAMANOS.
        escala_log: si es True usa escala logaritmica en ambos ejes.
        archivo: ruta del PNG que se genera.
    """
    figura, ejes = plt.subplots(figsize=(9, 5.5), dpi=150)
    ejes.plot(TAMANOS, tiempos_bruta, marker="o", markersize=5,
              linewidth=2, color=COLOR_FUERZA_BRUTA,
              label="Fuerza bruta, Θ(n²)")
    ejes.plot(TAMANOS, tiempos_dyv, marker="s", markersize=5,
              linewidth=2, color=COLOR_DIVIDE_Y_VENCERAS,
              label="Divide y vencerás, Θ(n log n)")

    titulo = "Subarreglo máximo: tiempo de ejecución vs. tamaño de entrada"
    if escala_log:
        ejes.set_xscale("log")
        ejes.set_yscale("log")
        titulo += " (escala log-log)"
    ejes.set_title(titulo, fontsize=12)
    ejes.set_xlabel("Tamaño de entrada n (días)", color=COLOR_TEXTO)
    ejes.set_ylabel("Tiempo de ejecución (segundos)", color=COLOR_TEXTO)
    ejes.grid(True, which="major", color="#e4e3df", linewidth=0.8)
    ejes.spines[["top", "right"]].set_visible(False)
    ejes.legend(frameon=False)
    figura.tight_layout()
    figura.savefig(archivo)
    plt.close(figura)


def main() -> None:
    """Corre el experimento, imprime la tabla y guarda las graficas."""
    tiempos_bruta, tiempos_dyv = medir()
    imprimir_factores(tiempos_bruta, tiempos_dyv)

    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    graficar(tiempos_bruta, tiempos_dyv, False,
             CARPETA_GRAFICAS / "tiempo_vs_n.png")
    graficar(tiempos_bruta, tiempos_dyv, True,
             CARPETA_GRAFICAS / "tiempo_vs_n_log.png")
    print(f"\nGraficas guardadas en {CARPETA_GRAFICAS}")


if __name__ == "__main__":
    main()
