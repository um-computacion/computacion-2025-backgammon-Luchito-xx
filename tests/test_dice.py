import pytest
from core.dice import Dice  

def test_creacion_dice():
    dice = Dice()
    assert isinstance(dice.get_valor(), list)
    assert all(isinstance(valor, int) for valor in dice.get_valor())
    assert len(dice.get_valor()) == 2

def test_roll_resultados_validos():
    dice = Dice()
    valores = dice.roll()
    assert all(1 <= valor <= 6 for valor in valores)

def test_roll_dobles():
    dice = Dice()
    dice._Dice__valor__ = [3, 3]
    dice.roll()
    valores = dice.get_valor()
    assert len(valores) in (2, 4)
    if len(valores) == 4:
        assert all(valor == valores[0] for valor in valores)

def test_str_output():
    d = Dice()
    salida = str(d)
    assert "Dado:" in salida
    assert isinstance(salida, str)
