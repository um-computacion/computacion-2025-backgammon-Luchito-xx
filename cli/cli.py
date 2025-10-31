"""
CLI para el juego de Backgammon.

Contiene la lógica de la interfaz de línea de comandos para interactuar
con la clase `Backgammon` del paquete `core`.
"""

from core.backgammon import Backgammon
from core.exceptions import BackgammonError

class BackgammonCLI:
    """Interfaz de línea de comandos para jugar una partida de Backgammon."""

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
            print("\n Fichas capturadas:")
            if cap_x > 0:
                print(f"   Jugador X: {cap_x} ficha(s)")
            if cap_o > 0:
                print(f"   Jugador O: {cap_o} ficha(s)")

        # mostrar si el jugador actual tiene capturas
        jugador_actual = estado['turno']
        if jugador_actual == "X" and cap_x > 0:
            print("\n  Reingresa fichas capturadas")
            print("   Usa: -1 como dado (ejemplo: -1 3)")
        elif jugador_actual == "O" and cap_o > 0:
            print("\n  Reingresa fichas capturadas")
            print("   Usa: -1 como dado (ejemplo: -1 3)")

    def movimiento(self, entrada):
        """
        Procesa el movimiento del jugador

        Arg:
            entrada: valores ingresados (celda y salto)
        Retorna:
            True si debe continuar el turno,
            False si cambió de turno,
            None si se solicita salir.
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

            print("\nTurno completado")
            return False  # Cambiar turno

        except BackgammonError as e:
            # Error esperado del dominio
            print(f"Movimiento inválido: {e}")
            return True

        except (ValueError, IndexError, TypeError) as e:
            # Error en conversión de entrada o problema con índices/ tipos
            print(f"Entrada inválida o error interno ({e.__class__.__name__}): {e}")
            return True

        except KeyboardInterrupt:
            print("\nJuego interrumpido por el usuario.")
            return None

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

            # Verificar si puede mover
            if not self.game.puede_mover():
                print("\nNo tienes movimientos posibles. paso turno...")
                self.game.cambio_turno()
                continue

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
