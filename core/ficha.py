"""
Módulo Ficha - Representación de fichas del juego.

Define la clase Ficha que representa cada pieza en el tablero de Backgammon,
incluyendo su propietario y estado de captura.

Una ficha pertenece a un jugador específico y puede estar en el tablero
o capturada en la barra. 
"""

class Ficha:
    """  
    class Ficha: Representa una ficha individual en el tablero de Backgammon.

    Atributos
        __jugador__ (str): Identificador del jugador propietario ('X' o 'O').
        __capturada__ (bool): True si está en la barra, False si está en juego.

    """

    def __init__(self, jugador: str):
        """ 
            Inicializa una nueva ficha para un jugador.
        Crea una ficha en estado libre (no capturada) perteneciente
        al jugador especificado.

        Args:
            jugador (str): Identificador del jugador propietario ('X' o 'O').
        """
        
        self.__jugador__ = jugador
        self.__capturada__ = False

    def get_jugador(self) -> str:
        """        
            Obtiene el identificador del jugador propietario de la ficha.
        Returns:
            str: Identificador del jugador ('X' o 'O').
        """

        return self.__jugador__

    def set_jugador(self, jugador: str) -> None:
        """
            Establece el jugador propietario de la ficha.
        Args:
            jugador (str): Nuevo identificador del jugador ('X' o 'O').

        """
        self.__jugador__ = jugador

    def is_capturada(self) -> bool:
        """        
            Verifica si la ficha está capturada en la barra.
        Returns:
            bool: True si está en la barra, False si está en el tablero.
        """
        return self.__capturada__

    def set_capturada(self, capturada: bool = True) -> None:
        """       
            Establece el estado de captura de la ficha.
        Args:
            capturada (bool, optional): True para marcar como capturada,
                False para liberar. Por defecto True.
        """
        self.__capturada__ = bool(capturada)

    def __repr__(self) -> str:
        """
            Representación técnica de la ficha para debugging.
        Returns:
            str: Cadena en formato '<Ficha jugador=X estado>'.
        """
        estado = "capturada" if self.__capturada__ else "libre"
        return f"<Ficha jugador={self.__jugador__} {estado}>"
    

        
