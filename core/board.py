from ficha import Ficha

class Board:
    def __init__(self):
        
        self.__celdas = [[] for _ in range(24)]  # Cada celda es una tupla (jugador, numero de fichas)
        self.__capturas = []  # Fichas capturadas


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

        fila_superior = [f"{i:02}:{self.repr_celda(self.__celdas[i])} \n" for i in range(0,12)]

        fila_inferior = [f"{i:02}:{self.repr_celda(self.__celdas[i])} \n" for i in range(12,24)]

        return "".join(fila_superior) + "\n" + "".join(fila_inferior) + "\n" #Poner las fichas capturadas
        
        
    def mover(self, jugador:str, celda:int , saltos:int):
        # Terminar validaciones primero ¿usar def mov_valido primero?

        celda_origen = self.__celdas[celda]
        ficha = celda_origen.pop()

        destino = self.__celdas[saltos + celda]
        
        # Caso destino vacio
        if not destino:
            self.__celdas[saltos + celda].append[ficha] 
            return True
        
        # Caso destino con fichas propias
        if destino[0].get_jugador() == jugador:
            self.__celdas[saltos + celda].append[ficha]
            return True
        # Caso destino con 1 ficha jugador (captura)
        captura = destino.pop()
        captura.capturar()
        self.__capturas.append(captura)
        self.__celdas[saltos + celda].append(ficha)
        pass


if __name__ == "__main__":
    b = Board()
    b.inicio()
    print(b.get_board())
    print(b.get_capturas())