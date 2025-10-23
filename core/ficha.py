class Ficha:
    """  
    class ficha -> Representa una ficha del tablero
    
    Atributos
    __jugador : str
        Identificador del jugador dueño de la ficha ('X' o 'O')
    __capturada : bool
        Indica si la ficha esta en la barra (capturada)

    Métodos
    __init__(jugador: str):
        Crea una ficha para el jugador indicado

    get_jugador():
        Devuelve el identificador del jugador dueño de la ficha

    set_jugador(jugador: str):
        Asigna o actualiza el jugador dueño de la ficha

    is_capturada(): 
        Indica si la ficha está capturada (en la barra)

    set_capturada(capturada: bool = True):
        Marca o desmarca la ficha como capturada

    __repr__():
        Representación corta
    """

    def __init__(self, jugador: str):
        """Crear una ficha para el jugador indicado"""
        self.__jugador = jugador
        self.__capturada = False

    def get_jugador(self) -> str:
        return self.__jugador

    def set_jugador(self, jugador: str) -> None:
        self.__jugador = jugador

    def is_capturada(self) -> bool:
        return self.__capturada

    def set_capturada(self, capturada: bool = True) -> None:
        self.__capturada = bool(capturada)

    def __repr__(self) -> str:
        estado = "capturada" if self.__capturada else "libre"
        return f"<Ficha jugador={self.__jugador} {estado}>"

        
