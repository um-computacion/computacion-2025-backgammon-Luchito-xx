from .board import Board
from .player import Player
from .dice import Dice
from .validaciones import *
from .exceptions import *

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
        self.__turno = None
        self.__saltos = []
        self.__ganador = None

    def inicio(self):
        """Iniciar el juego de Backgammon"""
        self.__board.inicio()
        self.__turno = None
        self.__saltos = []
        self.__ganador = None

        print("Seleccion de jugador inicial...")
        self.turno_inicial()
    
    def turno_inicial(self):
        """Determinar el primer jugador que inicia el juego"""
        while True:
            valores = self.__dice.roll()
            print(f"Dados lanzados: {valores[0]} y {valores[1]}")
            if valores[0] != valores[1]:
                break
            print("Empate, lanzo denuevo")
        
        if valores[0] > valores[1]:
            self.__turno = 0
        else:
            self.__turno = 1
        
        print(f"El jugador {self.get_jugador().get_name()} juego primero")
    
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
    
    def mover(self, celda, salto):
        """ Realizar un movimiento en el juego de Backgammon """

        # validar estado previo
        if not self.__saltos:
            raise SaltosError("Debes tirar dados primero")
        
        if salto not in self.__saltos:
            raise SaltosError(f"Salto {salto} no disponible")
        
        # validar desde validaciones movimiento
        if not Validaciones.movimiento_valido(
            celdas=self.__board.get_celdas(),
            capturas=self.__board.get_capturas(),
            celda=celda,
            salto=salto,
            jugador=self.get_jugador().get_name()
        ):
            raise ValueError("Movimiento inválido según las reglas")
        
        # mover desde board
        self.__board.mover(celda, salto, self.get_jugador().get_name())
        
        # eliminar salto usado
        self.__saltos.remove(salto)
        
        # ver si victoria
        if Validaciones.validar_victoria(
            self.__board.get_celdas(), 
            self.__board.get_capturas(), 
            self.get_jugador().get_name()):
            self.__ganador = self.get_jugador()
        
        # cambiar turno si no hay mas saltos
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
            "capturas":list(self.__board.get_capturas()),
            "ganador": self.__ganador.get_name() if self.__ganador else None
        }