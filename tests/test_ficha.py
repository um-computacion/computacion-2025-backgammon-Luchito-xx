import pytest
from core.ficha import Ficha 

def test_crear_ficha():
    ficha = Ficha("Lucho")
    assert ficha.get_jugador() == "Lucho"
    assert ficha.get_capturada() is False

def test_set_jugador():
    ficha = Ficha("X")
    ficha.set_jugador("O")
    assert ficha.get_jugador() == "O"

def test_set_capturada():
    ficha = Ficha("X")
    ficha.set_capturada(True)
    assert ficha.get_capturada() is True
    ficha.set_capturada(False)
    assert ficha.get_capturada() is False

def test_repr_estado_libre():
    ficha = Ficha("X")
    assert "Dueño de la ficha es X y esta Libre" == repr(ficha)

def test_repr_estado_capturada():
    ficha = Ficha("X")
    ficha.set_capturada(True)
    assert "Dueño de la ficha es X y esta Capturada" == repr(ficha)
