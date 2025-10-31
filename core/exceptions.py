"""
Módulo Exceptions - Excepciones personalizadas del juego.

Define todas las excepciones especificas del juego Backgammon
para manejo de errores de validacoin y reglas del juego
"""

class BackgammonError(Exception):
    """Base para todas las excepciones del juego Backgammon."""

class FueraDeRangoError(BackgammonError):
    """Índice de celda fuera del rango 0..23."""   

class CeldaInvalidaError(BackgammonError):
    """Se intentó operar sobre una celda vacía o no válida."""    

class ValidacionError(BackgammonError):
    """Error genérico de validación de reglas."""   

class CeldaBloqueadaError(BackgammonError):
    """Destino bloqueado por fichas enemigas.""" 

class FichasCapturadasError(BackgammonError):
    """Operación inválida cuando el jugador tiene fichas en la barra."""

class SinFichasCapturadas(BackgammonError):
    """No hay fichas capturadas para reingresar."""

class ReingresoInvalidoError(BackgammonError):
    """No se puede reingresar una ficha capturada (destino inválido)."""  

class SalidaInvalidaError(BackgammonError):
    """No se puede sacar fichas (condición de salida no cumplida)."""

class SaltosError(BackgammonError):
    """Errores relacionados con los saltos/dados (ej: no tirar antes de mover)."""
    