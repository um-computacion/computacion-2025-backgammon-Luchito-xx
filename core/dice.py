"""
Módulo Dice - Gestión de dados del juego.

Contiene la clase Dice que maneja el lanzamiento de dados para
determinar los movimientos disponibles en cada turno de Backgammon.
"""

import random

class Dice:
    """
    class Dice: Representa un par de dados en el juego.
    Atributos:
        __valor__ (list[int]): Lista con los valores actuales de los dados.
    """
    def __init__(self):
        """        
        Inicializa un par de dados con valores por defecto.
        """
        self.__valor__ = [1,1]

    def roll(self):
        """        
            Lanza los dados y genera valores aleatorios
        Returns:
            list[int]: Lista con 2 valores o 4 valores si son iguales. 
        """
        self.__valor__ = [random.randint(1, 6), random.randint(1, 6)]
        if self.__valor__[0] == self.__valor__[1]:
            self.__valor__ = [self.__valor__[0]] * 4
            return self.__valor__
        else: 
            return self.__valor__

    def __str__(self):
        """        
            Representación legible de los dados.
        Returns:
            str: Cadena describiendo los valores actuales de los dados."""
        return f"Dado: {self.__valor__}" 
           
    def get_valor(self):
        """        
            Obtiene los valores actuales de los dados.
        Returns:
            list[int]: Lista con los valores de los dados desde el último roll().
        """
        return self.__valor__