from exceptions import PosicionInvalidaError

class board:
    def __init__(self):
        self.__celdas__ = [0] * 24

    def inicio(self):
        for i in range(self.__celdas__.__len__()):
            if i > 0 and i < 6:
                self.__celdas__[i] = 1
            elif i > 17 and i < 23:
                self.__celdas__[i] = 2
                
    def __str__(self):
        return f"Board: {self.__celdas__}"
    
    def get_pos(self, pos):
        return self.__celdas__[pos]
    
    def get_board(self):
        return self.__celdas__
    
    def mover(self, celda, dado):
        try:
            if celda < 0 or celda > 23:
                raise PosicionInvalidaError("La celda inicial es inválida.")
        
            ficha = self.__celdas__[celda]    
            if ficha != 0:
                self.__celdas__[celda] = self.__celdas__[celda+dado]
                self.__celdas__[celda+dado] = ficha
                return self.__celdas__
        except PosicionInvalidaError as e:
            return str(e) 
            
        

if __name__ == "__main__":
    b = board()
    b.inicio()
    print(b)
    print(b.mover(1, 3))
    print(b.mover(1, 1231))