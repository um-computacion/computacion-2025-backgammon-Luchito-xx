"""
Script principal para ejecutar el juego de Backgammon con interfaz Pygame.

Punto de entrada que inicia la aplicación gráfica del juego.
"""

import sys
from pygame_ui.pygame_ui import PygameUI


def main():
    """
    Función principal que inicia la interfaz gráfica.
    
    Maneja cualquier error de inicialización y proporciona
    mensajes de error útiles.
    """
    try:
        ui = PygameUI()
        ui.ejecutar()
    except ImportError as e:
        print("Error: No se pudo importar Pygame")
        print("Instala Pygame con: pip install pygame")
        print(f"Detalle: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()