import pytest       
from core.board import Board
from core.ficha import Ficha  

def test_get_board():

    board = Board()
    board.inicio()
    tablero_str = board.get_board()
    
    assert isinstance(tablero_str, str)
    for n in range(1, 25):
        assert str(n) in tablero_str, f"no esta numero {n}"

    assert "|" in tablero_str
    assert "-" in tablero_str

    lineas = tablero_str.split("\n")
    assert len(lineas) >= 5

def test_get_board_inicio():
    
    board = Board()
    board.inicio()
    tablero_str = board.get_board()

    assert "X2" in tablero_str  
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