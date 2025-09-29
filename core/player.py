class Player:
    def __init__(self, name):
        self.__name = name
    
    def get_name(self):
        return self.__name

    def __repr__(self):
        return f"Player: {self.__name}"
    
    def set_name(self, name):
        self.__name = name