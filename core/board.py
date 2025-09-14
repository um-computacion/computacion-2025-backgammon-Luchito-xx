from ficha import Ficha

class Board:
    def __init__(self):
        
        self.__celdas = [[] for _ in range(24)]  # Cada celda es una tupla (jugador, numero de fichas)
        self.__capturas = {"O": 0, "X": 0}  # Fichas capturadas


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
    
    
    def get_celda(self, celdax:int):
        return self.__celdas[celdax]
    
    def get_board(self):
        fila_superior = []
        fila_inferior = []
        
        for i in reversed(range(12)):
            celda = self.__celdas[i]
            if celda:
                fichas = "".join([f.get_jugador() for f in celda])
            else:
                fichas = "-"
            fila_superior.append(f"{i}:{fichas}")

        for i in range(12, 24):
            celda = self.__celdas[-(i-12)]
            if celda:
                fichas = "".join([f.get_jugador() for f in celda])
            else:
                fichas = "-"
            fila_inferior.append(f"{i}:{fichas}")
        return fila_superior, fila_inferior
    
    def get_capturas(self):
        return self.__capturas
        
        

if __name__ == "__main__":
    b = Board()
    b.inicio()
    fila_sup, fila_inf = b.get_board()
    print(" ".join(fila_sup))
    print(" ".join(fila_inf))
    print(b.get_capturas())