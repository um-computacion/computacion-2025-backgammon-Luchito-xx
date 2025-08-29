class player:
    def __init__(self, name):
        self.__name__ = name
        self.__fichas_afuera__ = 0 # falta implementar
    
    def get_name(self):
        return self.__name__

    def __repr__(self):
        return f"Player: {self.__name__}"
    
if __name__ == "__main__":
    p = player("Lucho")
    print(p)