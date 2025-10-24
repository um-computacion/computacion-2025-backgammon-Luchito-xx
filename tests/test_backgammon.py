import pytest

from core.backgammon import Backgammon
from core.board import Board
from core.player import Player
from core.dice import Dice
from core.exceptions import *
from core import validaciones 

# Fake Dice para controlar resultados en tests
class FakeDice:
    def __init__(self, rolls):
        # rolls: lista de listas [a,b] que roll() devolverá secuencialmente
        self._rolls = list(rolls)
    def roll(self):
        if not self._rolls:
            return [1, 2]
        return self._rolls.pop(0)
    
# inicialización

def test_init():
    """
    si inicializo sin parametros, Backgammon debe:
      - crear Board por defecto
      - crear dos Players con nombres X y O
      - crear Dice por defecto
      - turno inicial 0 saltos vacios ganador None
    """

    b = Backgammon()

    assert isinstance(b._Backgammon__board, Board)
    assert isinstance(b._Backgammon__players, list)
    assert isinstance(b._Backgammon__players[0], Player)
    assert isinstance(b._Backgammon__dice, Dice)

    assert b._Backgammon__turno == None
    assert b.get_saltos() == []
    assert b._Backgammon__ganador is None

def test_init_injeccion_dep():

    """
    si inyectar board/players/dice personalizados -> Backgammon las deberia usar :)
    """
    board = Board()
    players = [Player("A"), Player("B")]
    dice = Dice()

    b = Backgammon(board=board, players=players, dice=dice)
    assert b._Backgammon__board is board
    assert b._Backgammon__players is players
    assert b._Backgammon__dice is dice



def test_inicio(monkeypatch):
    """
    inicio() debe invocar board.inicio(), resetear turno a 0 y limpiar saltos
    """
    class FakeDice:
        def roll(self):
            return [6, 1]  

    b = Backgammon(dice=FakeDice())
    setattr(b, "_Backgammon__turno", 1)
    setattr(b, "_Backgammon__saltos", [2])

    called = []
    monkeypatch.setattr(b._Backgammon__board, "inicio", lambda: called.append(True))

    b.inicio()

    assert called == [True]
    assert b._Backgammon__turno == 0
    assert b.get_saltos() == []



# Dados y saltos

def test_tirar_dado():
    """
    tirar_dado() debe llenar __saltos (con logica de dobles tambien) con el resultado de dice.roll() y devolverlo
    """
    b = Backgammon()
    saltos = b.tirar_dado()
    assert saltos == b.get_saltos()
    assert isinstance(saltos, list)
    assert all(isinstance(s, int) for s in saltos)
    assert all(1 <= s <= 6 for s in saltos)
    assert 1 <= len(saltos) <= 4 


def test_get_saltos():
    """
    get_saltos() devuelve la lista de saltos actual (inicialmente vacia)
    """
    b = Backgammon()
    assert b.get_saltos() == []
    saltos = b.tirar_dado()
    assert b.get_saltos() == saltos
    b.turno_inicial()
    b.cambio_turno()
    assert b.get_saltos() == [] 



# Turnos 

def test_turno_inicial_X(capsys):
    dice = FakeDice([[5, 3]])
    g = Backgammon(dice=dice)
    g.turno_inicial()
    assert g._Backgammon__turno == 0
    assert g.get_jugador().get_name() == "X"
    out = capsys.readouterr().out
    assert "Dados lanzados" in out

def test_turno_inicial_O(capsys):
    dice = FakeDice([[2, 4]])
    g = Backgammon(dice=dice)
    g.turno_inicial()
    assert g._Backgammon__turno == 1
    assert g.get_jugador().get_name() == "O"

def test_turno_inicial_empate(capsys):
    dice = FakeDice([[3, 3], [6, 1]])
    g = Backgammon(dice=dice)
    g.turno_inicial()
    assert g._Backgammon__turno == 0  
    out = capsys.readouterr().out
    assert "Empate" in out

def test_get_jugador_y_cambio_turno():
    """
    get_jugador() devuelve el jugador actual, cambio_turno alterna el turno y limpia saltos.
    """

    b = Backgammon()
    setattr(b, "_Backgammon__turno", 0)

    j0 = b.get_jugador()
    assert isinstance(j0, Player)
    assert j0.get_name() == "X"
    assert b.get_saltos() == []

    b.cambio_turno()
    assert b.get_saltos() == []
    assert b.get_jugador().get_name() == "O"

    b.cambio_turno()
    assert b.get_jugador().get_name() == "X"
    assert b.get_saltos() == []


# Mover...

def test_mover_invoca_board_y_consumo_salto(monkeypatch):
    """
    mover() debe invocar board.mover(...) si la validacion lo permite
    y consumir el salto utilizado.
    """
    b = Backgammon()
    setattr(b, "_Backgammon__turno", 0)
    setattr(b, "_Backgammon__saltos", [3])

    called = []
    def fake_board_mover(celda, salto, jugador):
        called.append((celda, salto, jugador))

    # parchear el board del objeto
    b._Backgammon__board.mover = fake_board_mover
    # forzar validacion positiva
    monkeypatch.setattr(validaciones.Validaciones, "movimiento_valido", lambda *args, **kwargs: True)

    b.mover(5, 3)

    assert called == [(5, 3, "X")]
    assert b.get_saltos() == []




