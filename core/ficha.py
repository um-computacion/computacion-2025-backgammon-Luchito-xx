class Ficha:

    def __init__(self, jugador: str):
        self.__jugador = jugador
        self.__capturada = False

    def get_jugador(self):
        return self.__jugador

    def set_jugador(self, jugador):
        self.__jugador = jugador
    
    def get_capturada(self):
        return self.__capturada
    
    def set_capturada(self, capturada: bool):
        self.__capturada = capturada
    
    def __repr__(self) -> str:
        estado = "Capturada" if self.__capturada else "Libre"
        return f"Dueño de la ficha es {self.__jugador} y esta {estado}"
    


        
