
"""
que hacer: 
- mostrar tablero
- tira dados
- intenta un movimiento simple (origen y pasos)
"""

from core.backgammon import Backgammon
from core.validaciones import ValidacionError

def main():
    game = Backgammon()
    game.inicio()

    print("Backgammon :D\n")
    print(game.mostrar()["board"])

    d1, d2 = game.tirar_dado()
    print(f"\nvalor de dados: {d1}, {d2}")
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
        print(game.get_state()["board"])
        if game.get_state().get("winner"):
            print("¡Ganadooor¡¡:", game.mostrar()["winner"], ")")
    except ValidacionError as e:
        print("movimiento invalido:", e)
    except Exception as e:
        print("error:", e)

if __name__ == "__main__":
    main()
