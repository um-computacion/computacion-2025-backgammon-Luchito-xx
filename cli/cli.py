from core.board import board
from core.player import player    
from core.dice import dice    

def main():
    print("Backgammon Reglas: ... \n")
    b = board()
    b.inicio()
    print(b.get_board())

    jugadorA = player("A")
    jugadorB = player("B")
    turno = jugadorA

    while True:
        print(f"Turno del jugador: {turno.get_name()}")
        dado = dice()
        valor_dado = dado.roll()
        print(f"Valor del dado: {valor_dado}")

        try:
            celda_origen = int(input("Ingresa origen (0-23): "))

            resultado = b.mover(celda_origen, valor_dado, turno.get_name())
            print(b.mover(celda_origen, valor_dado, turno.get_name()))
            if resultado == ("X", 0):
                raise ValueError("No se pudo realizar el movimiento: ", resultado)
            else:
                print(b.get_board())
                turno = jugadorB if turno == jugadorA else jugadorA
        except ValueError:
            print("Entrada invalida. Intente de nuevo.")
            
            break

if __name__ == "__main__":
    main()