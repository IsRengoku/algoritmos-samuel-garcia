"""Pruebas públicas del ordenamiento y los generadores."""
import random
import unittest

from algoritmos import insertion_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso


class PruebasParte3(unittest.TestCase):
    """Pruebas de insertion_sort y de los generadores de escenarios."""

    def test_orden_copia_y_comparaciones(self) -> None:
        """Verifica orden descendente, conteo y que la entrada no cambie."""
        for entrada, esperado, comparaciones in [
            ([], [], 0), ([7], [7], 0), ([3, 2, 1], [3, 2, 1], 2),
            ([1, 2, 3], [3, 2, 1], 3), ([1, 3, 2], [3, 2, 1], 3),
            ([2, 2, 1], [2, 2, 1], 2),
        ]:
            with self.subTest(entrada=entrada):
                original = entrada.copy()
                salida, cuenta = insertion_sort(entrada)
                self.assertEqual(salida, esperado)
                self.assertEqual(cuenta, comparaciones)
                self.assertEqual(entrada, original)
                self.assertIsNot(salida, entrada)

    def test_generadores_y_extremos(self) -> None:
        """Verifica tamaño, valores y forma de los lotes A, B y C."""
        generadores = (
            generar_aleatorio, generar_casi_ordenado, generar_inverso,
        )
        for n in (0, 1, 2, 100, 6400):
            for generar in generadores:
                with self.subTest(n=n, generador=generar.__name__):
                    datos = generar(n)
                    self.assertEqual(len(datos), n)
                    self.assertEqual(set(datos), set(range(1, n + 1)))
            inverso = generar_inverso(n)
            self.assertEqual(inverso, list(range(1, n + 1)))
            casi = generar_casi_ordenado(n)
            corte = 98 * n // 100
            self.assertTrue(
                all(casi[i] > casi[i + 1] for i in range(corte - 1))
            )

    def test_semillas_reproducibles_sin_estado_global(self) -> None:
        """Verifica que la semilla reproduzca el lote sin tocar random."""
        for generar in (generar_aleatorio, generar_casi_ordenado):
            estado = random.getstate()
            self.assertEqual(generar(100, 7), generar(100, 7))
            self.assertNotEqual(generar(100, 7), generar(100, 8))
            self.assertEqual(random.getstate(), estado)

    def test_formulas_mejor_y_peor(self) -> None:
        """Verifica n-1 comparaciones en el mejor caso y n(n-1)/2 en C."""
        for n in (0, 1, 2, 10, 100):
            _, mejor = insertion_sort(list(range(n, 0, -1)))
            _, peor = insertion_sort(generar_inverso(n))
            self.assertEqual(mejor, max(0, n - 1))
            self.assertEqual(peor, n * (n - 1) // 2)


if __name__ == '__main__':
    unittest.main()
