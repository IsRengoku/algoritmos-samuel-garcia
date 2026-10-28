import random

from estructuras import ListaEnlazada, TablaHash


def longitud_casilla(tabla, indice):
    """Cuenta los nodos de una casilla recorriendo su cadena."""
    cuenta = 0
    actual = tabla.casillas[indice].cabeza
    while actual is not None:
        cuenta += 1
        actual = actual.siguiente
    return cuenta


# Serie de ejemplo de la situacion problema.
serie = [
    (1000000010, "en bodega"),
    (1000000024, "en reparto"),
    (1000000017, "en bodega"),
    (1000000005, "entregado"),
]
lista = ListaEnlazada()
tabla = TablaHash(7)
for guia, estado in serie:
    lista.insertar(guia, estado)
    tabla.insertar(guia, estado)

# Busqueda exitosa e infructuosa en ambas estructuras.
assert lista.buscar(1000000024) == "en reparto"
assert tabla.buscar(1000000024) == "en reparto"
assert lista.buscar(1000000005) == "entregado"
assert tabla.buscar(1000000005) == "entregado"
assert lista.buscar(1000000099) is None
assert tabla.buscar(1000000099) is None
assert lista.tamano == 4
assert tabla.tamano == 4

# Estructuras vacias: toda busqueda es infructuosa.
assert ListaEnlazada().buscar(10) is None
assert TablaHash(7).buscar(10) is None
assert TablaHash(7).factor_carga() == 0

# Una tabla sin casillas o con m negativo se rechaza al crearla.
for m_invalido in (0, -7):
    try:
        TablaHash(m_invalido)
    except ValueError:
        pass
    else:
        raise AssertionError(f"TablaHash({m_invalido}) no lanzo ValueError")

# La insercion al inicio deja la ultima guia como cabeza.
assert lista.cabeza.guia == 1000000005

# Colision forzada: con m = 7, las guias 10, 24 y 17 caen en la casilla 3.
tabla = TablaHash(7)
for guia in (10, 24, 17):
    assert tabla.hash(guia) == 3
    tabla.insertar(guia, "en bodega")

assert tabla.buscar(10) == "en bodega"
assert tabla.buscar(24) == "en bodega"
assert tabla.buscar(17) == "en bodega"
assert tabla.buscar(3) is None  # misma casilla, guia inexistente
assert tabla.buscar(99) is None
assert tabla.casillas[3].tamano == 3
assert longitud_casilla(tabla, 3) == 3
for indice in range(7):
    if indice != 3:
        assert tabla.casillas[indice].tamano == 0

# Factor de carga tras las tres inserciones.
assert tabla.factor_carga() == 3 / 7

# Colecciones aleatorias: lista y tabla responden lo mismo.
random.seed(2026)
for _ in range(30):
    n = random.randint(1, 500)
    m = random.choice([1, 2, 7, 97, 101, 1009])
    guias = random.sample(range(1000000000, 10000000000), n)
    estados = ["en bodega", "en reparto", "entregado", "devuelto"]
    lista = ListaEnlazada()
    tabla = TablaHash(m)
    esperado = {}
    for guia in guias:
        estado = random.choice(estados)
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)
        esperado[guia] = estado

    assert lista.tamano == n
    assert tabla.tamano == n
    assert tabla.factor_carga() == n / m
    assert sum(casilla.tamano for casilla in tabla.casillas) == n

    # Guias existentes.
    for guia in guias:
        assert lista.buscar(guia) == tabla.buscar(guia) == esperado[guia]

    # Guias inexistentes.
    existentes = set(guias)
    inexistentes = 0
    while inexistentes < 50:
        guia = random.randint(1000000000, 9999999999)
        if guia in existentes:
            continue
        assert lista.buscar(guia) is None
        assert tabla.buscar(guia) is None
        inexistentes += 1

print("Todas las pruebas pasaron.")
