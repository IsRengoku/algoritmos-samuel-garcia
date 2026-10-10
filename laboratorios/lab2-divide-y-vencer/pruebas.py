import random

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo, suma_cruzada


def ambas(valores):
    """Ejecuta ambos algoritmos y verifica que no modifican la lista."""
    copia = list(valores)
    bruta = subarreglo_fuerza_bruta(valores)
    assert valores == copia, "la fuerza bruta modifico la lista"
    dyv = subarreglo_maximo(valores, 0, len(valores) - 1)
    assert valores == copia, "divide y venceras modifico la lista"
    return bruta, dyv


def suma_tramo(valores, tramo):
    """Recalcula la suma de un tramo (inicio, fin, suma) desde sus indices."""
    inicio, fin, _ = tramo
    return sum(valores[inicio:fin + 1])


# Serie de ocho dias de la situacion problema: dias 2 a 7, suma 17.
serie = [-3, 5, -2, 8, -6, 3, 9, -4]
bruta, dyv = ambas(serie)
assert bruta[2] == 17
assert dyv[2] == 17
assert suma_tramo(serie, bruta) == 17
assert suma_tramo(serie, dyv) == 17

# Un solo elemento (positivo y negativo).
for unico in ([7], [-7], [0]):
    bruta, dyv = ambas(unico)
    assert bruta[2] == unico[0]
    assert dyv[2] == unico[0]

# Todos negativos: la mejor racha es el mayor valor individual.
negativos = [-8, -3, -6, -2, -5, -4]
bruta, dyv = ambas(negativos)
assert bruta[2] == -2
assert dyv[2] == -2

# Todos positivos: la mejor racha es la serie completa.
positivos = [4, 1, 7, 3, 2, 9]
bruta, dyv = ambas(positivos)
assert bruta[2] == sum(positivos)
assert dyv[2] == sum(positivos)

# El mejor tramo cruza el punto medio (medio = 2): indices 1..4, suma 16.
# Ninguna mitad por si sola alcanza 16 (izquierda 8, derecha 8).
cruce = [-8, 1, 7, 6, 2, -9]
medio = (len(cruce) - 1) // 2
bruta, dyv = ambas(cruce)
assert bruta[2] == 16
assert dyv[2] == 16
assert suma_cruzada(cruce, 0, medio, len(cruce) - 1)[2] == 16
assert subarreglo_maximo(cruce, 0, medio)[2] == 8
assert subarreglo_maximo(cruce, medio + 1, len(cruce) - 1)[2] == 8

# Lista vacia: ambas funciones deben rechazarla con ValueError.
for llamada in (
    lambda: subarreglo_fuerza_bruta([]),
    lambda: subarreglo_maximo([], 0, -1),
):
    try:
        llamada()
    except ValueError:
        pass
    else:
        raise AssertionError("una lista vacia debe lanzar ValueError")

# Listas aleatorias: ambas funciones deben dar la misma suma.
generador = random.Random(2026)
for _ in range(30):
    n = generador.randint(1, 60)
    valores = [generador.randint(-100, 100) for _ in range(n)]
    bruta, dyv = ambas(valores)
    assert bruta[2] == dyv[2], (valores, bruta, dyv)
    assert suma_tramo(valores, bruta) == bruta[2]
    assert suma_tramo(valores, dyv) == dyv[2]

print("Todas las pruebas pasaron.")
