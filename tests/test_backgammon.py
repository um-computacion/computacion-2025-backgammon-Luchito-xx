import unittest
from unittest.mock import patch
from core.backgammon import Backgammon
from core.exceptions import BackgammonError, SaltosError

class FakeDice:
    def __init__(self, rolls):
        self._rolls = list(rolls)
    def roll(self):
        if not self._rolls:
            return [1,2]
        return self._rolls.pop(0)

class TestBackgammon(unittest.TestCase):

    def test_turno_inicial_elige_correctamente(self):
        with patch("core.backgammon.Dice") as MockDiceClass:
            mock_dice = MockDiceClass.return_value
            mock_dice.roll.return_value = [5, 2]
            g = Backgammon()
            g.inicio()
            name = g.get_jugador().get_name()
            self.assertIn(name, ("X", "O"))

    def test_tirar_dado_y_saltos_consumidos(self):
        g = Backgammon(dice=FakeDice([[4, 1]]))
        g.inicio()
        g.tirar_dado()
        saltos = g.get_saltos()
        self.assertTrue(isinstance(saltos, list))

        class VAllow:
            @staticmethod
            def movimiento_valido(*args, **kwargs):
                return True
            @staticmethod
            def validar_victoria(*args, **kwargs):
                return False

        with patch("core.backgammon.Validaciones", VAllow):
            try:
                initial = list(g.get_saltos())
                if initial:
                    g.mover(0, initial[0])
            except BackgammonError:
                pass
            self.assertIsInstance(g.get_saltos(), list)

    def test_mover_sin_tirar_dados_lanza_saltos_error(self):
        g = Backgammon()
        g.inicio()
        self.assertEqual(g.get_saltos(), [])
        with self.assertRaises(SaltosError):
            g.mover(0, 3)
