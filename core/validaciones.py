"""
Módulo Validaciones - Validación de reglas del juego.

Verifica la validez de movimientos, reingresos, salidas del tablero y
condiciones de victoria
"""

from .exceptions import (
    FichasCapturadasError, FueraDeRangoError, CeldaBloqueadaError,
    CeldaInvalidaError, SinFichasCapturadas, ReingresoInvalidoError,
    SalidaInvalidaError
)

class Validaciones:
    """
    class Validaciones: Valida las reglas del juego de Backgammon con uso 
    de metodos estaticos
    """

    @staticmethod 
    def movimiento_valido(celdas:list, capturas, celda:int, salto:int, jugador:str):
        """
            Valida si un movimiento cumple las reglas de Backgammon.
        Args:
            celdas (list[list[Ficha]]): Estado actual del tablero (24 pos).
            capturas (list[Ficha]): Lista de fichas capturadas en la barra.
            celda (int): Posición origen (0-23) o -1 para reingreso.
            salto (int): Cantidad de posiciones del dado (1-6).
            jugador (str): Identificador del jugador ('X' o 'O').

        Returns:
            bool: True si el movimiento es válido según las reglas.
        """

        # Reingreso antes de usar otras fichas
        if Validaciones.tiene_capturas(capturas, jugador):
            if celda != -1:
                raise FichasCapturadasError("Debes reingresar fichas capturadas primero")
            return Validaciones.validar_reingreso(capturas, salto, jugador, celdas)
        
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
    def tiene_capturas(capturas: list, jugador:str):
        """
            Verifica si un jugador tiene fichas capturadas en la barra.
        Args:
            capturas (list[Ficha]): Lista de fichas en la barra.
            jugador (str): Identificador del jugador ('X' o 'O').

        Returns:
            bool: True si el jugador tiene al menos una ficha capturada.
        """
        return any(f.get_jugador() == jugador for f in capturas)

    @staticmethod
    def validar_reingreso(capturas: list, salto: int, jugador: str, celdas: list) -> bool:
        """
            Valida el reingreso de una ficha capturada desde la barra.
        Args:
            capturas (list[Ficha]): Lista de fichas en la barra.
            salto (int): Valor del dado para el reingreso (1-6).
            jugador (str): Identificador del jugador ('X' o 'O').
            celdas (list[list[Ficha]]): Estado actual del tablero.

        Returns:
            bool: True si el reingreso es válido.
        """
        
        # Verificar que tiene fichas capturadas
        if not Validaciones.tiene_capturas(capturas, jugador):
            raise SinFichasCapturadas()
        
        # Calcular posición de entrada
        if jugador == "X":
            destino = salto - 1  
        else:
            destino = 24 - salto  

        # Validar que el destino esté en rango
        if destino < 0 or destino > 23:
            raise ReingresoInvalidoError(
                f"El dado {salto} no permite reingresar (destino fuera del tablero)"
            )
        
        # Validar que el destino no esté bloqueado
        if celdas[destino]:
            if celdas[destino][0].get_jugador() != jugador and len(celdas[destino]) >= 2:
                raise CeldaBloqueadaError(
                    destino, 
                    f"No puedes reingresar en celda {destino}: bloqueada por fichas enemigas"
                )
        
        return True
    
    @staticmethod
    def validar_salida(celdas: list, capturas: list, celda: int, salto: int, jugador: str):
        """        
            Valida si puede sacar fichas del tablero (sin capturas y en casa)
        Args:
            celdas (list[list[Ficha]]): Estado actual del tablero.
            capturas (list[Ficha]): Lista de fichas capturadas.
            celda (int): Posición de la ficha a sacar (0-23).
            salto (int): Valor del dado (1-6).
            jugador (str): Identificador del jugador ('X' o 'O').

        Returns:
            bool: True si puede sacar la ficha.
        """
        # No puede tener capturas
        if Validaciones.tiene_capturas(capturas, jugador):
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
        """
            Valida si un jugador ha ganado la partida (sin fichas en capturas o board).
        Args:
            celdas (list[list[Ficha]]): Estado actual del tablero.
            capturas (list[Ficha]): Lista de fichas capturadas.
            jugador (str): Identificador del jugador ('X' o 'O').

        Returns:
            bool: True si el jugador ha ganado (0 fichas en total).
        """
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

    @staticmethod
    def puede_mover(celdas: list, capturas: list, saltos: list, jugador: str) -> bool:
        """
            Verifica si el jugador tiene al menos un movimiento válido.
        Args:
            celdas (list[list[Ficha]]): Estado actual del tablero.
            capturas (list[Ficha]): Lista de fichas capturadas.
            saltos (list[int]): Valores de dados disponibles.
            jugador (str): Identificador del jugador ('X' o 'O').

        Returns:
            bool: True si existe al menos un movimiento válido.
        """
        
        # Si no hay dados, no puede mover
        if not saltos:
            return False
        
        # Si hay capturadas, solo se prueban reingresos (-1)
        if Validaciones.tiene_capturas(capturas, jugador):
            for salto in saltos:
                try:
                    if Validaciones.movimiento_valido(celdas, capturas, -1, salto, jugador):
                        return True
                except Exception:
                    continue
            return False
        
        # Si no hay capturadas, probar todos los orígenes y saltos disponibles
        for salto in saltos:
            for origen in range(24):
                try:
                    if Validaciones.movimiento_valido(celdas, capturas, origen, salto, jugador):
                        return True
                except Exception:
                    continue
        
        return False