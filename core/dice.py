import random

class Dice:
    def __init__(self):
        self.__valor__ = 1

    def roll(self):
        self.__valor__ = random.randint(1, 6)
        return self.__valor__
    
    def __str__(self):
        return f"Dado: {self.__valor__}" 
           
    def get_valor(self):
        return self.__valor__

if __name__ == "__main__":
    d = Dice()
    print(d.roll()) 
    print(d.get_valor())
    print(d)