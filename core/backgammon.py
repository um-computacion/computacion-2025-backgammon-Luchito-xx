from board import Board
from player import Player
from dice import Dice
from validaciones import *

class Backgammon:
    def __init__(self, board: Board, players: list, dice: Dice):
        self.__board = Board()
        self.__players = [Player("X"), Player("O")]
        self.__dice = Dice()
        self.__turno = 0
        self.__saltos = []
        self.__ganador = None

    def inicio(self):
        self.__board.inicio()
        self.__turno = 0
        self.__saltos = []
    
    def tirar_dado(self):
        self.__saltos = self.__dice.roll()
        return self.__saltos
    
    def get_saltos(self):
        return list(self.__saltos)
    
    def get_jugador(self):
        return self.__players[self.__turno]

    def mover(self, celda:int, salto:int):
        
        if not self.__saltos:
            raise ValueError("Tirar dados primero")
        
        try:
            i = self.__saltos.index(salto)
        except ValueError:
            raise ValueError(f"No hay un salto pendiente igual a {salto}")

        self.__saltos.pop(i)

        jugador = self.get_jugador()

        self.__board.mover(celda, salto, jugador) #????


        if Validaciones.validar_victoria(self.__board.get_celdas(),self.__board.get_capturas(), jugador): #?? porque jugador no es un str
            self.__ganador = jugador

        if not self.__saltos:
            self.cambio_turno()


    def cambio_turno(self):
        self.__turno = 1 - self.__turno
        self.__saltos = []



    

        
    