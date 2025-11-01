"""
Módulo Backgammon - Lógica principal del juego.

Coordina el flujo del juego de Backgammon, integrando el tablero, jugadores,
dados y validaciones para ejecutar partidas completas, reglas de juego
flujo de turnos, movimientos y condiciones de victoria.
"""

from .board import Board
from .player import Player
from .dice import Dice
from .validaciones import Validaciones
from .exceptions import SaltosError

class Backgammon:
    """
    class Backgammon:  Clase principal que coordina el juego de Backgammon.

    Atributos
        __board__ (Board): Instancia del tablero de juego.
        __players__ (list[Player]): Lista de 2 jugadores.
        __dice__ (Dice): Instancia de los dados del juego.
        __turno__ (int): Índice del jugador actual (0 o 1).
        __saltos__ (list[int]): Movimientos disponibles del dado actual.
        __ganador__ (Player|None): Jugador ganador o None si no hay.
    """
    def __init__(self, board=None, players=None, dice=None):
        """
        Inicializa una nueva partida de Backgammon.
        Args:
            board (Board, optional): Tablero personalizado. Por defecto None.
            players (list[Player], optional): Lista de jugadores. Default None.
            dice (Dice, optional): Dados personalizados. Por defecto None.
        Note:
            Si no se especifican parámetros, se crean con valores por defecto.

        """
        self.__board__ = board if board else Board()
        self.__players__ = players if players else [Player("X"), Player("O")]
        self.__dice__ = dice if dice else Dice()
        self.__turno__ = None
        self.__saltos__ = []
        self.__ganador__ = None

    def inicio(self):
        """
        Inicializa el juego de Backgammon.
        Configura el tablero, resetea el estado del juego y determina
        el jugador inicial mediante lanzamiento de dados.
        """
        self.__board__.inicio()
        self.__turno__ = None
        self.__saltos__ = []
        self.__ganador__ = None

        return self.turno_inicial()

    def turno_inicial(self):
        """Determinar el primer jugador que inicia el juego"""
        while True:
            valores = self.__dice__.roll()

            if valores[0] != valores[1]:

                if valores[0] > valores[1]:
                    self.__turno__ = 0
                else:
                    self.__turno__ = 1

                return {
                    "dados_x": valores[0],
                    "dados_o": valores[1],
                    "ganador": self.get_jugador().get_name()
                }

    def tirar_dado(self):
        """
        Lanza los dados y obtiene los saltos disponibles.
        Returns:
            list[int]: Lista de movimientos disponibles (2 o 4 valores).
        """
        self.__saltos__ = self.__dice__.roll()
        return self.__saltos__

    def get_saltos(self):
        """
        Obtiene los saltos disponibles para el jugador actual.
        Returns:
            list[int]: Copia de la lista de movimientos disponibles.
        """
        return list(self.__saltos__)

    def get_jugador(self):
        """
        Obtiene el jugador actual en turno.
        Returns:
            Player: Instancia del jugador en turno.
        """
        return self.__players__[self.__turno__]

    def get_board(self):
        """
        Obtiene el tablero actual del juego.
        Returns:
            Board: Instancia del tablero de juego.
        """
        return self.__board__

    def get_celdas(self):
        """
        Obtiene las celdas actuales del tablero de Backgammon.

        Returns:
            list[list[Ficha]]: Lista de 24 posiciones del tablero,
            donde cada posición contiene las fichas que se encuentran en ella.
        """
        return self.__board__.get_celdas()


    def get_capturas(self):
        """
        Obtiene las fichas capturadas actualmente en el tablero.

        Returns:
            dict[str, list[Ficha]]: Diccionario con las fichas capturadas
            por cada jugador, usando identificador como clave.
        """
        return self.__board__.get_capturas()

    def mover(self, celda, salto):
        """
        Realiza un movimiento en el juego de Backgammon.
        Valida reglas con modulo Validaciones, mueve con modulo Board
        consume dado usado y verifica victoria.
        Args:
            celda (int): Posición origen (0-23) o -1 para reingreso.
            salto (int): Valor del dado a usar (1-6).
        """

        # validar estado previo
        if not self.__saltos__:
            raise SaltosError("Debes tirar dados primero")

        if salto not in self.__saltos__:
            raise SaltosError(f"Salto {salto} no disponible")

        # validar desde validaciones movimiento
        if not Validaciones.movimiento_valido(
            celdas=self.__board__.get_celdas(),
            capturas=self.__board__.get_capturas(),
            celda=celda,
            salto=salto,
            jugador=self.get_jugador().get_name()
        ):
            raise ValueError("Movimiento inválido según las reglas")

        # mover desde board
        self.__board__.mover(celda, salto, self.get_jugador().get_name())

        # eliminar salto usado
        self.__saltos__.remove(salto)

        # ver si victoria
        if Validaciones.validar_victoria(
            self.__board__.get_celdas(),
            self.__board__.get_capturas(),
            self.get_jugador().get_name()):
            self.__ganador__ = self.get_jugador()

        # cambiar turno si no hay mas saltos
        if not self.__saltos__:
            self.cambio_turno()

    def cambio_turno(self):
        """
        Cambia el turno al siguiente jugador (alterna)
        """
        self.__turno__ = 1 - self.__turno__
        self.__saltos__ = []

    def puede_mover(self):
        """
        Verifica si el jugador actual puede realizar algún movimiento.
        Returns:
            bool: True si existe al menos un movimiento válido.
        """
        return Validaciones.puede_mover(
            celdas=self.__board__.get_celdas(),
            capturas=self.__board__.get_capturas(),
            saltos=self.__saltos__,
            jugador=self.get_jugador().get_name()
        )

    def mostrar(self):
        """
        Obtiene el estado completo actual del juego.
        Información tablero, turno actual, dados disponibles,
        fichas capturadas y ganador.
        Returns:
            dict: Diccionario:
                - 'board' (str): Representación visual del tablero
                - 'turno' (str): Nombre del jugador actual
                - 'saltos' (list[int]): Movimientos disponibles
                - 'capturas' (list[Ficha]): Fichas en la barra
                - 'ganador' (str|None): Nombre del ganador o None
        """
        return{
            "board": self.__board__.get_board(),
            "turno": self.get_jugador().get_name(),
            "saltos": list(self.__saltos__),
            "capturas":list(self.__board__.get_capturas()),
            "ganador": self.__ganador__.get_name() if self.__ganador__ else None
        }
