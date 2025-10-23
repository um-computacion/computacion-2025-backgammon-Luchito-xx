import random

class Dice:
    """Clase que representa un par de dados en el juego.
    Atributos:
        __valor__ : list
            Lista que contiene los valores actuales de los dados
    """
    def __init__(self):
        self.__valor__ = [1,1]

    def roll(self):
        """Lanza los dados y actualiza sus valores"""
        self.__valor__ = [random.randint(1, 6), random.randint(1, 6)]
        if self.__valor__[0] == self.__valor__[1]:
            self.__valor__ = [self.__valor__[0]] * 4
            return self.__valor__
        else: 
            return self.__valor__

    def __str__(self):
        """Representacion de los dados"""
        return f"Dado: {self.__valor__}" 
           
    def get_valor(self):
        """Obtiene los valores actuales de los dados"""
        return self.__valor__
