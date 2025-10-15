import pytest

from core.backgammon import Backgammon
from core.board import Board
from core.player import Player
from core.dice import Dice
from core import validaciones 


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

    assert b._Backgammon__turno == 0
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



def test_inicio():
    """
    inicio() debe invocar board.inicio(), resetear turno a 0 y limpiar saltos
    """
    b = Backgammon()
    b.tirar_dado() 
    b.cambio_turno()  
    b.inicio()

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
    b.cambio_turno()
    assert b.get_saltos() == [] 



# Turnos 
def test_get_jugador_y_cambio_turno():
    """
    get_jugador() al inicio devuelve player 0, cambio_turno alterna el turno y limpia saltos.
    """
    b = Backgammon()

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

# Mostrar ()
def test_mostrar():
    """
    mostrar() devuelve dict con claves:
      - 'board': str (resultado de board.get_board())
      - 'turno': str (nombre del jugador actual)
      - 'saltos': list (resultado de get_saltos())
      - 'capturas': list (representación de las fichas capturadas)
      - 'ganador': None o Player 
    """
    pass

# Mover...

def test_mover_raises_if_no_saltos():
    '''
    si no hay saltos (no se han tirado dados) mover() debe raise
    '''
    b = Backgammon()
    with pytest.raises(ValueError, match="Tirar dados primero"):
        b.mover(0, 3)

# Victoria...




