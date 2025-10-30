"""
Módulo Player - Representación de jugadores.

Contiene la clase Player que representa a cada jugador en el juego
de Backgammon con su identificador único.

Un jugador se identifica por su nombre y participa en el juego
realizando movimientos con sus fichas.
"""

class Player:
    """
    class Player: Representa a un jugador en el juego de Backgammon.

    Atributos:
        __name__ (str): Identificador del jugador.
    
    """
    def __init__(self, name):
        """        
            Inicializa un nuevo jugador con su identificador.
        Args:
            name (str): Identificador del jugador ('X' o 'O').
        """
        self.__name__ = name
    
    def get_name(self):
        """
            Obtiene el identificador del jugador.
        Returns:
            str: Nombre/identificador del jugador.
        """
        return self.__name__
    
    def set_name(self, name):
        """
            Establece un nuevo identificador para el jugador.
        Args:
            name (str): Nuevo identificador del jugador.
        """
        self.__name__ = name