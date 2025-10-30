from .ficha import Ficha
from .validaciones import *

class Board:
    """
    class board -> Representa el tablero del juego de backgammon
    
    Atributos
    __celdas__ : list
        Lista de listas que representan las celdas del tablero y las fichas en cada cel
    
    __capturas__ : list
        Lista de fichas capturadas (en la barra)
    """
    
    def __init__(self):
      
        self.__celdas__ = [[] for _ in range(24)]  
        self.__capturas__ = []  


    def inicio(self):
        """    Inicializa el tablero con la configuración inicial de fichas"""
        self.__celdas__ = [[] for _ in range(24)]
        self.__capturas__ = []

        self.__celdas__[0] = [Ficha ("X") for _ in range(2)]
        self.__celdas__[11] = [Ficha ("X") for _ in range(5)]
        self.__celdas__[16] = [Ficha ("X") for _ in range(3)]
        self.__celdas__[18] = [Ficha ("X") for _ in range(5)]

        self.__celdas__[23] = [Ficha ("O") for _ in range(2)]             
        self.__celdas__[12] = [Ficha ("O") for _ in range(5)]
        self.__celdas__[7] = [Ficha ("O") for _ in range(3)]
        self.__celdas__[5] = [Ficha ("O") for _ in range(5)]

             
    def __str__(self):
        """Representación del tablero como cadena de texto"""
        return f"Board: {self.__celdas__}"
    
    def get_celdas(self):
        """Devuelve las celdas del tablero"""
        return self.__celdas__

    def get_capturas(self):
        """Devuelve las fichas capturadas (en la barra)"""
        return self.__capturas__
    
    def tiene_capturadas(self, jugador:str) -> bool:
        """Verifica si un jugador tiene fichas capturadas"""
        for ficha in self.__capturas__:
            if ficha.get_jugador() == jugador:
                return True
        return False
    
    def repr_celda(self, celda:list):
        """Representación corta de una celda del tablero"""
        if not celda:
            return "--"
        jugador = celda[0].get_jugador()
        return f"{jugador * len(celda)}"
    
    def get_board(self):
        """Representación visual del tablero"""
        def c(i):
            cel = self.__celdas__[i]
            return "--" if not cel else f"{cel[0].get_jugador()}{len(cel)}"

        nums_sup   = " ".join(f"{i:>{3}}" for i in range(12, 24) )
        fichas_sup = " ".join(f"{c(i):>{3}}" for i in range(12, 24))

       
        linea = " " * (4 * 6) + "|"
        barra = (linea + "\n") * 2 + "-" * (4 * 12) + "\n" + linea + "\n" + linea

        nums_inf  = " ".join(f"{i:>{3}}" for i in range(11, -1, -1))
        fichas_inf = " ".join(f"{c(i):>{3}}" for i in range(11, -1, -1))

        cap_x= sum(1 for f in self.__capturas__ if f.get_jugador() == "X")
        cap_o= sum(1 for f in self.__capturas__ if f.get_jugador() == "O")

        if cap_x > 0:
            fichas_sup += f"   Capturadas X: {cap_x}"
        if cap_o > 0:
            fichas_inf += f"   Capturadas O: {cap_o}"

        return "\n".join([nums_sup, fichas_sup, barra, fichas_inf, nums_inf])

    def mover(self, celda, salto, jugador):
        """Mueve una ficha en el tablero (reingreso, salida o movimiento normal)"""
        
        # Reingreso de barra
        if celda == -1:
            destino = salto - 1 if jugador == "X" else 24 - salto
            
            # Sacar de capturas
            ficha = None
            for i, f in enumerate(self.__capturas__):
                if f.get_jugador() == jugador:
                    ficha = self.__capturas__.pop(i)
                    ficha.set_capturada(False)
                    break
            
            # Capturar ficha enemiga si hay una sola
            if self.__celdas__[destino] and len(self.__celdas__[destino]) == 1 and self.__celdas__[destino][0].get_jugador() != jugador:
                enemiga = self.__celdas__[destino].pop()
                enemiga.set_capturada(True)
                self.__capturas__.append(enemiga)
            
            # Colocar ficha
            self.__celdas__[destino].append(ficha)
            return
        
        # sacar de tablero
        destino = celda + salto if jugador == "X" else celda - salto

        # Tomar ficha origen
        ficha_sacada = self.__celdas__[celda].pop()

        if destino < 0 or destino > 23:
            return
        
        # movimiento normal 
        # Capturar si hay UNA ficha enemiga
        if self.__celdas__[destino] and len(self.__celdas__[destino]) == 1 and self.__celdas__[destino][0].get_jugador() != jugador:
            enemiga = self.__celdas__[destino].pop()
            enemiga.set_capturada(True)
            self.__capturas__.append(enemiga)
        
        # Colocar ficha sin capturar
        self.__celdas__[destino].append(ficha_sacada)
