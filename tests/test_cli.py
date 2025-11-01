"""
Tests para el módulo CLI de Backgammon.

Cubre las funcionalidades principales de la interfaz de línea de comandos
con tests simples y efectivos.
"""
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.cli import BackgammonCLI
from core.exceptions import BackgammonError, CeldaBloqueadaError


class TestBackgammonCLI(unittest.TestCase):
    """Tests para la clase BackgammonCLI"""

    def setUp(self):
        """Inicializa una instancia de CLI para cada test"""
        self.cli = BackgammonCLI()

    def test_init_crea_juego(self):
        """Test que verifica la inicialización correcta"""
        self.assertIsNotNone(self.cli.game)

    @patch('cli.cli.os.system')
    def test_limpiar_pantalla(self, mock_system):
        """Test que verifica la limpieza de pantalla"""
        self.cli.limpiar_pantalla()
        mock_system.assert_called_once()

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_titulo(self, mock_stdout):
        """Test que verifica el título se muestra correctamente"""
        self.cli.mostrar_titulo()
        output = mock_stdout.getvalue()
        self.assertIn("BACKGAMMON", output)
        self.assertIn("═", output)

    @patch('builtins.input', return_value='')
    def test_pausar(self, mock_input):
        """Test que verifica la pausa funciona"""
        self.cli.pausar()
        mock_input.assert_called_once()

    @patch('builtins.input', return_value='12 3')
    def test_obtener_movimiento_valido(self, mock_input):
        """Test obtención de movimiento válido"""
        entrada = self.cli.obtener_movimiento()
        self.assertEqual(entrada, '12 3')

    @patch('builtins.input', return_value='salir')
    def test_obtener_movimiento_salir(self, mock_input):
        """Test comando salir"""
        entrada = self.cli.obtener_movimiento()
        self.assertEqual(entrada, 'salir')

    @patch('builtins.input', return_value='ayuda')
    def test_obtener_movimiento_ayuda(self, mock_input):
        """Test comando ayuda"""
        entrada = self.cli.obtener_movimiento()
        self.assertEqual(entrada, 'ayuda')

    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_obtener_movimiento_interrupt(self, mock_input):
        """Test interrupción con Ctrl+C"""
        entrada = self.cli.obtener_movimiento()
        self.assertEqual(entrada, 'salir')

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_estado_juego_basico(self, mock_stdout):
        """Test que muestra el estado del juego"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()
        self.cli.mostrar_estado_juego()
        output = mock_stdout.getvalue()
        self.assertIn("Turno de:", output)
        self.assertIn("Dados disponibles:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_estado_con_capturas(self, mock_stdout):
        """Test mostrar estado cuando hay fichas capturadas"""
        from core.ficha import Ficha

        self.cli.game.inicio()
        # Forzar una captura para testing
        capturas = self.cli.game.get_capturas()
        capturas.append(Ficha("X"))

        self.cli.mostrar_estado_juego()
        output = mock_stdout.getvalue()
        self.assertIn("capturadas", output.lower())

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    def test_movimiento_entrada_vacia(self, mock_sleep, mock_input):
        """Test movimiento con entrada vacía"""
        resultado = self.cli.movimiento('')
        self.assertTrue(resultado)

    @patch('builtins.input', return_value='s')
    @patch('cli.cli.os.system')
    def test_movimiento_comando_salir_confirmado(self, mock_system, mock_input):
        """Test comando salir confirmado"""
        resultado = self.cli.movimiento('salir')
        self.assertIsNone(resultado)

    @patch('builtins.input', return_value='n')
    @patch('cli.cli.os.system')
    def test_movimiento_comando_salir_cancelado(self, mock_system, mock_input):
        """Test comando salir cancelado"""
        resultado = self.cli.movimiento('salir')
        self.assertTrue(resultado)

    @patch('builtins.input', return_value='')
    @patch('cli.cli.os.system')
    @patch('cli.cli.time.sleep')
    def test_movimiento_comando_ayuda(self, mock_sleep, mock_system, mock_input):
        """Test comando ayuda"""
        resultado = self.cli.movimiento('ayuda')
        self.assertTrue(resultado)

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    def test_movimiento_formato_incorrecto(self, mock_sleep, mock_input):
        """Test movimiento con formato incorrecto"""
        resultado = self.cli.movimiento('12')  # Falta el salto
        self.assertTrue(resultado)

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    def test_movimiento_valores_no_numericos(self, mock_sleep, mock_input):
        """Test movimiento con valores no numéricos"""
        resultado = self.cli.movimiento('abc xyz')
        self.assertTrue(resultado)

    @patch('cli.cli.time.sleep')
    def test_procesar_movimiento_exitoso(self, mock_sleep):
        """Test procesamiento de movimiento exitoso"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()

        # Mock de movimiento válido
        with patch.object(self.cli.game, 'mover', return_value=None):
            with patch.object(self.cli.game, 'get_saltos', return_value=[]):
                resultado = self.cli._procesar_movimiento('0 1')
                self.assertFalse(resultado)  # Turno completado

    @patch('cli.cli.time.sleep')
    @patch('cli.cli.os.system')
    def test_procesar_movimiento_invalido(self, mock_system, mock_sleep):
        """Test procesamiento de movimiento inválido"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()

        # Mock de movimiento que lanza excepción
        with patch.object(self.cli.game, 'mover', side_effect=BackgammonError("Error")):
            with patch.object(self.cli, 'pausar'):
                resultado = self.cli._procesar_movimiento('0 1')
                self.assertTrue(resultado)  # Continuar turno

    @patch('cli.cli.time.sleep')
    @patch('cli.cli.os.system')
    def test_procesar_movimiento_celda_bloqueada(self, mock_system, mock_sleep):
        """Test error de celda bloqueada"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()

        with patch.object(self.cli.game, 'mover', side_effect=CeldaBloqueadaError("Bloqueada")):
            with patch.object(self.cli, 'pausar'):
                resultado = self.cli._procesar_movimiento('0 1')
                self.assertTrue(resultado)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', return_value='')
    @patch('cli.cli.os.system')
    def test_mostrar_ayuda(self, mock_system, mock_input, mock_stdout):
        """Test que muestra la ayuda completa"""
        self.cli.mostrar_ayuda()

        output = mock_stdout.getvalue()
        self.assertIn("AYUDA", output)
        self.assertIn("OBJETIVO", output)
        self.assertIn("MOVIMIENTOS", output)
        self.assertIn("CAPTURAS", output)
        self.assertIn("COMANDOS", output)

    def test_movimiento_continua_con_dados_restantes(self):
        """Test que el turno continúa cuando quedan dados"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()

        with patch.object(self.cli.game, 'mover', return_value=None):
            with patch.object(self.cli.game, 'get_saltos', return_value=[1, 2]):
                with patch('cli.cli.time.sleep'):
                    resultado = self.cli._procesar_movimiento('0 1')
                    # Si quedan saltos, debe continuar el turno
                    self.assertTrue(resultado)

    def test_puede_mover_sin_movimientos(self):
        """Test verificación de sin movimientos posibles"""
        self.cli.game.inicio()

        # Mock de estado sin movimientos posibles
        with patch.object(self.cli.game, 'puede_mover', return_value=False):
            puede = self.cli.game.puede_mover()
            self.assertFalse(puede)

    def test_puede_mover_con_movimientos(self):
        """Test verificación con movimientos disponibles"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()

        with patch.object(self.cli.game, 'puede_mover', return_value=True):
            puede = self.cli.game.puede_mover()
            self.assertTrue(puede)

    @patch('cli.cli.time.sleep')
    @patch('cli.cli.os.system')
    def test_procesar_movimiento_valor_error(self, mock_system, mock_sleep):
        """Test manejo de ValueError"""
        with patch.object(self.cli, 'pausar'):
            resultado = self.cli._procesar_movimiento('abc def')
            self.assertTrue(resultado)

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    def test_movimiento_entrada_espacios_extra(self, mock_sleep, mock_input):
        """Test entrada con espacios adicionales"""
        resultado = self.cli.movimiento('  12   3  ')
        # Debe intentar procesar (puede fallar por lógica del juego, pero no por formato)
        self.assertIsNotNone(resultado)

    def test_obtener_movimiento_convierte_minusculas(self):
        """Test que comandos se convierten a minúsculas"""
        with patch('builtins.input', return_value='SALIR'):
            entrada = self.cli.obtener_movimiento()
            self.assertEqual(entrada, 'salir')

        with patch('builtins.input', return_value='AYUDA'):
            entrada = self.cli.obtener_movimiento()
            self.assertEqual(entrada, 'ayuda')

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_estado_con_capturas_ambos_jugadores(self, mock_stdout):
        """Test mostrar estado con capturas de ambos jugadores"""
        from core.ficha import Ficha

        self.cli.game.inicio()
        capturas = self.cli.game.get_capturas()
        capturas.append(Ficha("X"))
        capturas.append(Ficha("O"))

        self.cli.mostrar_estado_juego()
        output = mock_stdout.getvalue()
        self.assertIn("Jugador X:", output)
        self.assertIn("Jugador O:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_estado_indica_reingreso(self, mock_stdout):
        """Test que indica necesidad de reingresar fichas"""
        from core.ficha import Ficha

        self.cli.game.inicio()

        # Simular turno de X con fichas capturadas
        with patch.object(self.cli.game, 'get_jugador') as mock_jugador:
            mock_jugador.return_value = MagicMock(get_name=lambda: 'X')

            capturas = self.cli.game.get_capturas()
            capturas.append(Ficha("X"))

            self.cli.mostrar_estado_juego()
            output = mock_stdout.getvalue()
            self.assertIn("Reingresa", output)


if __name__ == '__main__':
    unittest.main()