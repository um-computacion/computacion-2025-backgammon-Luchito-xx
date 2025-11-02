import unittest
from core.ficha import Ficha

class TestFicha(unittest.TestCase):

    def test_crear_ficha(self):
        ficha = Ficha("Lucho")
        self.assertEqual(ficha.get_jugador(), "Lucho")
        self.assertFalse(ficha.is_capturada())

    def test_set_jugador(self):
        ficha = Ficha("X")
        ficha.set_jugador("O")
        self.assertEqual(ficha.get_jugador(), "O")

    def test_set_capturada(self):
        ficha = Ficha("X")
        ficha.set_capturada(True)
        self.assertTrue(ficha.is_capturada())
        ficha.set_capturada(False)
        self.assertFalse(ficha.is_capturada())

    def test_repr_estado_libre_and_capturada(self):
        ficha = Ficha("X")
        rlibre = repr(ficha)
        self.assertIn("Ficha", rlibre)
        self.assertIn("jugador", rlibre)

        ficha.set_capturada(True)
        rcapt = repr(ficha)
        self.assertIn("Ficha", rcapt)
        self.assertIn("jugador", rcapt)
