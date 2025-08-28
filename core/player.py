class player:
    def __init__(self, name, direccion, fichas=99):
        self.__name__ = name
        self.__direccion__ = direccion
        self.__fichas__ = fichas
        self.__turno__ = False
        self.__ganador__ = False
    
    def get_name(self):
        return self.__name__
    
    def get_direccion(self):    
        return self.__direccion__
    
    def get_fichas(self):
        return self.__fichas__
    
    def __repr__(self):
        return f"Player: {self.__name__}, Direccion: {self.__direccion__}, Fichas: {self.__fichas__}, Turno: {self.__turno__}, Ganador: {self.__ganador__}"
    
if __name__ == "__main__":
    p = player("Lucho", -1)
    print(p)