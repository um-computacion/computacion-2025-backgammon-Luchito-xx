import pytest       
from core.board import Board
from core.ficha import Ficha  


def test_inicio_setup():
    b = Board()
    b.inicio()
    c = b.get_celdas()

    
    assert len(c[0]) == 2
    assert all(f.get_jugador() == "X" for f in c[0])

    assert len(c[11]) == 5
    assert all(f.get_jugador() == "X" for f in c[11])

    assert len(c[23]) == 2
    assert all(f.get_jugador() == "O" for f in c[23])

    assert len(c[12]) == 5
    assert all(f.get_jugador() == "O" for f in c[12])


def test_repr_celda():
    b = Board()


    assert b.repr_celda([]) == "--"

    celda = [Ficha("X") for _ in range(3)] 
    assert b.repr_celda(celda) == "XXX"


def test_get_board_contains_expected_lines():
    b = Board()
    b.inicio()
    s = b.get_board()

    assert "00:XX" in s         
    assert "11:XXXXX" in s      
    assert "23:OO" in s         
    assert "12:OOOOO" in s      





