"""Algoritmos de ordenamiento instrumentados para el Laboratorio 1."""


def insertion_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de insercion.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    resultado = datos.copy()
    comparaciones = 0
    for i in range(1, len(resultado)):
        actual = resultado[i]
        j = i - 1
        while j >= 0:
            # Cuenta también la comparación falsa que termina la búsqueda.
            comparaciones += 1
            if resultado[j] < actual:
                resultado[j + 1] = resultado[j]
                j -= 1
            else:
                break
        resultado[j + 1] = actual
    return resultado, comparaciones


def merge_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de mezcla.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    resultado = datos.copy()
    if len(resultado) <= 1:
        return resultado, 0

    medio = len(resultado) // 2
    izquierda, cuenta_izquierda = merge_sort(resultado[:medio])
    derecha, cuenta_derecha = merge_sort(resultado[medio:])
    comparaciones = cuenta_izquierda + cuenta_derecha
    mezcla = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        comparaciones += 1
        # Priorizar la izquierda en los empates conserva la estabilidad.
        if izquierda[i] >= derecha[j]:
            mezcla.append(izquierda[i])
            i += 1
        else:
            mezcla.append(derecha[j])
            j += 1
    mezcla.extend(izquierda[i:])
    mezcla.extend(derecha[j:])
    return mezcla, comparaciones
