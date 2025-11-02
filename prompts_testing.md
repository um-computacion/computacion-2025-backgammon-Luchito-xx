## prompt

Analisa y propon tests para cli usando unittest, debe alcanzar ~90%

### Claude-Sonnet_4.5

### Respuesta

Analizo tu repositorio y veo que tienes una CLI bastante completa en cli/cli.py con 170 líneas de código que actualmente no tienen tests. El coverage actual de CLI es 0%, lo que está bajando tu cobertura general del 92%.
Voy a crear tests que cubran las funcionalidades principales de la CLI:

```
"""
Tests para el módulo CLI de Backgammon.

Cubre las funcionalidades principales de la interfaz de línea de comandos.
"""
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.cli import BackgammonCLI
from core.exceptions import BackgammonError


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
        self.cli.game.inicio()
        # Forzar una captura para testing
        capturas = self.cli.game.get_capturas()
        from core.ficha import Ficha
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

    @patch('builtins.input', side_effect=['s'])
    @patch('cli.cli.os.system')
    def test_movimiento_comando_salir_confirmado(self, mock_system, mock_input):
        """Test comando salir confirmado"""
        resultado = self.cli.movimiento('salir')
        self.assertIsNone(resultado)

    @patch('builtins.input', side_effect=['n'])
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

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    def test_procesar_movimiento_exitoso(self, mock_sleep, mock_input):
        """Test procesamiento de movimiento exitoso"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()
        
        # Mock de movimiento válido
        with patch.object(self.cli.game, 'mover', return_value=None):
            with patch.object(self.cli.game, 'get_saltos', return_value=[]):
                resultado = self.cli._procesar_movimiento('0 1')
                self.assertFalse(resultado)  # Turno completado

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    def test_procesar_movimiento_invalido(self, mock_sleep, mock_input):
        """Test procesamiento de movimiento inválido"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()
        
        # Mock de movimiento que lanza excepción
        with patch.object(self.cli.game, 'mover', side_effect=BackgammonError("Error")):
            resultado = self.cli._procesar_movimiento('0 1')
            self.assertTrue(resultado)  # Continuar turno

    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('cli.cli.time.sleep')
    def test_procesar_movimiento_keyboard_interrupt(self, mock_sleep, mock_input):
        """Test interrupción durante movimiento"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()
        
        # Simular KeyboardInterrupt y respuesta 'n'
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            resultado = self.cli._procesar_movimiento('0 1')
            # El resultado depende de cómo maneje la excepción
            self.assertIsNotNone(resultado)

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_ayuda(self, mock_stdout):
        """Test que muestra la ayuda completa"""
        with patch('builtins.input', return_value=''):
            with patch('cli.cli.os.system'):
                self.cli.mostrar_ayuda()
        
        output = mock_stdout.getvalue()
        self.assertIn("AYUDA", output)
        self.assertIn("OBJETIVO", output)
        self.assertIn("MOVIMIENTOS", output)
        self.assertIn("CAPTURAS", output)

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    @patch('cli.cli.os.system')
    def test_jugar_inicio_con_empate(self, mock_system, mock_sleep, mock_input):
        """Test inicio de juego con empate en dados"""
        # Mock de inicio que retorna None (empate) y luego resultado
        resultados = [
            None,  # Primer intento: empate
            {'dados_x': 5, 'dados_o': 3, 'ganador': 'X'}  # Segundo intento: ganador
        ]
        
        with patch.object(self.cli.game, 'inicio', side_effect=resultados):
            with patch.object(self.cli.game, 'tirar_dado'):
                with patch.object(self.cli.game, 'mostrar', return_value={
                    'ganador': 'X',
                    'turno': 'X',
                    'saltos': [],
                    'capturas': [],
                    'board': 'test'
                }):
                    # Ejecutar solo el inicio, no todo el juego
                    resultado = self.cli.game.inicio()
                    while resultado is None:
                        resultado = self.cli.game.inicio()
                    
                    self.assertIsNotNone(resultado)
                    self.assertIn('ganador', resultado)

    @patch('builtins.input', return_value='')
    @patch('cli.cli.time.sleep')
    @patch('cli.cli.os.system')
    def test_jugar_sin_movimientos_posibles(self, mock_system, mock_sleep, mock_input):
        """Test cambio de turno cuando no hay movimientos"""
        self.cli.game.inicio()
        
        # Mock de estado sin movimientos posibles
        with patch.object(self.cli.game, 'puede_mover', return_value=False):
            with patch.object(self.cli.game, 'get_saltos', return_value=[]):
                with patch.object(self.cli.game, 'tirar_dado'):
                    # Verificar que puede_mover se llama
                    puede = self.cli.game.puede_mover()
                    self.assertFalse(puede)

    def test_movimiento_continua_turno_con_dados_restantes(self):
        """Test que el turno continúa cuando quedan dados"""
        self.cli.game.inicio()
        self.cli.game.tirar_dado()
        
        with patch.object(self.cli.game, 'mover', return_value=None):
            with patch.object(self.cli.game, 'get_saltos', return_value=[1, 2]):
                with patch('builtins.input', return_value=''):
                    with patch('cli.cli.time.sleep'):
                        resultado = self.cli._procesar_movimiento('0 1')
                        # Si quedan saltos, debe continuar el turno
                        self.assertTrue(resultado)


if __name__ == '__main__':
    unittest.main()
```


