from exceptions import *

'''
Validar: 
        - Seleccion de ficha a mover (existe, es suya, seleccion dentro de tabla)
        - Destino(¿sale de la tabla? o hay mas de 2 fichas contrarias)
'''
class Validaciones:

    @staticmethod
    def validar_celda(celda:int):
        if not isinstance(celda,int) or celda < 0 or celda > 23:
            raise FueraDeRangoError(f"celda {celda} fuera del rango de la tabla (0-23)")
    
    # No va a funcionar
    @staticmethod
    def validar_ficha_celda(ficha:list, jugador:str):
        if not ficha:
            raise CeldaInvalidaError("La celda no tiene fichas en juego")
        if ficha.get_jugador() != jugador:
            raise CeldaInvalidaError("La celda contiene fichas de otro jugador")
    
    
