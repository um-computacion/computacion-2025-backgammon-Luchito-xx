class Ficha:

    def __init__(self, dueño: str):
        self.__dueño__ = dueño
        self.__capturada__ = False

    def get_dueño(self):
        return self.__dueño__

    def set_dueño(self, dueño):
        self.__dueño__ = dueño
    
    def get_capturada(self):
        return self.__capturada__
    
    def set_capturada(self, capturada: bool):
        self.__capturada__ = capturada
    
    def __repr__(self) -> str:
        estado = "Capturada" if self.__capturada__ else "Libre"
        return f"Dueño de la ficha es {self.__dueño__} y esta {estado}"

if __name__ == "__main__":
    f = Ficha("X")
    g = Ficha("O")
    print(f)
    print(f.get_dueño())
    print(f.get_capturada())
    f.set_capturada(True)
    print(f.get_capturada())
    print(f)
    print(g)    

        