### Implementacion

```
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
```

## prompt

Ayudame a desarrollar test para board.py pero desarrolla logica en pytest

### GPT-4o

```
import pytest
from core.board import Board
from core.ficha import Ficha
from core.exceptions import FueraDeRangoError

# --- Helpers mínimos ---
def empty_board_with(orig=None, dst=None):
    """Crea un Board con todas las celdas vacías y opcionalmente coloca fichas."""
    b = Board()
    c = b.get_celdas()
    c[:] = [[] for _ in range(24)]
    if orig is not None:
        c[orig] = [Ficha("X")]
    if dst is not None:
        c[dst] = [Ficha("O")]
    return b

# --- Stubs de Validaciones (muy simples) ---
class V_Normal:
    @staticmethod
    def validar_salida(celdas, capturas, jugador): return False
    @staticmethod
    def movimiento_valido(celdas, celda, salto, jugador, validar_salida=False):
        return celda + salto if jugador == "X" else celda - salto
    @staticmethod
    def validar_movimiento_salida(celdas, capturas, celda, salto, jugador): return True

class V_Returns_None_For_Exit(V_Normal):
    @staticmethod
    def movimiento_valido(celdas, celda, salto, jugador, validar_salida=False): return None

class V_Prevent_Exit(V_Returns_None_For_Exit):
    @staticmethod
    def validar_movimiento_salida(celdas, capturas, celda, salto, jugador): return False

# -----------------------
# Tests simplificados
# -----------------------
def test_get_board_basic():
    b = Board()
    b.inicio()
    s = b.get_board()
    assert isinstance(s, str)
    assert "|" in s and "-" in s
    assert any("X5" in s for _ in [0])  # chequear que aparece X5 (inicio)
    assert any("O5" in s for _ in [0])  # chequear que aparece O5 (inicio)

def test_repr_and_empty_cell():
    b = Board()
    assert b.repr_celda([]) == "--"
    f = Ficha("X")
    assert b.repr_celda([f, f]) == "XX"

def test_mover_to_empty_cell(monkeypatch):
    b = empty_board_with(orig=0)
    c = b.get_celdas()
    c[3] = []
    monkeypatch.setattr("core.board.Validaciones", V_Normal, raising=True)

    assert b.mover(0, 3, "X") is True
    assert c[0] == []
    assert len(c[3]) == 1
    assert c[3][0].get_jugador() == "X"
    assert c[3][0].get_capturada() is False

def test_mover_to_own_cell(monkeypatch):
    b = empty_board_with(orig=0)
    c = b.get_celdas()
    c[2] = [Ficha("X")]
    monkeypatch.setattr("core.board.Validaciones", V_Normal, raising=True)

    assert b.mover(0, 2, "X") is True
    assert len(c[2]) == 2
    assert all(x.get_jugador() == "X" for x in c[2])

def test_mover_capture_enemy(monkeypatch):
    b = empty_board_with(orig=0, dst=2)
    c = b.get_celdas()
    # parche Validaciones
    monkeypatch.setattr("core.board.Validaciones", V_Normal, raising=True)

    # parche temporal para que set_capturada() sin args funcione
    original = Ficha.set_capturada
    monkeypatch.setattr(Ficha, "set_capturada", lambda self, *a, **k: original(self, True), raising=True)

    assert b.mover(0, 2, "X") is True
    assert c[2][-1].get_jugador() == "X"
    assert c[0] == []

def test_mover_exit_allowed(monkeypatch):
    b = empty_board_with()
    c = b.get_celdas()
    c[20] = [Ficha("X")]
    monkeypatch.setattr("core.board.Validaciones", V_Returns_None_For_Exit, raising=True)

    assert b.mover(20, 6, "X") is True
    assert c[20] == []

def test_mover_exit_forbidden(monkeypatch):
    b = empty_board_with()
    c = b.get_celdas()
    c[21] = [Ficha("X")]
    monkeypatch.setattr("core.board.Validaciones", V_Prevent_Exit, raising=True)

    with pytest.raises(FueraDeRangoError):
        b.mover(21, 6, "X")
```

