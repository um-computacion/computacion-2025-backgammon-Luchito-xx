from ficha import Ficha

class board:
    def __init__(self):
        self.__celdas__ = [[] for _ in range(24)]  # Cada celda es una tupla (jugador, numero de fichas)
        self.__capturas__ = {"O": 0, "X": 0}  # Fichas capturadas


    def inicio(self):
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
        return f"Board: {self.__celdas__}"
    
    def get_celda(self, celdax:int):
        return self.__celdas__[celdax]
    
    def get_board(self):
        def mostrar(lst):
            if not lst:
                return ""
            else:
                return f"{lst[0].get_dueño()}{len(lst)}"
        return [mostrar(celda) for celda in self.__celdas__]
    
    def get_capturas(self):
        return self.__capturas__
    
"""    def mover(self, celda: int, dado: int, jugador:str):
        try:

            if celda < 0 or celda > 23:
                raise ValueError("La celda inicial es invalida.")
            
            #Validar celda origen
            celda_origen = self.__celdas__[celda]  
            if celda_origen == None:
                raise ValueError("No hay ficha en la celda seleccionada.")
            if celda_origen[0] != jugador:
                raise ValueError("La celda no pertenece al jugador.")


            # Calcular celda destino y validar
            new_celda = celda + dado if jugador == "A" else celda - dado
            if new_celda < 0 or new_celda > 23:
                raise ValueError("Movimiento se va del tablero.")
            if new_celda != ("X",0) and self.__celdas__[new_celda][1] >= 2  and self.__celdas__[new_celda][0] != jugador:
                raise ValueError(f"La celda destino esta ocupada por el oponente {self.__celdas__[new_celda][0]}, tiene {self.__celdas__[new_celda][1]} fichas")
            
            # Quitar ficha origen
            if celda_origen[1] <= 1:
                self.__celdas__[celda] = ("X", 0)
            else:
                self.__celdas__[celda] = (jugador, celda_origen[1] - 1)

            # Poner ficha destino
            if self.__celdas__[new_celda] == ("X", 0):
                self.__celdas__[new_celda] = (jugador, 1)

            elif self.__celdas__[new_celda][0] == jugador:
                self.__celdas__[new_celda] = (jugador, self.__celdas__[new_celda][1] + 1)

            else:
                self.__celdas__[new_celda] = (jugador, 1)
                # Falta capturar ficha oponente y poner en barra

        except ValueError as e:
            return str(e)  """
            
        

if __name__ == "__main__":
    b = board()
    b.inicio()
    print(b.get_board(), "\n")
    print(b.get_capturas())