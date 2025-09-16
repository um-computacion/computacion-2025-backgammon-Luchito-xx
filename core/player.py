class Player:
    def __init__(self, name):
        self.__name = name
        self.__fichas_afuera = 0 # falta implementar
    
    def get_name(self):
        return self.__name

    def __repr__(self):
        return f"Player: {self.__name}"
    
if __name__ == "__main__":
    p = Player("Lucho")
    print(p)
