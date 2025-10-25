class BackgammonError(Exception):
    """Base para todas las excepciones del juego Backgammon."""
    pass

class FueraDeRangoError(BackgammonError):
    """Índice de celda fuera del rango 0..23."""
    pass

class CeldaInvalidaError(BackgammonError):
    """Se intentó operar sobre una celda vacía o no válida."""
    pass

class ValidacionError(BackgammonError):
    """Error genérico de validación de reglas."""
    pass

class CeldaBloqueadaError(BackgammonError):
    """Destino bloqueado por fichas enemigas."""
    pass

class FichasCapturadasError(BackgammonError):
    """Operación inválida cuando el jugador tiene fichas en la barra."""
    pass

class SalidaInvalidaError(BackgammonError):
    """No se puede sacar fichas (condición de salida no cumplida)."""
    pass

class SaltosError(BackgammonError):
    """Errores relacionados con los saltos/dados (ej: no tirar antes de mover)."""
    pass



