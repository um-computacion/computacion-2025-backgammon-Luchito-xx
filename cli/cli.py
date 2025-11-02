"""
CLI para el juego de Backgammon.

Contiene la lógica de la interfaz de línea de comandos para interactuar
con la clase `Backgammon` del paquete `core`.
"""
import os
import time

from core.backgammon import Backgammon
from core.exceptions import BackgammonError

class BackgammonCLI:
    """Interfaz de línea de comandos para jugar una partida de Backgammon."""

    def __init__(self):
        self.game = Backgammon()

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_titulo(self):
        """Printea en consola BACKGAMMON con estilo :p"""
        print("╔" + "═" * 50 + "╗")
        print("║" + " " * 15 + "BACKGAMMON" + " " * 25 + "║")
        print("╚" + "═" * 50 + "╝")
        print()

    def pausar(self):
        """Pausa hasta que el usuario presione Enter"""
        input("\nPresiona Enter para continuar...")

    def obtener_movimiento(self):
        """Obtiene el movimiento del jugador"""
        print("\n" + "─" * 52)
        print("Ingresa...")
        print("  Formato: 'origen salto' (ej: 12 3)")
        print("  O escribe 'salir', 'ayuda'")
        print("─" * 52)

        try:
            entrada = input(">>> ").strip().lower()
            return entrada
        except (KeyboardInterrupt, EOFError):
            print("\n\nInterrupción detectada")
            return 'salir'

    def mostrar_estado_juego(self):
        """Muestra el estado actual del juego"""
        estado = self.game.mostrar()

        print("\n" + "═" * 52)
        print(estado["board"])
        print("═" * 52)

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
            print("\n¡PRIMERO! Reingresa fichas capturadas")
            print("   Usa: -1 como dado (ejemplo: -1 3)")
        elif jugador_actual == "O" and cap_o > 0:
            print("\n¡PRIMERO! Reingresa fichas capturadas")
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
        if not entrada:
            print("\nDebes escribir algo.")
            self.pausar()
            self.limpiar_pantalla()
            return True

        if entrada == 'salir':
            print("\n¿Seguro que quieres salir? (s/n)")
            respuesta = input(">>> ").strip().lower()
            self.limpiar_pantalla()
            return None if respuesta == "s" else True

        if entrada == 'ayuda':
            self.mostrar_ayuda()
            self.limpiar_pantalla()
            return True  # Continuar en el mismo turno

        return self._procesar_movimiento(entrada)

    def _procesar_movimiento(self, entrada):
        """Procesa un movimiento del juego"""

        try:
            partes = entrada.split()

            if len(partes) != 2:
                print("\nFORMATO INCORRECTO (ingresa 'ayuda' o lee leyenda de arribaa)")
                self.pausar()
                return True

            origen = int(partes[0])
            salto = int(partes[1])

            # Realizar movimiento
            self.game.mover(origen, salto)
            print("Movimiento realizado correctamente")
            time.sleep(0.5)

            # Verificar si quedan movimientos
            if self.game.get_saltos():
                time.sleep(2)
                self.limpiar_pantalla()
                return True  # Continuar turno

            print("\nTurno completado")
            time.sleep(2)
            return False  # Cambiar turno

        except BackgammonError as e:
            # Error esperado del dominio
            print(f"Movimiento inválido: {e}")
            self.pausar()
            self.limpiar_pantalla()
            return True

        except ValueError:
            print("Debes usar números enteros.")
            print("   Incorrecto: A 5, 12.5 3, abc xyz")
            print("   Correcto: 12 5, -1 4, 0 3")
            self.pausar()
            self.limpiar_pantalla()
            return True

        except KeyboardInterrupt:
            print("\n\nInterrupción detectada")
            print("¿Quieres salir del juego? (s/n)")
            respuesta = input(">>> ").strip().lower()
            self.limpiar_pantalla()
            return None if respuesta in ['s', 'si', 'sí'] else True


    def jugar(self):
        """Bucle principal del juego"""
        self.game = Backgammon()
        self.limpiar_pantalla()
        self.game.inicio()
        print("Iniciando nueva partida...\n")

        # Mostrar selección de turno inicial
        print("DETERMINANDO JUGADOR INICIAL")
        print("\nCada jugador lanza un dado...")
        time.sleep(1.5)

        # Iniciar juego y obtener resultado
        while True:
            time.sleep(1)

            resultado = self.game.inicio()

            if resultado:  # Si no hubo empate
                print(f"\n  Jugador X: {resultado['dados_x']}")
                time.sleep(0.5)
                print(f"  Jugador O: {resultado['dados_o']}")
                time.sleep(1)

                print(f"\n¡Gano el jugador {resultado['ganador']}! Comienza jugando...")
                time.sleep(1.5)
                self.limpiar_pantalla()
                break

            print("\n¡Empate! Lanzando de nuevo...")
            time.sleep(1)


        # Bucle principal
        while True:

            # Verificar ganador
            estado = self.game.mostrar()
            if estado["ganador"]:
                print(f"\nGano el jugador {estado['ganador']}\n")
                print()
                print(estado["board"])
                break

            # Tirar dados si es nuevo turno
            if not self.game.get_saltos():
                self.game.tirar_dado()

            # Mostrar estado
            self.mostrar_titulo()
            self.mostrar_estado_juego()

            # Verificar si puede mover
            if not self.game.puede_mover():
                print("\nNo tienes movimientos posibles. Se cambiara de turno")
                self.game.cambio_turno()
                time.sleep(2)
                self.limpiar_pantalla()
                continue

            # Obtener movimiento
            entrada = self.obtener_movimiento()
            resultado = self.movimiento(entrada)

            # salir del juego
            if resultado is None:
                break

    def mostrar_ayuda(self):
        """Muestra la ayuda completa del juego"""
        self.limpiar_pantalla()
        self.mostrar_titulo()

        print("AYUDA - CÓMO JUGAR BACKGAMMON\n")

        print("-    OBJETIVO DEL JUEGO\n")
        print("Ser el primero en mover todas tus fichas a tu 'casa'")
        print("y sacarlas del tablero.\n")

        print("-    FICHAS EN TABLERO\n")
        print("  X2 = 2 fichas del jugador X")
        print("  O5 = 5 fichas del jugador O")
        print("  -- = Posición vacía.\n")

        print("-    MOVIMIENTOS BÁSICOS\n")
        print("• Formato: origen salto")
        print("  Ejemplo: 12 5  (mover desde celda 12 con dado 5)")
        print()
        print("• Jugador X: mueve de celdas bajas (0-11) a altas (12-23)")
        print("  Casa de X: celdas 18-23")
        print()
        print("• Jugador O: mueve de celdas altas (23-12) a bajas (11-0)")
        print("  Casa de O: celdas 0-5\n")

        print("-    CAPTURAS\n")
        print("• Si una celda tiene UNA ficha enemiga, puedes capturarla")
        print("• Las fichas capturadas van a la barra (centro)")
        print("• Si tienes fichas capturadas, DEBES reingresarlas primero")
        print("• Para reingresar: -1 [dado]")
        print("  Ejemplo: -1 3  (reingresar con dado 3)\n")

        print("- SACAR FICHAS (salida de tablero)\n")
        print("• Solo puedes sacar fichas cuando TODAS estén en tu casa")
        print("• No puedes tener fichas capturadas")
        print("• El dado debe sacarte exactamente, o puedes usar un dado")
        print("  mayor si no hay fichas más atrás\n")

        print("-    COMANDOS\n")
        print("• origen salto  - Realizar movimiento")
        print("• -1 dado       - Reingresar ficha capturada")
        print("• pasar         - Pasar turno (si no puedes mover)")
        print("• ayuda         - Mostrar esta ayuda")
        print("• salir         - Salir del juego\n")

        self.pausar()

def main():
    """Punto de entrada del programa"""
    cli = BackgammonCLI()
    cli.jugar()


if __name__ == "__main__":
    main()
