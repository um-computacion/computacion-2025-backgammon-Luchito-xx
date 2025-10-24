from .exceptions import *

class Validaciones:
    """
    Clase de validaciones para el juego de backgammon.
    Proporciona metodos estaticos para validar movimientos y condicion de victoria"""

    @staticmethod 
    def movimiento_valido(celdas:list, capturas, celda:int, salto:int, jugador:str):
        """Valida si un movimiento es valido """

        # Reingreso antes de usar otras fichas
        if Validaciones._tiene_capturas(capturas, jugador):
            if celda != -1:
                raise FichasCapturadasError("Debes reingresar fichas capturadas primero")
            return Validaciones._validar_reingreso(capturas, salto, jugador, celdas)
        
        # validar celda ingresada (origen)
        if celda == -1:
            raise FichasCapturadasError("No tienes fichas capturadas para reingresar")
        
        if celda < 0 or celda > 23:
            raise FueraDeRangoError(f"Celda {celda} fuera de rango")
        
        if not celdas[celda]:
            raise CeldaInvalidaError("La celda está vacía")
        
        if celdas[celda][0].get_jugador() != jugador:
            raise CeldaBloqueadaError("No es tu ficha")
        
        # calcular destino y validar
        destino = celda + salto if jugador == "X" else celda - salto
        
        # ver si sale del tablero (moviemiento de salida)
        if destino < 0 or destino > 23:
            return Validaciones.validar_salida(celdas, capturas, celda, salto, jugador)
        
        # validar destino
        if celdas[destino] and celdas[destino][0].get_jugador() != jugador and len(celdas[destino]) >= 2:
            raise CeldaBloqueadaError("Destino bloqueado por fichas enemigas")
        
        return True

    @staticmethod
    def _tiene_capturas(capturas: list, jugador:str):
        """verifica si tiene capturas"""
        return any(f.get_jugador() == jugador for f in capturas)
    
    @staticmethod
    def validar_salida(celdas: list, capturas: list, celda: int, salto: int, jugador: str):
        """Valida si puede sacar fichas del tablero"""
        # No puede tener capturas
        if Validaciones._tiene_capturas(capturas, jugador):
            raise FichasCapturadasError("No puedes sacar fichas teniendo capturas")
        
        # Todas las fichas deben estar en casa
        if jugador == "X":
            rango_casa = range(18, 24)
        else:
            rango_casa = range(0, 6)
        
        for i in range(24):
            if i not in rango_casa:
                for ficha in celdas[i]:
                    if ficha.get_jugador() == jugador:
                        raise SalidaInvalidaError("No todas tus fichas están en casa")
        
        # Si el dado te saca exactamente, ok
        destino = celda + salto if jugador == "X" else celda - salto
        if destino == 24 or destino == -1:
            return True
        
        # Si el dado es mayor, verificar que no haya fichas más atrás
        if jugador == "X":
            for i in range(celda + 1, 24):
                if celdas[i] and celdas[i][0].get_jugador() == jugador:
                    raise SalidaInvalidaError("Tienes fichas mas atras")
        else:
            for i in range(0, celda):
                if celdas[i] and celdas[i][0].get_jugador() == jugador:
                    raise SalidaInvalidaError("Tienes fichas mas atrás")
        
        return True
        
    @staticmethod
    def validar_victoria(celdas: list, capturas:list, jugador: str):
        """Valida si un jugador ha ganado la partida"""
        # fichas a contar
        fichas = 0

        # contar fichas en el tablero
        for celda in range(24):
            for ficha in celdas[celda]:
                if ficha.get_jugador() == jugador:
                    fichas += 1

        # contar fichas capturadas
        fichas_capturadas = sum(1 for ficha in capturas if ficha.get_jugador() == jugador)
        
        # retornar si gano (true)
        return(fichas_capturadas + fichas) == 0