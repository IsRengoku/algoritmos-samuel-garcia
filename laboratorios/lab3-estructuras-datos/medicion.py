"""Experimentos: busqueda en lista enlazada vs. tabla hash y efecto de alfa."""

import random
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from estructuras import ListaEnlazada, TablaHash  # noqa: E402

SEMILLA = 2026
TAMANOS = [100, 500, 1000, 5000, 10000, 20000, 50000]
N_FIJO = 20000
ALFAS = [0.25, 0.5, 1, 2, 4, 6, 8, 10]
BUSQUEDAS = 200
MUESTRA_VERIFICACION = 200
REPETICIONES = 5
VUELTAS_TABLA = 50
ESTADOS = ["en bodega", "en reparto", "entregado", "devuelto"]

CARPETA_GRAFICAS = Path(__file__).parent / "graficas"
COLOR_LISTA = "#eb6834"
COLOR_TABLA = "#2a78d6"
COLOR_TEXTO = "#52514e"


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def generar_envios(n: int, semilla: int) -> list[tuple[int, str]]:
    """Genera n envios con guias distintas de diez digitos.

    Args:
        n: cantidad de envios.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Lista de n tuplas (guia, estado) con guias sin repetir.
    """
    azar = random.Random(semilla)
    guias = azar.sample(range(10**9, 10**10), n)
    return [(guia, azar.choice(ESTADOS)) for guia in guias]


def es_primo(numero: int) -> bool:
    """Indica si un entero es primo, por division de prueba.

    Args:
        numero: entero a evaluar.

    Returns:
        True si numero es primo.
    """
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def primo_cercano(objetivo: float) -> int:
    """Busca el primo mas cercano a un valor, alejandose hacia ambos lados.

    Args:
        objetivo: valor alrededor del cual se busca el primo.

    Returns:
        El primo mas cercano a objetivo (el menor si hay empate).
    """
    centro = max(2, round(objetivo))
    distancia = 0
    while True:
        if es_primo(centro - distancia):
            return centro - distancia
        if es_primo(centro + distancia):
            return centro + distancia
        distancia += 1


def construir(
    envios: list[tuple[int, str]], m: int
) -> tuple[ListaEnlazada, TablaHash]:
    """Carga los mismos envios en una lista enlazada y en una tabla hash.

    Args:
        envios: tuplas (guia, estado) a insertar.
        m: numero de casillas de la tabla.

    Returns:
        Una tupla (lista, tabla) con los envios cargados.
    """
    lista = ListaEnlazada()
    tabla = TablaHash(m)
    for guia, estado in envios:
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)
    return lista, tabla


def verificar(
    lista: ListaEnlazada,
    tabla: TablaHash,
    envios: list[tuple[int, str]],
    inexistentes: list[int],
) -> None:
    """Comprueba que lista y tabla responden lo mismo antes de medir.

    Usa una muestra de guias existentes y todas las inexistentes.

    Args:
        lista: lista enlazada cargada con envios.
        tabla: tabla hash cargada con los mismos envios.
        envios: tuplas (guia, estado) cargadas en ambas estructuras.
        inexistentes: guias que no estan en la coleccion.
    """
    azar = random.Random(SEMILLA)
    muestra = azar.sample(envios, min(MUESTRA_VERIFICACION, len(envios)))
    for guia, estado in muestra:
        assert lista.buscar(guia) == tabla.buscar(guia) == estado, guia
    for guia in inexistentes:
        assert lista.buscar(guia) is None, guia
        assert tabla.buscar(guia) is None, guia


def tiempo_medio_busqueda(
    estructura: ListaEnlazada | TablaHash, guias: list[int], vueltas: int = 1
) -> float:
    """Mide el tiempo medio de una busqueda sobre una lista de guias.

    Solo las busquedas quedan dentro de la ventana de perf_counter(). Se
    repite REPETICIONES veces y se conserva la menor, que es la menos
    afectada por interrupciones del sistema operativo.

    Args:
        estructura: lista enlazada o tabla hash ya construida.
        guias: guias a buscar.
        vueltas: cuantas veces se recorre guias dentro de cada ventana;
            sirve para que las busquedas rapidas superen el ruido del reloj.

    Returns:
        El tiempo medio por busqueda en segundos.
    """
    mejor = float("inf")
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        for _ in range(vueltas):
            for guia in guias:
                estructura.buscar(guia)
        transcurrido = time.perf_counter() - inicio
        mejor = min(mejor, transcurrido)
    return mejor / (len(guias) * vueltas)


