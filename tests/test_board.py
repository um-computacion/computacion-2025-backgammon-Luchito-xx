import pytest       
from core.board import Board
from core.ficha import Ficha 
from core.exceptions import *

def test_get_board():
    board = Board()
    board.inicio()
    tablero_str = board.get_board()

    assert isinstance(tablero_str, str)
    for n in range(0, 24):
        assert str(n) in tablero_str, f"no esta numero {n}"


def test_get_board_inicio():
    
    board = Board()
    board.inicio()
    tablero_str = board.get_board()

    assert "X5" in tablero_str  
    assert "X3" in tablero_str 
    assert "X5" in tablero_str 

    assert "O2" in tablero_str  
    assert "O5" in tablero_str 
    assert "O3" in tablero_str  
    assert "O5" in tablero_str  


def test_get_board_celdas_vacias():

    board = Board()
    board.inicio()
    board.get_celdas()[0] = []  
    tablero_str = board.get_board()

    assert "--" in tablero_str, "celda vacia no esta como '--'"

def test_get_board_estructura():

    board = Board()
    board.inicio()
    tablero_str = board.get_board()
    lineas = tablero_str.split("\n")

    assert len(lineas[0]) == len(lineas[-1]), "numeros no estan alineados"
    assert len(lineas[1]) == len(lineas[-2]), "fichas no estan alineadas"
    assert "-" * 4 in tablero_str, "falta barra del medio"

def test_repr_celda():

    board = Board()
    ficha_x = Ficha("X")
    ficha_o = Ficha("O")

    assert board.repr_celda([]) == "--"
    assert board.repr_celda([ficha_x, ficha_x]) == "XX"
    assert board.repr_celda([ficha_o, ficha_o, ficha_o]) == "OOO"

    

class V_Normal:
    @staticmethod
    def movimiento_valido(celdas, capturas, celda, salto, jugador, validar_salida=None):
        return celda + salto if jugador == "X" else celda - salto
    @staticmethod
    def validar_movimiento_salida(celdas, capturas, celda, salto, jugador):
        return True
    @staticmethod
    def validar_salida(celdas, capturas, jugador):
        return True


class V_Returns_None_For_Exit(V_Normal):
    @staticmethod
    def movimiento_valido(celdas, capturas, celda, salto, jugador, validar_salida=None):
        return None

class V_Prevent_Exit(V_Returns_None_For_Exit):
    @staticmethod
    def validar_movimiento_salida(celdas, capturas, celda, salto, jugador):
        return False


def test_mover_destino_vacio(monkeypatch):
    """
    Mover ficha X desde celda 0 a celda 3 cuando la celda destino está vacía.
    """
    b = Board()
    c = b.get_celdas()
    c[:] = [[] for _ in range(24)]
    c[0] = [Ficha("X")]
    c[3] = []

    monkeypatch.setattr("core.board.Validaciones", V_Normal, raising=True)

    # ejecutar mover (no esperamos True/False, comprobamos el estado del tablero)
    b.mover(0, 3, "X")

    assert len(c[0]) == 0
    assert len(c[3]) == 1
    assert c[3][0].get_jugador() == "X"

def test_mover_destino_fichas_propias(monkeypatch):
    """
    Mover ficha a una celda que ya contiene fichas propias.
    """
    b = Board()
    c = b.get_celdas()
    c[:] = [[] for _ in range(24)]
    c[0] = [Ficha("X")]
    c[2] = [Ficha("X")]

    monkeypatch.setattr("core.board.Validaciones", V_Normal, raising=True)

    b.mover(0, 2, "X")

    assert len(c[0]) == 0
    assert len(c[2]) == 2
    assert all(f.get_jugador() == "X" for f in c[2])


def test_mover_destino_capturar_enemigo(monkeypatch):
    """
    Mover una ficha sobre una celda con una sola ficha enemiga.
    """
    b = Board()
    c = b.get_celdas()
    c[:] = [[] for _ in range(24)]

    origen = 0
    destino = 2
    ficha_X = Ficha("X")
    ficha_O = Ficha("O")
    c[origen] = [ficha_X]
    c[destino] = [ficha_O]

    monkeypatch.setattr("core.board.Validaciones", V_Normal, raising=True)

    # parcheo temporal para asegurar set_capturada funciona como se espera
    original_set = Ficha.set_capturada
    def wrapper(self, *args, **kwargs):
        return original_set(self, True)
    monkeypatch.setattr(Ficha, "set_capturada", wrapper, raising=True)

    b.mover(origen, destino - origen, "X")

    # destino ahora tiene ficha X, y la ficha O deberia estar en capturas
    assert len(c[origen]) == 0
    assert len(c[destino]) == 1
    assert c[destino][0].get_jugador() == "X"
    caps = b.get_capturas()
    assert len(caps) == 1
    assert caps[0].get_jugador() == "O"

def test_mover_sacar_ficha_tablero_permitido(monkeypatch):
    """
    Si movimiento_valido devuelve None (intención de salida) y validar_movimiento_salida
    es True, la ficha debe ser removida (pop) del tablero.
    """
    b = Board()
    c = b.get_celdas()
    c[:] = [[] for _ in range(24)]
    c[20] = [Ficha("X")]

    monkeypatch.setattr("core.board.Validaciones", V_Returns_None_For_Exit, raising=True)

    b.mover(20, 6, "X")

    assert len(c[20]) == 0

def test_mover_sacar_ficha_tablero_no_permitido(monkeypatch):
    """
    Si movimiento_valido devuelve None y validar_movimiento_salida devuelve False,
    el comportamiento actual del Board es simplemente no colocar la ficha (se removió),
    comprobamos que no hay capturas y la celda origen quedó vacía.
    """
    b = Board()
    c = b.get_celdas()
    c[:] = [[] for _ in range(24)]
    c[21] = [Ficha("X")]

    monkeypatch.setattr("core.board.Validaciones", V_Prevent_Exit, raising=True)

    b.mover(21, 6, "X")

    assert len(c[21]) == 0
    assert b.get_capturas() == []

def test_reingreso_ficha():
    """
    Reingreso de una ficha desde capturas a la celda correspondiente.
    """
    b = Board()
    c = b.get_celdas()
    c[:] = [[] for _ in range(24)]

    ficha_O = Ficha("O")
    ficha_O.set_capturada(True)
    b.get_capturas().append(ficha_O)

    b.mover(-1, 4, "O")

    assert len(b.get_capturas()) == 0
    assert len(c[20]) == 1
    assert c[20][0].get_jugador() == "O"