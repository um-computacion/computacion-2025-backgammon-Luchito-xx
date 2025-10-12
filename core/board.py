from .ficha import Ficha
from .validaciones import *

class Board:
    def __init__(self):
        
        self.__celdas = [[] for _ in range(24)]  
        self.__capturas = []  


    def inicio(self):
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
        return f"Board: {self.__celdas}"
    
    def get_celdas(self):
        return self.__celdas

    def get_capturas(self):
        return self.__capturas
    
    def repr_celda(self, celda:list):
        if not celda:
            return "--"
        jugador = celda[0].get_jugador()
        return f"{jugador * len(celda)}"
    
    def get_board(self):

        def c(i):
            cel = self.__celdas[i]
            return "--" if not cel else f"{cel[0].get_jugador()}{len(cel)}"

        top_idx    = range(12, 24)     
        bottom_idx = range(11, -1, -1)  
        w = 4  # ancho por columna (espaciado)

        top_nums   = " ".join(f"{i+1:>{w-1}}" for i in top_idx)
        top_cells  = " ".join(f"{c(i):>{w-1}}"    for i in top_idx)

        # líneas centrales (dos '|' centradas) y línea de separación
        center_space = " " * (w * 6)   # 12 columnas / 2 = 6
        middle = center_space + "|\n" + center_space + "|\n" + "-" * (w * 12) + "\n"

        bottom_nums  = " ".join(f"{i+1:>{w-1}}" for i in bottom_idx)
        bottom_cells = " ".join(f"{c(i):>{w-1}}"    for i in bottom_idx)

        return "\n".join([top_nums, top_cells, middle, bottom_nums, bottom_cells])

    def validar_movimiento(self, celda:int, salto:int, jugador:str):
        try:
            validar_salida = Validaciones.validar_salida(self.__celdas, self.__capturas, jugador)
            Validaciones.movimiento_valido (self.__celdas, celda, salto, jugador, validar_salida=validar_salida)

            return True
        except Exception:
            return False



    def mover(self, celda:int, salto:int, jugador:str):

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


if __name__ == "__main__":
    b = Board()
    b.inicio()
    print(b.get_board())
    print(b.get_capturas())
