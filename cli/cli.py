from core.backgammon import Backgammon
from core.exceptions import *


class BackgammonCLI:
    def __init__(self):
        self.game = Backgammon()
        
 
    def obtener_movimiento(self):
        """Obtiene el movimiento del jugador"""
        print("Formato: 'origen salto' (ej: 12 3)\n")
        
        entrada = input("   Ingresa movimiento: ").strip().lower()
        return entrada
    
    def mostrar_estado_juego(self):
        """Muestra el estado actual del juego"""
        estado = self.game.mostrar()
        
        print(estado["board"])
        
        print(f"\nTurno de: {estado['turno']}")
        print(f"Dados disponibles: {estado['saltos']}")
        
        # Mostrar capturas
        capturas = estado["capturas"]
        cap_x = sum(1 for f in capturas if f.get_jugador() == "X")
        cap_o = sum(1 for f in capturas if f.get_jugador() == "O")
        
        if cap_x > 0 or cap_o > 0:
            print(f"\n Fichas capturadas:")
            if cap_x > 0:
                print(f"   Jugador X: {cap_x} ficha(s)")
            if cap_o > 0:
                print(f"   Jugador O: {cap_o} ficha(s)")
        
        # mostrar si el jugador actual tiene capturas
        jugador_actual = estado['turno']
        if jugador_actual == "X" and cap_x > 0:
            print(f"\n  Reingresa fichas capturadas")
            print(f"   Usa: -1 como dado (ejemplo: -1 3)")
        elif jugador_actual == "O" and cap_o > 0:
            print(f"\n  Reingresa fichas capturadas")
            print(f"   Usa: -1 como dado (ejemplo: -1 3)")
    
    def movimiento(self, entrada):
        """
        Procesa el movimiento del jugador
        Retorna True si debe continuar el turno, False si cambió de turno
        Si hay error, retorna None y muestra el error
        """
        try:
            partes = entrada.split()
            if len(partes) != 2:
                print(" Formato incorrecto. Usa: origen salto")
                print(" Ejemplo: 1 3  o  -1 4")
                return True
            
            origen = int(partes[0])
            salto = int(partes[1])
            
            # Realizar movimiento
            self.game.mover(origen, salto)
            print("Movimiento realizado correctamente")
            
            # Verificar si quedan movimientos
            if self.game.get_saltos():
                print(f"\nTe quedan dados: {self.game.get_saltos()}")
                return True  # Continuar turno
            else:
                print("\nTurno completado")
                return False  # Cambiar turno
                
        except BackgammonError as e:
            # Error esperado del dominio
            print(f"Movimiento inválido: {e}")
            return True

        except Exception as e:
            # Error inesperado: mostramos tipo y mensaje
            print(f"Error inesperado ({e.__class__.__name__}): {e}")
            return True
    
    def jugar(self):
        """Bucle principal del juego"""
        self.game = Backgammon()
        self.game.inicio()
        
        # Bucle principal
        while True:

            # Verificar ganador
            estado = self.game.mostrar()
            if estado["ganador"]:
                print(f"\nGano el jugador {estado['ganador']}\n")
                print()
                print(estado["board"])
                break
            
            # Mostrar estado
            self.mostrar_estado_juego()
            
            # Tirar dados si es un nuevo turno
            if not self.game.get_saltos():
                print("\n Dados tirados...")
                dados = self.game.tirar_dado()
                print(f"   Resultado: {dados}")
                
            # Obtener movimiento
            entrada = self.obtener_movimiento()
            resultado = self.movimiento(entrada)
            
            # salir del juego
            if resultado is None:
                break

                    


def main():
    """Punto de entrada del programa"""
    cli = BackgammonCLI()
    cli.jugar()


if __name__ == "__main__":
    main()