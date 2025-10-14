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
    pass


def test_init_injeccion_dep():
    """
    si inyectar board/players/dice personalizados -> Backgammon las deberia usar :)
    """
    pass


def test_inicio():
    """
    inicio() debe invocar board.inicio(), resetear turno a 0 y limpiar saltos
    """
    pass


# Dados y saltos

def test_tirar_dado():
    """
    tirar_dado() debe llenar __saltos con el resultado de dice.roll() y devolverlo
    """
    pass


def test_tirar_dado_dobles():
    """
    cuando dice devuelve dobles, get_saltos pone 4 de esos
    """
    pass


# Turnos 
def test_get_jugador_y_cambio_turno():
    """
    get_jugador() al inicio devuelve player 0, cambio_turno alterna el turno y limpia saltos.
    """
    pass

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

# Victoria...




