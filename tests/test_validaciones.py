
import pytest
from core import validaciones
from core.ficha import Ficha
from core.exceptions import *

def crear_celdas_vacias():
    return [[] for _ in range(24)]

# movimiento_valido

def test_movimiento_valido_X_ok():
    celdas = crear_celdas_vacias()
    celdas[0] = [Ficha("X")]
    capturas = []
    destino = validaciones.Validaciones.movimiento_valido(celdas, capturas, 0, 3, "X")
    assert destino is True

def test_movimiento_valido_O_ok():
    celdas = crear_celdas_vacias()
    celdas[5] = [Ficha("O")]
    capturas = []
    destino = validaciones.Validaciones.movimiento_valido(celdas, capturas, 5, 2, "O")
    assert destino is True

def test_movimiento_valido_destino_fuera_raises_salida_invalida():
    # intento de bearing-off pero hay fichas fuera del "home" -> debe raise SalidaInvalidaError
    celdas = crear_celdas_vacias()
    celdas[22] = [Ficha("X")]
    celdas[10] = [Ficha("X")]  # ficha fuera de home
    capturas = []
    with pytest.raises(SalidaInvalidaError):
        validaciones.Validaciones.movimiento_valido(celdas, capturas, 22, 3, "X")

def test_movimiento_valido_destino_fuera_validar_ok():
    # bearing-off permitido -> validar_salida devuelve True y movimiento_valido retorna True
    celdas = crear_celdas_vacias()
    celdas[22] = [Ficha("X")]
    capturas = []
    res = validaciones.Validaciones.movimiento_valido(celdas, capturas, 22, 3, "X")
    # en la implementación actual validar_salida devuelve True, por lo que movimiento_valido retorna True
    assert res is True


# Salida (sacar fichas del tablero)

# validar_salida (bearing-off)

def test_validar_salida_raises_si_tiene_capturas():
    celdas = crear_celdas_vacias()
    capturas = [Ficha("X")]
    with pytest.raises(FichasCapturadasError):
        validaciones.Validaciones.validar_salida(celdas, capturas, 22, 2, "X")

def test_validar_salida_raises_si_fichas_fuera_home():
    celdas = crear_celdas_vacias()
    celdas[10] = [Ficha("X")]
    capturas = []
    with pytest.raises(SalidaInvalidaError):
        validaciones.Validaciones.validar_salida(celdas, capturas, 22, 2, "X")

def test_validar_salida_true():
    celdas = crear_celdas_vacias()
    celdas[18] = [Ficha("X")]
    capturas = []
    assert validaciones.Validaciones.validar_salida(celdas, capturas, 18, 1, "X") is True

def test_validar_salida_true_O():
    celdas = crear_celdas_vacias()
    celdas[5] = [Ficha("O")]
    capturas = []
    assert validaciones.Validaciones.validar_salida(celdas, capturas, 5, 1, "O") is True

# validar_victoria

def test_validar_victoria_true():
    celdas = crear_celdas_vacias()
    capturas = []
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is True

def test_validar_victoria_false_por_tablero_y_capturas():
    celdas = crear_celdas_vacias()
    celdas[0] = [Ficha("X")]
    capturas = []
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is False

    celdas = crear_celdas_vacias()
    capturas = [Ficha("X")]
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is False

# Victoria

def test_validar_victoria_true():
    '''
    No hay fichas del jugador en el tablero ni en capturas
    '''
    celdas = crear_celdas_vacias()
    capturas = []
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is True


def test_validar_victoria_false():
    '''
    Hay fichas del jugador en el tablero o en capturas
    '''
    celdas = crear_celdas_vacias()
    celdas[0] = [Ficha("X")]
    capturas = []
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is False

    celdas = crear_celdas_vacias()
    capturas = [Ficha("X")]
    assert validaciones.Validaciones.validar_victoria(celdas, capturas, "X") is False