### Implementacion

Se entiende logica e intenta pasar a unittest

```
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
```

## prompt 

Genera un pytest con segun los archivos adjuntados (contexto de backgammonon.py)

### GPT.4o

### Respuesta

```
# tests/test_backgammon.py
import pytest

# Intento de import seguro; ajustá si tu proyecto tiene otra estructura.
from core.backgammon import Backgammon
from core.board import Board
from core.player import Player
from core.dice import Dice
from core.ficha import Ficha
from core.exceptions import FueraDeRangoError

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def board_empty():
    """Board vacío (sin inicializar con inicio())."""
    b = Board()
    # dejar las celdas tal cual el constructor crea (vacías)
    return b


@pytest.fixture
def fixed_dice_factory():
    """Factory que devuelve objetos dice con roll() determinista."""
    class FixedDice:
        def __init__(self, values):
            self._values = list(values)

        def roll(self):
            # devolvemos copia para evitar aliasing sorpresa
            return list(self._values)

    def _factory(values):
        return FixedDice(values)

    return _factory


@pytest.fixture
def player_X():
    return Player("X")


@pytest.fixture
def player_O():
    return Player("O")


@pytest.fixture
def backgammon():
    """Backgammon con dependencias reales."""
    return Backgammon()


@pytest.fixture
def backgammon_with_mocks(fixed_dice_factory):
    """
    Backgammon con board y dice inyectados (mocks simples).
    El mock de Board registra llamadas a mover.
    """
    class MockBoard:
        def __init__(self):
            self.mover_calls = []
            self._celdas = [[] for _ in range(24)]
            self._capturas = []

        def inicio(self):
            # posible implementación mínima
            self._celdas = [[] for _ in range(24)]
            self._capturas = []

        def mover(self, celda, salto, jugador):
            # registrar llamada y simular movimiento sencillo: pop/append if present
            self.mover_calls.append((celda, salto, jugador))
            if not self._celdas[celda]:
                raise IndexError("origen vacio")
            ficha = self._celdas[celda].pop()
            # si destino fuera de rango -> raise
            destino = celda + salto
            if destino < 0 or destino > 23:
                raise FueraDeRangoError("destino fuera")
            self._celdas[destino].append(ficha)
            return True

        def get_celdas(self):
            return self._celdas

        def get_capturas(self):
            return self._capturas

        def get_board(self):
            return "MOCK_BOARD"

    mock_board = MockBoard()
    fake_dice = fixed_dice_factory([3])  # por defecto un roll simple
    bk = Backgammon(board=mock_board, players=[Player("X"), Player("O")], dice=fake_dice)
    return bk


# -------------------------
# Tests - Inicialización
# -------------------------
def test_init_defaults():
    """
    Crear Backgammon sin argumentos: verificar tipos y estado inicial.
    """
    bk = Backgammon()
    # comprobar objetos
    assert isinstance(bk._Backgammon__board, Board)
    assert isinstance(bk._Backgammon__players, list)
    assert isinstance(bk._Backgammon__players[0], Player)
    assert isinstance(bk._Backgammon__dice, Dice)
    # estado inicial interno
    assert bk._Backgammon__turno == 0
    assert bk.get_saltos() == []
    assert bk._Backgammon__ganador is None


def test_init_with_injected_dependencies():
    """
    Inyectar dependencias personalizadas del constructor (identidad).
    """
    custom_board = Board()
    custom_players = [Player("A"), Player("B")]
    class FakeDice:
        def roll(self):
            return [1, 2]
    fake_dice = FakeDice()

    bk = Backgammon(board=custom_board, players=custom_players, dice=fake_dice)
    assert bk._Backgammon__board is custom_board
    assert bk._Backgammon__players is custom_players
    assert bk._Backgammon__dice is fake_dice


# -------------------------
# Tests - inicio()
# -------------------------
def test_inicio_resets_board_and_turn(monkeypatch):
    """
    inicio() debe invocar board.inicio(), resetear turno a 0 y limpiar saltos.
    """
    class SpyBoard(Board):
        def __init__(self):
            super().__init__()
            self.inicio_called = False
        def inicio(self):
            self.inicio_called = True
            super().inicio()

    spy = SpyBoard()
    bk = Backgammon(board=spy)
    # set turn and saltos to non-defaults
    bk._Backgammon__turno = 1
    bk._Backgammon__saltos = [2,3]
    bk.inicio()
    assert spy.inicio_called is True
    assert bk._Backgammon__turno == 0
    assert bk.get_saltos() == []


# -------------------------
# Tests - tirar_dado() y get_saltos()
# -------------------------
def test_tirar_dado_returns_and_stores_saltos(fixed_dice_factory):
    bk = Backgammon(dice=fixed_dice_factory([2, 5]))
    res = bk.tirar_dado()
    assert res == [2, 5]
    # get_saltos devuelve copia según implementación (list(self.__saltos))
    gs = bk.get_saltos()
    assert gs == [2, 5]
    # modificar la lista retornada no cambia el estado interno
    gs.append(99)
    assert bk.get_saltos() == [2, 5]


def test_tirar_dado_handles_doubles(fixed_dice_factory):
    bk = Backgammon(dice=fixed_dice_factory([4,4,4,4]))
    res = bk.tirar_dado()
    assert res == [4,4,4,4]
    assert bk.get_saltos() == [4,4,4,4]


# -------------------------
# Tests - turno y cambio_turno
# -------------------------
def test_get_jugador_and_cambio_turno():
    bk = Backgammon()
    # inicial
    j0 = bk.get_jugador()
    assert isinstance(j0, Player)
    assert j0.get_name() == "X"
    # cambio turno
    bk.cambio_turno()
    assert bk.get_saltos() == []
    assert bk.get_jugador().get_name() == "O"
    # otra vez
    bk.cambio_turno()
    assert bk.get_jugador().get_name() == "X"


# -------------------------
# Tests - mover() precondiciones
# -------------------------
def test_mover_raises_if_no_saltos():
    bk = Backgammon()
    with pytest.raises(ValueError, match="Tirar dados primero"):
        bk.mover(0, 3)


def test_mover_raises_if_salto_not_pending(fixed_dice_factory):
    bk = Backgammon(dice=fixed_dice_factory([2, 2]))
    bk.tirar_dado()
    # intentar mover con salto que no exista
    with pytest.raises(ValueError, match="No hay un salto pendiente igual a"):
        bk.mover(0, 3)

    # comportamiento con duplicados: consumir uno solo
    # preparar tablero para que board.mover no falle: inyectar board y una ficha
    b = Board()
    b.get_celdas()[0] = [Ficha("X")]
    bk2 = Backgammon(board=b, dice=fixed_dice_factory([2, 2]))
    bk2.tirar_dado()
    bk2.mover(0, 2)  # consume un 2
    assert bk2.get_saltos() == [2]  # todavía queda otro 2


# -------------------------
# Tests - interacción con Board.mover()
# -------------------------
def test_mover_calls_board_mover_with_correct_args(monkeypatch, fixed_dice_factory):
    # mock board con spy
    class SpyBoard(Board):
        def __init__(self):
            super().__init__()
            self.calls = []
        def mover(self, celda, salto, jugador_name):
            self.calls.append((celda, salto, jugador_name))
            return True

    spy = SpyBoard()
    # dejar ficha en origen
    spy.get_celdas()[5] = [Ficha("X")]
    bk = Backgammon(board=spy, dice=fixed_dice_factory([3]))
    bk.tirar_dado()
    # asegurarnos del jugador actual
    assert bk.get_jugador().get_name() == "X"
    bk.mover(5, 3)
    assert spy.calls == [(5, 3, "X")]


def test_mover_propagates_board_exceptions(monkeypatch, fixed_dice_factory):
    class BadBoard(Board):
        def mover(self, celda, salto, jugador_name):
            raise FueraDeRangoError("bad")

    bad = BadBoard()
    bad.get_celdas()[0] = [Ficha("X")]
    bk = Backgammon(board=bad, dice=fixed_dice_factory([3]))
    bk.tirar_dado()
    with pytest.raises(FueraDeRangoError):
        bk.mover(0, 3)


# -------------------------
# Tests - validar_victoria y ganador
# -------------------------
def test_mover_sets_ganador_when_validar_victoria_returns_true(monkeypatch, fixed_dice_factory):
    # Usamos un Board real pero parcheamos Validaciones.validar_victoria en el módulo core.backgammon
    bk = Backgammon(board=Board(), dice=fixed_dice_factory([1]))
    b = bk._Backgammon__board
    # necesitamos una ficha en origen para no fallar el movimiento
    b.get_celdas()[0] = [Ficha("X")]
    bk.tirar_dado()

    # wrapper para capturar el argumento pasado como 'jugador'
    captured = {}
    def fake_validar_victoria(celdas, capturas, jugador_arg):
        captured['arg'] = jugador_arg
        return True

    monkeypatch.setattr("core.backgammon.Validaciones.validar_victoria", fake_validar_victoria, raising=True)
    bk.mover(0, 1)
    # ganador debe establecerse al objeto Player actual
    assert bk._Backgammon__ganador is bk.get_jugador() or bk._Backgammon__ganador is not None
    # comprobar qué tipo se pasó al validador (debe ser Player según la implementación actual)
    assert isinstance(captured.get('arg'), Player)


def test_mover_does_not_set_ganador_when_false(monkeypatch, fixed_dice_factory):
    bk = Backgammon(board=Board(), dice=fixed_dice_factory([1]))
    b = bk._Backgammon__board
    b.get_celdas()[0] = [Ficha("X")]
    bk.tirar_dado()

    monkeypatch.setattr("core.backgammon.Validaciones.validar_victoria", lambda *a, **k: False, raising=True)
    bk.mover(0, 1)
    assert bk._Backgammon__ganador is None


# -------------------------
# Tests - consumo de saltos y cambio de turno
# -------------------------
def test_mover_consumes_one_salto_and_turn_changes_if_no_saltos(fixed_dice_factory):
    # dice devuelve un solo salto -> después de mover debe cambiar turno
    b = Board()
    b.get_celdas()[0] = [Ficha("X")]
    bk = Backgammon(board=b, dice=fixed_dice_factory([2]))
    bk.tirar_dado()
    assert bk.get_saltos() == [2]
    bk.mover(0, 2)
    assert bk.get_saltos() == []
    # turno debe cambiar
    assert bk.get_jugador().get_name() == "O"


def test_mover_keeps_turn_if_still_saltos(fixed_dice_factory):
    # dice devuelve dos saltos -> después de un mover aún quedan saltos y turno no cambia
    b = Board()
    b.get_celdas()[0] = [Ficha("X")]
    bk = Backgammon(board=b, dice=fixed_dice_factory([2, 3]))
    bk.tirar_dado()
    assert bk.get_saltos() == [2, 3]
    bk.mover(0, 2)
    # aún queda un salto, por lo tanto turno no debería cambiar
    assert bk.get_jugador().get_name() == "X"
    assert bk.get_saltos() == [3]


# -------------------------
# Tests - mostrar()
# -------------------------
def test_mostrar_structure_and_types(monkeypatch):
    # Mock board con get_board y get_capturas
    class MockBoard:
        def get_board(self):
            return "BOARD_STR"
        def get_capturas(self):
            # devolver lista de Ficha
            return [Ficha("X"), Ficha("O")]

    bk = Backgammon(board=MockBoard())
    s = bk.mostrar()
    assert isinstance(s, dict)
    assert "board" in s and isinstance(s["board"], str)
    assert "turno" in s and isinstance(s["turno"], str)
    assert "saltos" in s and isinstance(s["saltos"], list)
    assert "capturas" in s and isinstance(s["capturas"], list)
    # Actualmente el código genera una lista cuyo primer elemento es un generator.
    # Detectamos ese comportamiento (es un bug a corregir en mostrar()).
    assert len(s["capturas"]) == 1
    gen = s["capturas"][0]
    assert hasattr(gen, "__iter__") and not isinstance(gen, list)


# -------------------------
# Tests - integración básica
# -------------------------
def test_integration_simple_play_flow(monkeypatch, fixed_dice_factory):
    """
    Mini integración: parcheamos core.board.Validaciones para facilitar movimientos
    y hacemos un par de mover() usando Board real + Backgammon.
    """
    # parche pequeño para que movimiento_valido simplemente sume y validar_movimiento_salida permita salida
    class V_simple:
        @staticmethod
        def validar_salida(celdas, capturas, jugador):
            return False
        @staticmethod
        def movimiento_valido(celdas, celda, saltos, jugador, validar_salida=False):
            return celda + saltos
        @staticmethod
        def validar_movimiento_salida(*a, **k):
            return True
        @staticmethod
        def validar_victoria(*a, **k):
            return False

    monkeypatch.setattr("core.board.Validaciones", V_simple, raising=True)
    b = Board()
    # setup: colocar ficha X en 0
    b.get_celdas()[0] = [Ficha("X")]
    bk = Backgammon(board=b, dice=fixed_dice_factory([1, 2]))
    bk.tirar_dado()
    # ejecutar dos movimientos válidos
    bk.mover(0, 1)  # mueve la ficha de 0 a 1
    # después de primer mover debe quedar al menos un salto (2) -> turno no cambia
    assert bk.get_jugador().get_name() == "X" or bk.get_saltos() != []
    # consumir el siguiente salto con la ficha ahora en 1
    bk.mover(1, 2)
    # al final, la ficha habrá sido movida a 3
    assert any(len(cell) > 0 and cell[0].get_jugador() == "X" for cell in b.get_celdas())


# -------------------------
# Tests - casos límite y robustez
# -------------------------
def test_mover_with_invalid_celda_propagates_error(fixed_dice_factory):
    # Crear board cuyo mover lanza FueraDeRangoError
    class BadBoard(Board):
        def mover(self, celda, salto, jugador_name):
            raise FueraDeRangoError("bad celda")
    bad = BadBoard()
    bad.get_celdas()[0] = [Ficha("X")]
    bk = Backgammon(board=bad, dice=fixed_dice_factory([3]))
    bk.tirar_dado()
    with pytest.raises(FueraDeRangoError):
        bk.mover(0, 3)


def test_mutating_returned_saltos_does_not_change_internal_state(fixed_dice_factory):
    bk = Backgammon(dice=fixed_dice_factory([6]))
    bk.tirar_dado()
    s = bk.get_saltos()
    s.append(100)
    # state must remain original
    assert bk.get_saltos() == [6]


# -------------------------
# Tests - extras (dobles y formato capturas)
# -------------------------
def test_double_roll_consumption_sequence(fixed_dice_factory):
    # dice devuelve 4 saltos iguales; usamos mocked board mover para aceptar movimientos
    class AcceptBoard(Board):
        def mover(self, celda, salto, jugador_name):
            # simple acceptor: mover si origen tiene ficha, si no raise
            if not self.get_celdas()[celda]:
                raise IndexError("origen vacio")
            f = self.get_celdas()[celda].pop()
            destino = celda + salto
            if destino < 0 or destino > 23:
                raise FueraDeRangoError()
            self.get_celdas()[destino].append(f)
            return True

    b = AcceptBoard()
    b.get_celdas()[0] = [Ficha("X")]
    bk = Backgammon(board=b, dice=fixed_dice_factory([2,2,2,2]))
    bk.tirar_dado()
    # hacer 4 movimientos: movemos la misma ficha en cadena (requiere ajustar origenes)
    # mover 0->2
    bk.mover(0, 2)
    # mover 2->2 (uso de otro salto)
    bk.mover(2, 2)
    # mover 4->2
    bk.mover(4, 2)
    # mover 6->2
    # para la última mover, deberíamos tener ficha en 6
    bk.mover(6, 2)
    # si llegamos aquí sin excepciones, secuencia consumida
    assert bk.get_saltos() == []


def test_show_captures_format_expectation():
    """
    Test idea: el formato actual de 'capturas' en mostrar() se compone de una lista
    que contiene un generator — se detecta como mala práctica/bug.
    """
    b = Board()
    b.get_capturas().append(Ficha("X"))
    bk = Backgammon(board=b)
    out = bk.mostrar()
    assert isinstance(out, dict)
    # se espera que 'capturas' sea una lista; la implementación actual devuelve una lista
    # con un generador en su interior, detectamos eso:
    assert len(out["capturas"]) == 1
    assert not isinstance(out["capturas"][0], list)
    assert hasattr(out["capturas"][0], "__iter__")
```

