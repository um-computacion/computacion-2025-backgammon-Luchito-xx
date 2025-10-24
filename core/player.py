class Player:
    """Clase que representa a un jugador en el juego.
    Atributos:
        __name : str
            Nombre del jugador
    """
    def __init__(self, name):
        self.__name = name
    
    def get_name(self):
        """Obtener el nombre del jugador"""
        return self.__name
    
    def set_name(self, name):
        """Establecer el nombre del jugador"""
        self.__name = name

    def __repr__(self):
        """Representacion del jugador"""
        return f"Player: {self.__name}"
    
