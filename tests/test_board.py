import unittest
from unittest.mock import patch
from core.board import Board
from core.ficha import Ficha

class TestBoard(unittest.TestCase):

    def test_get_board(self):
        board = Board()
        board.inicio()
        tablero_str = board.get_board()
        self.assertIsInstance(tablero_str, str)
        for n in range(0, 24):
            self.assertIn(str(n), tablero_str, f"numero {n} no está en la representación")

    def test_get_board_inicio(self):
        board = Board()
        board.inicio()
        tablero_str = board.get_board()
        self.assertIn("X5", tablero_str)
        self.assertIn("X3", tablero_str)
        self.assertIn("O2", tablero_str)
        self.assertIn("O5", tablero_str)
        self.assertIn("O3", tablero_str)

    def test_get_board_celdas_vacias(self):
        board = Board()
        board.inicio()
        board.get_celdas()[0] = []
        tablero_str = board.get_board()
        self.assertIn("--", tablero_str)

    def test_get_board_estructura(self):
        board = Board()
        board.inicio()
        tablero_str = board.get_board()
        lineas = tablero_str.split("\n")
        self.assertEqual(len(lineas[0]), len(lineas[-1]), "numeros no estan alineados")
        self.assertEqual(len(lineas[1]), len(lineas[-2]), "fichas no estan alineadas")
        self.assertIn("-" * 4, tablero_str, "falta barra del medio")

    def test_repr_celda(self):
        board = Board()
        ficha_x = Ficha("X")
        ficha_o = Ficha("O")
        self.assertEqual(board.repr_celda([]), "--")
        self.assertEqual(board.repr_celda([ficha_x, ficha_x]), "XX")
        self.assertEqual(board.repr_celda([ficha_o, ficha_o, ficha_o]), "OOO")

    def test_mover_destino_vacio(self):
        b = Board()
        c = b.get_celdas()
        c[:] = [[] for _ in range(24)]
        c[0] = [Ficha("X")]
        c[3] = []

        class V_Normal:
            @staticmethod
            def movimiento_valido(*args, **kwargs):
                return True

        with patch("core.board.Validaciones", V_Normal):
            b.mover(0, 3, "X")

        self.assertEqual(len(c[0]), 0)
        self.assertEqual(len(c[3]), 1)
        self.assertEqual(c[3][0].get_jugador(), "X")

    def test_mover_destino_fichas_propias(self):
        b = Board()
        c = b.get_celdas()
        c[:] = [[] for _ in range(24)]
        c[0] = [Ficha("X")]
        c[2] = [Ficha("X")]

        class V_Normal:
            @staticmethod
            def movimiento_valido(*args, **kwargs):
                return True

        with patch("core.board.Validaciones", V_Normal):
            b.mover(0, 2, "X")

        self.assertEqual(len(c[0]), 0)
        self.assertEqual(len(c[2]), 2)
        self.assertTrue(all(f.get_jugador() == "X" for f in c[2]))

    def test_mover_destino_capturar_enemigo(self):
        b = Board()
        c = b.get_celdas()
        c[:] = [[] for _ in range(24)]
        origen = 0
        destino = 2
        ficha_X = Ficha("X")
        ficha_O = Ficha("O")
        c[origen] = [ficha_X]
        c[destino] = [ficha_O]

        class V_Normal:
            @staticmethod
            def movimiento_valido(*args, **kwargs):
                return True

        with patch("core.board.Validaciones", V_Normal):
            with patch.object(Ficha, "set_capturada", autospec=True) as mock_setcap:
                b.mover(origen, destino - origen, "X")

        self.assertEqual(len(c[origen]), 0)
        self.assertEqual(len(c[destino]), 1)
        self.assertEqual(c[destino][0].get_jugador(), "X")
        caps = b.get_capturas()
        self.assertEqual(len(caps), 1)
        self.assertEqual(caps[0].get_jugador(), "O")

    def test_mover_sacar_ficha_tablero_permitido(self):
        b = Board()
        c = b.get_celdas()
        c[:] = [[] for _ in range(24)]
        c[20] = [Ficha("X")]

        class V_Returns_None_For_Exit:
            @staticmethod
            def movimiento_valido(*args, **kwargs):
                return None

        with patch("core.board.Validaciones", V_Returns_None_For_Exit):
            b.mover(20, 6, "X")

        self.assertEqual(len(c[20]), 0)

    def test_mover_sacar_ficha_tablero_no_permitido(self):
        b = Board()
        c = b.get_celdas()
        c[:] = [[] for _ in range(24)]
        c[21] = [Ficha("X")]

        class V_Prevent_Exit:
            @staticmethod
            def movimiento_valido(*args, **kwargs):
                return None
            @staticmethod
            def validar_reingreso(*args, **kwargs):
                return False

        with patch("core.board.Validaciones", V_Prevent_Exit):
            b.mover(21, 6, "X")

        self.assertEqual(len(c[21]), 0)
        self.assertEqual(b.get_capturas(), [])

    def test_reingreso_ficha(self):
        b = Board()
        c = b.get_celdas()
        c[:] = [[] for _ in range(24)]

        ficha_O = Ficha("O")
        ficha_O.set_capturada(True)
        b.get_capturas().append(ficha_O)

        b.mover(-1, 4, "O")

        self.assertEqual(len(b.get_capturas()), 0)
        self.assertEqual(len(c[20]), 1)
        self.assertEqual(c[20][0].get_jugador(), "O")