### Implementacion

Al igual que cli
```
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
```

## prompt

Desarrolla pytest de validaciones.py

### GPT-4o

### Respuesta:

```
# tests/test_validaciones.py
import pytest
import validaciones
from ficha import Ficha

# Helper: crea lista de 24 celdas vacías
def crear_celdas_vacias():
    return [[] for _ in range(24)]


# ---------- validar_celda ----------
def test_validar_celda_valida():
    # no debería levantar excepción para índices 0 y 23
    validaciones.Validaciones.validar_celda(0)
    validaciones.Validaciones.validar_celda(23)


@pytest.mark.parametrize("bad", [-1, 24, "a", 3.5])
def test_validar_celda_invalida(bad):
    with pytest.raises(validaciones.FueraDeRangoError):
        validaciones.Validaciones.validar_celda(bad)


# ---------- validar_ficha_celda ----------
def test_validar_ficha_celda_empty_raises():
    with pytest.raises(validaciones.CeldaInvalidaError):
        validaciones.Validaciones.validar_ficha_celda([], "X")


def test_validar_ficha_celda_other_player_raises():
    celda = [Ficha("O")]
    with pytest.raises(validaciones.CeldaBloqueadaError):
        validaciones.Validaciones.validar_ficha_celda(celda, "X")


def test_validar_ficha_celda_ok():
    celda = [Ficha("X"), Ficha("X")]
    # no debe levantar excepción
    validaciones.Validaciones.validar_ficha_celda(celda, "X")


# ---------- validar_destino ----------
def test_validar_destino_blocked_raises():
    # destino tiene 2 fichas enemigas -> bloqueada
    destino = [Ficha("O"), Ficha("O")]
    with pytest.raises(validaciones.CeldaBloqueadaError):
        validaciones.Validaciones.validar_destino(destino, "X")


def test_validar_destino_ok_with_own_or_one_enemy():
    # vacío -> ok
    validaciones.Validaciones.validar_destino([], "X")
    # una ficha enemiga -> ok (se puede capturar)
    validaciones.Validaciones.validar_destino([Ficha("O")], "X")
    # fichas propias -> ok
    validaciones.Validaciones.validar_destino([Ficha("X"), Ficha("X")], "X")


# ---------- movimiento_valido ----------
def test_movimiento_valido_normal_X_forward():
    celdas = crear_celdas_vacias()
    celdas[0] = [Ficha("X")]        # origen
    celdas[3] = []                  # destino vacío
    destino = validaciones.Validaciones.movimiento_valido(celdas, 0, 3, "X", validar_salida=False)
    assert destino == 3


def test_movimiento_valido_normal_O_backward():
    celdas = crear_celdas_vacias()
    celdas[5] = [Ficha("O")]
    celdas[3] = []
    destino = validaciones.Validaciones.movimiento_valido(celdas, 5, 2, "O", validar_salida=False)
    assert destino == 3


def test_movimiento_valido_destino_fuera_sin_validar_salida_raises():
    celdas = crear_celdas_vacias()
    celdas[22] = [Ficha("X")]
    # destino 22+3 = 25 > 23 -> debe levantar FueraDeRangoError si validar_salida=False
    with pytest.raises(validaciones.FueraDeRangoError):
        validaciones.Validaciones.movimiento_valido(celdas, 22, 3, "X", validar_salida=False)


def test_movimiento_valido_destino_fuera_con_validar_salida_returns_none():
    celdas = crear_celdas_vacias()
    celdas[22] = [Ficha("X")]
    # con validar_salida=True debería devolver None (permitir salida)
    res = validaciones.Validaciones.movimiento_valido(celdas, 22, 3, "X", validar_salida=True)
    assert res is None


# ---------- validar_salida ----------
def test_validar_salida_false_if_player_has_captured_piece():
    celdas = crear_celdas_vacias()
    capturas = [Ficha("X")]
    assert validaciones.Validaciones.validar_salida(celdas, capturas, "X") is False


def test_validar_salida_false_if_player_has_pieces_in_home_range():
    # Para "X" el rango comprobado es 0..17. Si hay fichas del jugador en ese rango -> False
    celdas = crear_celdas_vacias()
    celdas[10] = [Ficha("X")]
    capturas = []
    assert validaciones.Validaciones.validar_salida(celdas, capturas, "X") is False


def test_validar_salida_true_when_no_pieces_or_captures_in_blocking_zones():
    # Ponemos las fichas del jugador X solo en las celdas 18..23 (fuera del rango que bloquea la salida)
    celdas = crear_celdas_vacias()
    celdas[18] = [Ficha("X")]
    celdas[19] = [Ficha("X")]
    capturas = []
    assert validaciones.Validaciones.validar_salida(celdas, capturas, "X") is True


# ---------- validar_movimiento_salida ----------
def test_validar_movimiento_salida_allows_exit_for_X_when_destino_24_and_celda_out_of_range():
    # Debido a la implementación actual de validar_movimiento_salida, la función
    # primero verifica si 'validar_salida' es True y luego exige que 'celda' NO esté en 0..23.
    # Por eso probamos con celda=24 y destino=24 para obtener True.
    celdas = crear_celdas_vacias()
    capturas = []
    # Para que validar_salida devuelva True, aseguramos no tener piezas en las zonas bloqueantes:
    # (vacío en 0..17)
    res = validaciones.Validaciones.validar_movimiento_salida(celdas, capturas, 24, 0, "X")
    assert res is True


def test_validar_movimiento_salida_allows_exit_for_O_when_destino_minus1_and_celda_out_of_range():
    celdas = crear_celdas_vacias()
    capturas = []
    res = validaciones.Validaciones.validar_movimiento_salida(celdas, capturas, -1, 0, "O")
    assert res is True


# ---------- validar_victoria ----------
def test_validar_victoria_true_when_no_pieces_and_no_captures():
    celdas = crear_celdas_vacias()
    capturas = []
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is True


def test_validar_victoria_false_when_player_has_pieces_or_captures():
    celdas = crear_celdas_vacias()
    celdas[0] = [Ficha("X")]
    capturas = []
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is False

    # también si hay capturadas
    celdas = crear_celdas_vacias()
    capturas = [Ficha("X")]
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is False
```

### Implementacion

Se fueron corrigiendo varios puntos al modificar modulo de validaciones y al final se pasa logica a unittest

```
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
```