def cadena_mas_larga(tabla: TablaHash) -> int:
    """Devuelve la longitud de la casilla con mas guias.

    Args:
        tabla: tabla hash ya construida.

    Returns:
        El tamano de la lista mas larga entre todas las casillas.
    """
    return max(casilla.tamano for casilla in tabla.casillas)


def experimento_a() -> tuple[list[float], list[float]]:
    """Mide lista vs. tabla para cada n de TAMANOS con alfa cercano a 2.

    Returns:
        Una tupla (tiempos_lista, tiempos_tabla) en segundos por busqueda,
        alineados con TAMANOS.
    """
    tiempos_lista: list[float] = []
    tiempos_tabla: list[float] = []

    print("Experimento A: busquedas infructuosas, lista vs. tabla")
    print(f"{'n':>6} | {'m':>6} | {'alfa':>5} | {'lista (us)':>11}"
          f" | {'tabla (us)':>10} | {'lista/tabla':>11} | cadena max")
    print("-" * 79)
    for n in TAMANOS:
        envios = generar_envios(n, SEMILLA + n)
        m = primo_cercano(n / 2)
        lista, tabla = construir(envios, m)
        inexistentes = generar_guias_inexistentes(
            {guia for guia, _ in envios}, BUSQUEDAS
        )
        verificar(lista, tabla, envios, inexistentes)

        tiempo_lista = tiempo_medio_busqueda(lista, inexistentes)
        tiempo_tabla = tiempo_medio_busqueda(
            tabla, inexistentes, VUELTAS_TABLA
        )
        tiempos_lista.append(tiempo_lista)
        tiempos_tabla.append(tiempo_tabla)
        print(f"{n:>6} | {m:>6} | {tabla.factor_carga():>5.2f}"
              f" | {tiempo_lista * 1e6:>11.2f}"
              f" | {tiempo_tabla * 1e6:>10.3f}"
              f" | {tiempo_lista / tiempo_tabla:>11.1f}"
              f" | {cadena_mas_larga(tabla)}")
    return tiempos_lista, tiempos_tabla


def experimento_b() -> tuple[list[float], list[float]]:
    """Mide la tabla con N_FIJO guias para distintos factores de carga.

    Returns:
        Una tupla (alfas_reales, tiempos_tabla): el factor de carga
        obtenido con cada m primo y el tiempo medio por busqueda en
        segundos.
    """
    envios = generar_envios(N_FIJO, SEMILLA + N_FIJO)
    inexistentes = generar_guias_inexistentes(
        {guia for guia, _ in envios}, BUSQUEDAS
    )
    alfas_reales: list[float] = []
    tiempos_tabla: list[float] = []

    print(f"\nExperimento B: tabla con n = {N_FIJO}, variando alfa")
    print(f"{'alfa obj.':>9} | {'m':>6} | {'alfa':>6} | {'tabla (us)':>10}"
          f" | cadena max")
    print("-" * 52)
    for alfa in ALFAS:
        m = primo_cercano(N_FIJO / alfa)
        tabla = TablaHash(m)
        for guia, estado in envios:
            tabla.insertar(guia, estado)
        muestra = random.Random(SEMILLA).sample(envios, MUESTRA_VERIFICACION)
        for guia, estado in muestra:
            assert tabla.buscar(guia) == estado, guia
        for guia in inexistentes:
            assert tabla.buscar(guia) is None, guia

        tiempo = tiempo_medio_busqueda(tabla, inexistentes, VUELTAS_TABLA)
        alfas_reales.append(tabla.factor_carga())
        tiempos_tabla.append(tiempo)
        print(f"{alfa:>9} | {m:>6} | {tabla.factor_carga():>6.2f}"
              f" | {tiempo * 1e6:>10.3f} | {cadena_mas_larga(tabla)}")
    return alfas_reales, tiempos_tabla


