from .board import Board
from .player import Player
from .dice import Dice
from .validaciones import *
from .exceptions import *


class Backgammon:
    """Clase principal del juego de Backgammon.
    Atributos
    __board__ : Board
        Representa el tablero de juego
    __players__ : list[Player]
        Lista de jugadores en el juego
    __dice__ : Dice
        Representa los dados del juego
    __turno__ : int
        Índice del jugador actual en la lista de jugadores
    __saltos__ : list[int]
        Lista de saltos disponibles para el jugador actual
    __ganador__ : Player | None
        Representa al jugador ganador, si lo hay   
    """
    def __init__(self, board=None, players=None, dice=None):
        self.__board__ = board if board else Board()
        self.__players__ = players if players else [Player("X"), Player("O")]
        self.__dice__ = dice if dice else Dice()
        self.__turno__ = None
        self.__saltos__ = []
        self.__ganador__ = None

    def inicio(self):
        """Iniciar el juego de Backgammon"""
        self.__board__.inicio()
        self.__turno__ = None
        self.__saltos__ = []
        self.__ganador__ = None

        print("Seleccion de jugador inicial...")
        self.turno_inicial()
    
    def turno_inicial(self):
        """Determinar el primer jugador que inicia el juego"""
        while True:
            valores = self.__dice__.roll()
            print(f"Dados lanzados: {valores[0]} y {valores[1]}")
            if valores[0] != valores[1]:
                break
            print("Empate, lanzo denuevo")
        
        if valores[0] > valores[1]:
            self.__turno__ = 0
        else:
            self.__turno__ = 1
        
        print(f"El jugador {self.get_jugador().get_name()} juego primero")
    
    def tirar_dado(self):
        """Tirar los dados y obtener los saltos disponibles"""
        self.__saltos__ = self.__dice__.roll()
        return self.__saltos__
    
    def get_saltos(self):
        """Obtener los saltos disponibles para el jugador actual"""
        return list(self.__saltos__)
    
    def get_jugador(self):
        """Obtener el jugador actual"""
        return self.__players__[self.__turno__]
    
    def mover(self, celda, salto):
        """ Realizar un movimiento en el juego de Backgammon """

        # validar estado previo
        if not self.__saltos__:
            raise SaltosError("Debes tirar dados primero")
        
        if salto not in self.__saltos__:
            raise SaltosError(f"Salto {salto} no disponible")
        
        # validar desde validaciones movimiento
        if not Validaciones.movimiento_valido(
            celdas=self.__board__.get_celdas(),
            capturas=self.__board__.get_capturas(),
            celda=celda,
            salto=salto,
            jugador=self.get_jugador().get_name()
        ):
            raise ValueError("Movimiento inválido según las reglas")
        
        # mover desde board
        self.__board__.mover(celda, salto, self.get_jugador().get_name())
        
        # eliminar salto usado
        self.__saltos__.remove(salto)
        
        # ver si victoria
        if Validaciones.validar_victoria(
            self.__board__.get_celdas(), 
            self.__board__.get_capturas(), 
            self.get_jugador().get_name()):
            self.__ganador__ = self.get_jugador()
        
        # cambiar turno si no hay mas saltos
        if not self.__saltos__:
            self.cambio_turno()

    def cambio_turno(self):
        """Cambiar el turno al siguiente jugador"""
        self.__turno__ = 1 - self.__turno__
        self.__saltos__ = []

    def puede_mover(self):
        """Verificar si el jugador actual puede mover"""
        return Validaciones.puede_mover(
            celdas=self.__board__.get_celdas(),
            capturas=self.__board__.get_capturas(),
            saltos=self.__saltos__,
            jugador=self.get_jugador().get_name()
        )

    def mostrar(self):
        """Mostrar el estado actual del juego"""
        return{
            "board": self.__board__.get_board(),
            "turno": self.get_jugador().get_name(),
            "saltos": list(self.__saltos__),
            "capturas":list(self.__board__.get_capturas()),
            "ganador": self.__ganador__.get_name() if self.__ganador__ else None
        }