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

    @staticmethod
    def validar_ficha_celda(ficha:list, jugador:str):
        if not ficha:
            raise CeldaInvalidaError("La celda no tiene fichas en juego")
        if ficha != jugador:
            raise CeldaInvalidaError("La celda contiene fichas de otro jugador")
        
    @staticmethod
    def validar_destino(ficha_destino:list , jugador:str):
        if ficha_destino[0].get_jugador() != jugador and len(ficha_destino) >= 2:
            raise CeldaBloqueadaError("La celda destino de la ficha esta ocupada por 2 o mas fichas enemigas")
    
    @staticmethod
    def movimiento_valido(celdas:list, celda:int, saltos:int, jugador:str):
        Validaciones.validar_celda(celda)
        ficha = celdas[celda]
        Validaciones.validar_ficha_celda(ficha, jugador)
        destino = celda + saltos if jugador == "X" else celda - saltos 
        ficha_destino = celdas[destino]
        Validaciones.validar_destino(ficha_destino, jugador)
