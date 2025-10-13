import pytest
from core.player import Player

def test_player_init_y_get():
    p = Player("Luchito")
    assert p.get_name() == "Luchito"

def test_player_set_name():
    p = Player("Luchito")
    p.set_name("Lucas")
    assert p.get_name() == "Lucas"

def test_player_repr():
    p = Player("Luchito")
    assert repr(p) == "Player: Luchito"