def estilizar(ejes: plt.Axes, titulo: str, etiqueta_x: str) -> None:
    """Aplica titulo, etiquetas, rejilla y bordes comunes a una grafica.

    Args:
        ejes: ejes de matplotlib a estilizar.
        titulo: titulo de la grafica.
        etiqueta_x: texto del eje horizontal, con sus unidades.
    """
    ejes.set_title(titulo, fontsize=12)
    ejes.set_xlabel(etiqueta_x, color=COLOR_TEXTO)
    ejes.set_ylabel("Tiempo medio por búsqueda (microsegundos)",
                    color=COLOR_TEXTO)
    ejes.grid(True, which="major", color="#e4e3df", linewidth=0.8)
    ejes.spines[["top", "right"]].set_visible(False)


def graficar_lista_vs_tabla(
    tiempos_lista: list[float],
    tiempos_tabla: list[float],
    escala_log: bool,
    archivo: Path,
) -> None:
    """Dibuja tiempo medio por busqueda vs. n para ambas estructuras.

    Args:
        tiempos_lista: tiempos de la lista, alineados con TAMANOS.
        tiempos_tabla: tiempos de la tabla, alineados con TAMANOS.
        escala_log: si es True usa escala logaritmica en ambos ejes.
        archivo: ruta del PNG que se genera.
    """
    figura, ejes = plt.subplots(figsize=(9, 5.5), dpi=150)
    ejes.plot(TAMANOS, [t * 1e6 for t in tiempos_lista], marker="o",
              markersize=5, linewidth=2, color=COLOR_LISTA,
              label="Lista enlazada")
    ejes.plot(TAMANOS, [t * 1e6 for t in tiempos_tabla], marker="s",
              markersize=5, linewidth=2, color=COLOR_TABLA,
              label="Tabla hash (α ≈ 2)")

    titulo = "Búsqueda de guías inexistentes: lista enlazada vs. tabla hash"
    if escala_log:
        ejes.set_xscale("log")
        ejes.set_yscale("log")
        titulo += " (log-log)"
    estilizar(ejes, titulo, "Número de guías n")
    ejes.legend(frameon=False)
    figura.tight_layout()
    figura.savefig(archivo)
    plt.close(figura)


def graficar_tiempo_vs_alfa(
    alfas: list[float], tiempos: list[float], archivo: Path
) -> None:
    """Dibuja tiempo medio por busqueda vs. factor de carga.

    Args:
        alfas: factores de carga medidos.
        tiempos: tiempos de la tabla en segundos, alineados con alfas.
        archivo: ruta del PNG que se genera.
    """
    figura, ejes = plt.subplots(figsize=(9, 5.5), dpi=150)
    ejes.plot(alfas, [t * 1e6 for t in tiempos], marker="s", markersize=5,
              linewidth=2, color=COLOR_TABLA)
    estilizar(
        ejes,
        f"Tabla hash con n = {N_FIJO} guías: tiempo de búsqueda "
        "infructuosa vs. factor de carga",
        "Factor de carga α = n / m (guías por casilla)",
    )
    ejes.set_ylim(bottom=0)
    ejes.set_xlim(left=0)
    figura.tight_layout()
    figura.savefig(archivo)
    plt.close(figura)


def main() -> None:
    """Corre ambos experimentos, imprime las tablas y guarda las graficas."""
    tiempos_lista, tiempos_tabla = experimento_a()
    alfas, tiempos_alfa = experimento_b()

    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    graficar_lista_vs_tabla(tiempos_lista, tiempos_tabla, False,
                            CARPETA_GRAFICAS / "lista_vs_tabla.png")
    graficar_lista_vs_tabla(tiempos_lista, tiempos_tabla, True,
                            CARPETA_GRAFICAS / "lista_vs_tabla_log.png")
    graficar_tiempo_vs_alfa(alfas, tiempos_alfa,
                            CARPETA_GRAFICAS / "tiempo_vs_alfa.png")
    print(f"\nGraficas guardadas en {CARPETA_GRAFICAS}")


if __name__ == "__main__":
    main()
