"""Pruebas del contrato público de merge sort."""
import unittest
from itertools import permutations

from algoritmos import merge_sort


class PruebasMergeSort(unittest.TestCase):
    """Pruebas de orden, conteo y no mutación de merge_sort."""

    def test_copia_orden_y_comparaciones(self) -> None:
        """Verifica orden descendente, conteo y que la entrada no cambie."""
        casos = [
            ([], [], 0), ([7], [7], 0), ([1, 2], [2, 1], 1),
            ([2, 1], [2, 1], 1), ([1, 3, 2], [3, 2, 1], 3),
            ([4, 3, 2, 1], [4, 3, 2, 1], 4),
            ([2, 2, 1], [2, 2, 1], 2),
            ([-1, 0, -2], [0, -1, -2], 3),
        ]
        for entrada, esperado, cuenta in casos:
            with self.subTest(entrada=entrada):
                original = entrada.copy()
                salida, comparaciones = merge_sort(entrada)
                self.assertEqual(salida, esperado)
                self.assertEqual(comparaciones, cuenta)
                self.assertEqual(entrada, original)
                self.assertIsNot(salida, entrada)

    def test_todas_las_permutaciones_pequenas(self) -> None:
        """Verifica el orden para todas las permutaciones con n < 7."""
        for n in range(7):
            for permutacion in permutations(range(n)):
                entrada = list(permutacion)
                salida, cuenta = merge_sort(entrada)
                self.assertEqual(salida, list(range(n - 1, -1, -1)))
                self.assertEqual(entrada, list(permutacion))
                self.assertGreaterEqual(cuenta, 0)


if __name__ == '__main__':
    unittest.main()
