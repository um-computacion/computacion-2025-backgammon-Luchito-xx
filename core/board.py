"""
Módulo Board - Gestión del tablero de Backgammon.

Contiene la clase Board que maneja el estado del tablero, las posiciones
de las fichas y las operaciones de movimiento, captura y reingreso.
"""

from .ficha import Ficha

class Board:
    """
    class board -> Representa el tablero del juego de backgammon
    
    Atributos
        __celdas__ (list[list[Ficha]]): 24 listas que representan las
            posiciones del tablero. Cada posición contiene fichas apiladas.
        __capturas__ (list[Ficha]): Lista de fichas capturadas en la barra.
    """
    
    def __init__(self):
        """
        Inicializa un tablero vacío de Backgammon.

        Crea 24 posiciones vacías y una lista vacía para fichas capturadas.
        """
        self.__celdas__ = [[] for _ in range(24)]  
        self.__capturas__ = []  


    def inicio(self):
        """    
        Inicializa el tablero con la configuración estándar de Backgammon.

        Coloca las 15 fichas de cada jugador en sus posiciones iniciales
        según las reglas oficiales y limpia las fichas capturadas.
        """
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
        """Representación del tablero como cadena de texto"""
        return f"Board: {self.__celdas__}"
    
    def get_celdas(self):
        """
            Obtiene todas las celdas del tablero.
        Returns:
            list[list[Ficha]]: Lista de 24 posiciones, cada una con sus fichas.
        """
        return self.__celdas__

    def get_capturas(self):
        """
            Obtiene la lista de fichas capturadas en la barra.
        Returns:
            list[Ficha]: Lista de fichas capturadas que deben reingresar.
        """
        return self.__capturas__
    
    def tiene_capturadas(self, jugador:str) -> bool:
        """        
            Verifica si un jugador tiene fichas capturadas en la barra.
        Args:
            jugador (str): Identificador del jugador ('X' o 'O').

        Returns:
            bool: True si el jugador tiene al menos una ficha capturada.
        """
        for ficha in self.__capturas__:
            if ficha.get_jugador() == jugador:
                return True
        return False
    
    def repr_celda(self, celda:list):
        """
            Genera representación corta de una celda del tablero.
        Args:
            celda (list[Ficha]): Lista de fichas en una posición.

        Returns:
            str: Representación compacta (ej: "XXX" para 3 fichas X).
        """
        if not celda:
            return "--"
        jugador = celda[0].get_jugador()
        return f"{jugador * len(celda)}"
    
    def get_board(self):
        """        
            Genera representación visual completa del tablero.
        Returns:
            str: Representación visual del tablero en formato texto.
        """
        def c(i):
            cel = self.__celdas__[i]
            return "--" if not cel else f"{cel[0].get_jugador()}{len(cel)}"

        nums_sup   = " ".join(f"{i:>{3}}" for i in range(12, 24) )
        fichas_sup = " ".join(f"{c(i):>{3}}" for i in range(12, 24))

       
        linea = " " * (4 * 6) + "|"
        barra = (linea + "\n") * 2 + "-" * (4 * 12) + "\n" + linea + "\n" + linea

        nums_inf  = " ".join(f"{i:>{3}}" for i in range(11, -1, -1))
        fichas_inf = " ".join(f"{c(i):>{3}}" for i in range(11, -1, -1))

        cap_x= sum(1 for f in self.__capturas__ if f.get_jugador() == "X")
        cap_o= sum(1 for f in self.__capturas__ if f.get_jugador() == "O")

        if cap_x > 0:
            fichas_sup += f"   Capturadas X: {cap_x}"
        if cap_o > 0:
            fichas_inf += f"   Capturadas O: {cap_o}"

        return "\n".join([nums_sup, fichas_sup, barra, fichas_inf, nums_inf])

    def mover(self, celda, salto, jugador):
        """
        Mueve una ficha en el tablero según las reglas de Backgammon.

        Ejecuta movimientos normales, reingresos desde la barra o salidas
        del tablero. Maneja capturas de fichas enemigas automáticamente.

        Args:
            celda (int): Posición origen (0-23) o -1 para reingreso.
            salto (int): Cantidad de posiciones a avanzar según el dado.
            jugador (str): Identificador del jugador que mueve ('X' o 'O').

        Returns:
            None
        """
        
        # Reingreso de barra
        if celda == -1:
            destino = salto - 1 if jugador == "X" else 24 - salto
            
            # Sacar de capturas
            ficha = None
            for i, f in enumerate(self.__capturas__):
                if f.get_jugador() == jugador:
                    ficha = self.__capturas__.pop(i)
                    ficha.set_capturada(False)
                    break
            
            # Capturar ficha enemiga si hay una sola
            if self.__celdas__[destino] and len(self.__celdas__[destino]) == 1 and self.__celdas__[destino][0].get_jugador() != jugador:
                enemiga = self.__celdas__[destino].pop()
                enemiga.set_capturada(True)
                self.__capturas__.append(enemiga)
            
            # Colocar ficha
            self.__celdas__[destino].append(ficha)
            return
        
        # sacar de tablero
        destino = celda + salto if jugador == "X" else celda - salto

        # Tomar ficha origen
        ficha_sacada = self.__celdas__[celda].pop()

        if destino < 0 or destino > 23:
            return
        
        # movimiento normal 
        # Capturar si hay UNA ficha enemiga
        if self.__celdas__[destino] and len(self.__celdas__[destino]) == 1 and self.__celdas__[destino][0].get_jugador() != jugador:
            enemiga = self.__celdas__[destino].pop()
            enemiga.set_capturada(True)
            self.__capturas__.append(enemiga)
        
        # Colocar ficha sin capturar
        self.__celdas__[destino].append(ficha_sacada)