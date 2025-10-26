import unittest
from core import validaciones
from core.ficha import Ficha
from core.exceptions import *


def crear_celdas_vacias():
    return [[] for _ in range(24)]


class TestValidaciones(unittest.TestCase):

    def test_movimiento_valido_X_ok(self):
        celdas = crear_celdas_vacias()
        celdas[0] = [Ficha("X")]
        capturas = []
        destino = validaciones.Validaciones.movimiento_valido(
            celdas, capturas, 0, 3, "X"
        )
        self.assertTrue(destino)

    def test_movimiento_valido_O_ok(self):
        celdas = crear_celdas_vacias()
        celdas[5] = [Ficha("O")]
        capturas = []
        destino = validaciones.Validaciones.movimiento_valido(
            celdas, capturas, 5, 2, "O"
        )
        self.assertTrue(destino)

    def test_movimiento_valido_destino_fuera_raises_salida_invalida(self):
        celdas = crear_celdas_vacias()
        celdas[22] = [Ficha("X")]
        celdas[10] = [Ficha("X")]
        capturas = []
        with self.assertRaises(SalidaInvalidaError):
            validaciones.Validaciones.movimiento_valido(
                celdas, capturas, 22, 3, "X"
            )

    def test_validar_salida_raises_si_tiene_capturas(self):
        celdas = crear_celdas_vacias()
        capturas = [Ficha("X")]
        with self.assertRaises(FichasCapturadasError):
            validaciones.Validaciones.validar_salida(
                celdas, capturas, 22, 2, "X"
            )

    def test_validar_salida_raises_si_fichas_fuera_home(self):
        celdas = crear_celdas_vacias()
        celdas[10] = [Ficha("X")]
        capturas = []
        with self.assertRaises(SalidaInvalidaError):
            validaciones.Validaciones.validar_salida(
                celdas, capturas, 22, 2, "X"
            )

    def test_validar_salida_true_X(self):
        celdas = crear_celdas_vacias()
        celdas[18] = [Ficha("X")]
        capturas = []
        self.assertTrue(
            validaciones.Validaciones.validar_salida(celdas, capturas, 18, 1, "X")
        )

    def test_validar_salida_true_O(self):
        celdas = crear_celdas_vacias()
        celdas[5] = [Ficha("O")]
        capturas = []
        self.assertTrue(
            validaciones.Validaciones.validar_salida(celdas, capturas, 5, 1, "O")
        )

    def test_validar_victoria_true(self):
        celdas = crear_celdas_vacias()
        capturas = []
        self.assertTrue(validaciones.Validaciones.validar_victoria(celdas, capturas, "X"))

    def test_validar_victoria_false_por_tablero_y_capturas(self):
        celdas = crear_celdas_vacias()
        celdas[0] = [Ficha("X")]
        capturas = []
        self.assertFalse(validaciones.Validaciones.validar_victoria(celdas, capturas, "X"))

        celdas = crear_celdas_vacias()
        capturas = [Ficha("X")]
        self.assertFalse(validaciones.Validaciones.validar_victoria(celdas, capturas, "X"))

    def test_puede_mover_true(self):
        celdas = crear_celdas_vacias()
        celdas[0] = [Ficha("X")]
        capturas = []
        saltos = [1, 2, 3]
        self.assertTrue(validaciones.Validaciones.puede_mover(celdas, capturas, saltos, "X"))

    def test_puede_mover_false_no_saltos(self):
        celdas = crear_celdas_vacias()
        celdas[0] = [Ficha("X")]
        capturas = []
        saltos = []
        self.assertFalse(validaciones.Validaciones.puede_mover(celdas, capturas, saltos, "X"))

    def test_puede_mover_false_no_movimientos_validos(self):
        celdas = crear_celdas_vacias()
        celdas[1] = [Ficha("O"), Ficha("O")] 
        celdas[0] = [Ficha("X")]
        capturas = []
        saltos = [1, 1]
        self.assertFalse(validaciones.Validaciones.puede_mover(celdas, capturas, saltos, "X"))

    def test_puede_mover_false_capturas_sin_reingreso(self):
        celdas = crear_celdas_vacias()
        celdas[0] = [Ficha("O"), Ficha("O")]
        capturas = [Ficha("X")]
        saltos = [1]
        self.assertFalse(validaciones.Validaciones.puede_mover(celdas, capturas, saltos, "X"))