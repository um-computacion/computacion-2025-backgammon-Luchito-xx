class Ficha:
    """  
    class ficha -> Representa una ficha del tablero
    
    Atributos
    __jugador__ : str
        Identificador del jugador dueño de la ficha ('X' o 'O')
    __capturada : bool
        Indica si la ficha esta en la barra (capturada)
    """

    def __init__(self, jugador: str):
        self.__jugador__ = jugador
        self.__capturada = False

    def get_jugador(self) -> str:
        """Obtener el jugador dueño de la ficha"""
        return self.__jugador__

    def set_jugador(self, jugador: str) -> None:
        """Establecer el jugador dueño de la ficha"""
        self.__jugador__ = jugador

    def is_capturada(self) -> bool:
        """Verificar si la ficha esta capturada"""
        return self.__capturada

    def set_capturada(self, capturada: bool = True) -> None:
        """Establecer el estado de captura de la ficha"""
        self.__capturada = bool(capturada)

    def __repr__(self) -> str:
        """Representacion de la ficha"""
        estado = "capturada" if self.__capturada else "libre"
        return f"<Ficha jugador={self.__jugador__} {estado}>"

        
