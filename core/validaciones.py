from exceptions import *

'''
Validar: 
        - Seleccion de ficha a mover (existe, es suya, seleccion dentro de tabla)
        - Destino(¿sale de la tabla? o hay mas de 2 fichas contrarias)
        - Movimiento -> True
        - Sacar fichas de tabla?
        - Victoria
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
            raise CeldaBloqueadaError("La celda contiene fichas de otro jugador")
        
    @staticmethod
    def validar_destino(ficha_destino:list , jugador:str):
        if ficha_destino[0].get_jugador() != jugador and len(ficha_destino) >= 2: # Usar validar_salida?
            raise CeldaBloqueadaError(f"La celda destino de la ficha esta ocupada por {len(ficha_destino)} fichas enemigas")
    
    @staticmethod
    def movimiento_valido(celdas:list, celda:int, saltos:int, jugador:str):

        Validaciones.validar_celda(celda)
        ficha = celdas[celda]
        Validaciones.validar_ficha_celda(ficha, jugador)
        
        destino = celda + saltos if jugador == "X" else celda - saltos 
        if destino < 0 or destino > 23: 
            if validar_salida: # Falta implementar
                return None
            raise FueraDeRangoError(f"Destino {destino} fuera del rango de la tabla (0-23)")
    
        
        ficha_destino = celdas[destino]
        Validaciones.validar_destino(ficha_destino, jugador)


    @staticmethod
    def validar_salida():
        pass

    @staticmethod
    def validar_victoria(celdas: list, capturas:list, jugador: str):
        # Chequear
        fichas = 0

        for celda in range(24):
            for ficha in celdas[celda]:
                if ficha.get_jugador() == jugador:
                    fichas += 1

        fichas_capturadas = sum(1 for ficha in capturas if ficha.get_jugador() == jugador)
        return(fichas_capturadas + fichas) == 0