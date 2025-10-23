from .ficha import Ficha
from .validaciones import *

class Board:
    """
    class board -> Representa el tablero del juego de backgammon
    
    Atributos
    __celdas : list
        Lista de listas que representan las celdas del tablero y las fichas en cada cel
    
    __capturas : list
        Lista de fichas capturadas (en la barra)
    """
    
    def __init__(self):
      
        self.__celdas = [[] for _ in range(24)]  
        self.__capturas = []  


    def inicio(self):
        """    Inicializa el tablero con la configuración inicial de fichas"""
        self.__celdas = [[] for _ in range(24)]
        self.__capturas = []

        self.__celdas[0] = [Ficha ("X") for _ in range(2)]
        self.__celdas[11] = [Ficha ("X") for _ in range(5)]
        self.__celdas[16] = [Ficha ("X") for _ in range(3)]
        self.__celdas[18] = [Ficha ("X") for _ in range(5)]

        self.__celdas[23] = [Ficha ("O") for _ in range(2)]             
        self.__celdas[12] = [Ficha ("O") for _ in range(5)]
        self.__celdas[7] = [Ficha ("O") for _ in range(3)]
        self.__celdas[5] = [Ficha ("O") for _ in range(5)]

             
    def __str__(self):
        """Representación del tablero como cadena de texto"""
        return f"Board: {self.__celdas}"
    
    def get_celdas(self):
        """Devuelve las celdas del tablero"""
        return self.__celdas

    def get_capturas(self):
        """Devuelve las fichas capturadas (en la barra)"""
        return self.__capturas
    
    def repr_celda(self, celda:list):
        """Representación corta de una celda del tablero"""
        if not celda:
            return "--"
        jugador = celda[0].get_jugador()
        return f"{jugador * len(celda)}"
    
    def get_board(self):
        """Representación visual del tablero"""
        def c(i):
            cel = self.__celdas[i]
            return "--" if not cel else f"{cel[0].get_jugador()}{len(cel)}"

        nums_sup   = " ".join(f"{i+1:>{3}}" for i in range(12, 24) )
        fichas_sup  = " ".join(f"{c(i):>{3}}" for i in range(23, 11, -1))

       
        linea = " " * (4 * 6) + "|"
        barra = (linea + "\n") * 2 + "-" * (4 * 12) + "\n" + linea + "\n" + linea

        nums_inf  = " ".join(f"{i+1:>{3}}" for i in range(11, -1, -1))
        fichas_inf = " ".join(f"{c(i):>{3}}" for i in range(11, -1, -1))

        return "\n".join([nums_sup, fichas_sup, barra, fichas_inf, nums_inf])

    
    def validar_movimiento(self, celda:int, salto:int, jugador:str):
        """Valida si un movimiento es posible"""
        try:
            validar_salida = Validaciones.validar_salida(self.__celdas, self.__capturas, jugador)
            Validaciones.movimiento_valido (self.__celdas, celda, salto, jugador, validar_salida=validar_salida)

            return True
        except Exception:
            return False



    def mover(self, celda:int, salto:int, jugador:str):
        """Realiza un movimiento en el tablero"""
        #Validar
        validar_salida = Validaciones.validar_salida(self.__celdas, self.__capturas, jugador)
        destino = Validaciones.movimiento_valido(self.__celdas, celda, salto, jugador, validar_salida = validar_salida)
        
        #Sacar de tablero
        if destino is None:
            if Validaciones.validar_movimiento_salida(self.__celdas, self.__capturas, celda, salto, jugador):
                celda_origen = self.__celdas[celda]
                ficha_sacada = celda_origen.pop()
                
                return True
            else: 
                raise FueraDeRangoError("No se pueden sacar fichas del tablero")
            
        
        celda_origen = self.__celdas[celda]
        ficha_sacada = celda_origen.pop()

        dst = self.__celdas[destino]
        
        # Dentro de tablero
        if not dst:
            self.__celdas[destino].append(ficha_sacada)
            return True
        
        #Ficha propia
        if dst[0].get_jugador() == jugador:
            self.__celdas[destino].append(ficha_sacada)
            return True
        
        # Captura ficha
        capturada = dst.pop()
        capturada.set_capturada()
        self.__celdas[destino].append(ficha_sacada)

        return True
