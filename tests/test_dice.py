import unittest
from unittest.mock import patch
from core.dice import Dice

class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    def test_creacion_dice(self):
        vals = self.dice.get_valor()
        self.assertIsInstance(vals, list)
        self.assertTrue(all(isinstance(v, int) for v in vals))
        self.assertEqual(len(vals), 2)

    def test_roll_resultados_validos(self):
        valores = self.dice.roll()
        self.assertTrue(all(1 <= valor <= 6 for valor in valores))

    def test_roll_dobles(self):
        # random.randint dentro de core.dice para simular dobles 3,3
        with patch("core.dice.random.randint", side_effect=[3, 3]):
            d = Dice()
            valores = d.roll()
            # si la implementación convierte dobles en 4 valores iguales
            self.assertIn(len(valores), (2, 4))
            if len(valores) == 4:
                self.assertTrue(all(valor == valores[0] for valor in valores))
            else:
                # si la implementación no expande a 4, al menos ambos deben ser iguales
                self.assertEqual(valores[0], valores[1])

    def test_str_output(self):
        salida = str(self.dice)
        self.assertIn("Dado", salida)  
        self.assertIsInstance(salida, str)