from .board import Board
from .player import Player
from .dice import Dice
from .validaciones import *

class Backgammon:
    """Clase principal del juego de Backgammon.
    Atributos
    __board : Board
        Representa el tablero de juego
    __players : list[Player]
        Lista de jugadores en el juego
    __dice : Dice
        Representa los dados del juego
    __turno : int
        Índice del jugador actual en la lista de jugadores
    __saltos : list[int]
        Lista de saltos disponibles para el jugador actual
    __ganador : Player | None
        Representa al jugador ganador, si lo hay   
    """
    def __init__(self, board=None, players=None, dice=None):
        self.__board = board if board else Board()
        self.__players = players if players else [Player("X"), Player("O")]
        self.__dice = dice if dice else Dice()
        self.__turno = 0
        self.__saltos = []
        self.__ganador = None

    def inicio(self):
        """Iniciar el juego de Backgammon"""
        self.__board.inicio()
        self.__turno = 0
        self.__saltos = []
    
    def tirar_dado(self):
        """Tirar los dados y obtener los saltos disponibles"""
        self.__saltos = self.__dice.roll()
        return self.__saltos
    
    def get_saltos(self):
        """Obtener los saltos disponibles para el jugador actual"""
        return list(self.__saltos)
    
    def get_jugador(self):
        """Obtener el jugador actual"""
        return self.__players[self.__turno]

    def mover(self, celda:int, salto:int):
        """Mover una ficha en el tablero"""
        if not self.__saltos:
            raise ValueError("Tirar dados primero")
        
        try:
            i = self.__saltos.index(salto)
        except ValueError:
            raise ValueError(f"No hay un salto pendiente igual a {salto}")

        self.__saltos.pop(i)

        jugador = self.get_jugador()

        self.__board.mover(celda, salto, jugador.get_name())


        if Validaciones.validar_victoria(self.__board.get_celdas(),self.__board.get_capturas(), jugador): #?? porque jugador no es un str
            self.__ganador = jugador

        if not self.__saltos:
            self.cambio_turno()
    


    def cambio_turno(self):
        """Cambiar el turno al siguiente jugador"""
        self.__turno = 1 - self.__turno
        self.__saltos = []


    def mostrar(self):
        """Mostrar el estado actual del juego"""
        return{
            "board": self.__board.get_board(),
            "turno": self.get_jugador().get_name(),
            "saltos": list(self.__saltos),
            "capturas":[(ficha.get_jugador() for ficha in self.__board.get_capturas())],
            "ganador": self.__ganador
        }