
"""
que hacer: 
- mostrar tablero, dados, turno, movimientos pendientes
- tira dados
- intenta un movimiento simple (origen y pasos)
- mostarar resultado
- si error, mostrar error
- fin
"""

from core.backgammon import Backgammon
from core.validaciones import ValidacionError

def main():
    game = Backgammon()
    game.inicio()

    print("Backgammon :D\n")
    print(game.mostrar()["board"])

    saltos = []
    saltos = game.tirar_dado()

    print(f"\nvalor de dados: {saltos}")
    print(f"Turno de: {game.get_jugador().get_name()}")
    print("Movimientos pendientes:", game.get_saltos())

    mov = input("\ningrese 'origen pasos' (11 2) o (0 1) ").strip()
    if not mov:
        print("fin prueba")
        return

    try:
        origen, salto = mov.split()
        origen = int(origen)
        salto = int(salto)
        game.mover(origen, salto)
        print("\nMovimiento aplicado\ntablero:\n")
        print(game.mostrar()["board"])
    except ValidacionError as e:
        print("movimiento invalido:", e)
    except Exception as e:
        print("error:", e)

if __name__ == "__main__":
    main()