import random

class Dice:
    def __init__(self):
        self.__valor__ = [1,1]

    def roll(self):
        self.__valor__ = [random.randint(1, 6), random.randint(1, 6)]
        if self.__valor__[0] == self.__valor__[1]:
            self.__valor__ = [self.__valor__[0]] * 4
            return self.__valor__
        else: 
            return self.__valor__

    def __str__(self):
        return f"Dado: {self.__valor__}" 
           
    def get_valor(self):
        return self.__valor__
