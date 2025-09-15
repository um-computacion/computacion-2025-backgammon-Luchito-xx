from board import Board
from player import Player
from dice import Dice

''' 
    Controlador del juego
    
    Que hace: 
        - Manejar jugadores, tablero, dados... Con el fin de ejecutar logica del juego
        - Facilitar manejo para el CLI y algunas pruebas

    Posibles atributos
        - __board
        - __player
        - __turno
        - __dice
        - __validacion

    Metodos a aplicar:
        - constructor __init__
        - inicio()
        - roll_dice()
        - validar_movimiento()
        - mover()
        - victoria()
         
'''

class Backgammon:
    def __init__(self, board: Board, players: list, dice: Dice):
        self.__board = Board()
        self.__players = [Player("X"), Player("O")]
        self.__dice = Dice()
        self.__turno = 0
        self.__movimientos = []

    def inicio(self):
        self.__board.inicio()
        self.__turno = 0
        self.__movimientos = []
    
    def tirar_dado(self):
        self.__movimientos = self.__dice.roll()
        return self.__movimientos
    
    def get_saltos(self):
        return list(self.__movimientos)
    
    def get_jugador(self):
        return self.__players[self.__turno]
    
    def mover(self, celda:int, saltos:int, jugador:str):

        # Como  manejar movimientos?
        # cambiar turno cuando no queden mas

        pass

    def cambio_turno(self):
        pass



    

        
    
    


