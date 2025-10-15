
import pytest
from core import validaciones
from core.ficha import Ficha
from core.exceptions import *

def crear_celdas_vacias():
    return [[] for _ in range(24)]

# celda
def test_validar_celda_valida():
    validaciones.Validaciones.validar_celda(0)
    validaciones.Validaciones.validar_celda(23)


@pytest.mark.parametrize("bad", [-1, 24, "a", 3.5])
def test_validar_celda_invalida(bad):
    with pytest.raises(FueraDeRangoError):
        validaciones.Validaciones.validar_celda(bad)


# ficha - celda
def test_validar_ficha_celda_vacia():
    with pytest.raises(CeldaInvalidaError):
        validaciones.Validaciones.validar_ficha_celda([], "X")


def test_validar_ficha_celda_jugador_enemigo():
    celda = [Ficha("O")]
    with pytest.raises(validaciones.CeldaBloqueadaError):
        validaciones.Validaciones.validar_ficha_celda(celda, "X")


def test_validar_ficha_celda_ok():
    celda = [Ficha("X"), Ficha("X")]
    validaciones.Validaciones.validar_ficha_celda(celda, "X")

# destino

def test_validar_destino_bloqueado_enemigo():
    destino = [Ficha("O"), Ficha("O")]
    with pytest.raises(validaciones.CeldaBloqueadaError):
        validaciones.Validaciones.validar_destino(destino, "X")


def test_validar_destino_ok():

    validaciones.Validaciones.validar_destino([], "X")
    validaciones.Validaciones.validar_destino([Ficha("O")], "X")
    validaciones.Validaciones.validar_destino([Ficha("X"), Ficha("X")], "X")

# movimiento valido

def test_movimiento_valido_X():
    celdas = crear_celdas_vacias()
    celdas[0] = [Ficha("X")]       
    celdas[3] = []                  
    destino = validaciones.Validaciones.movimiento_valido(celdas, 0, 3, "X", validar_salida=False)
    assert destino == 3

def test_movimiento_valido_O():
    celdas = crear_celdas_vacias()
    celdas[5] = [Ficha("O")]
    celdas[3] = []
    destino = validaciones.Validaciones.movimiento_valido(celdas, 5, 2, "O", validar_salida=False)
    assert destino == 3

def test_movimiento_valido_destino_fuera_validar_salida_false():
    celdas = crear_celdas_vacias()
    celdas[22] = [Ficha("X")]
    with pytest.raises(validaciones.FueraDeRangoError):
        validaciones.Validaciones.movimiento_valido(celdas, 22, 3, "X", validar_salida=False)

def test_movimiento_valido_destino_fuera_validar_salida_ok():
    celdas = crear_celdas_vacias()
    celdas[22] = [Ficha("X")]
    res = validaciones.Validaciones.movimiento_valido(celdas, 22, 3, "X", validar_salida=True)
    assert res is None

# Salida (sacar fichas del tablero)

def test_validar_salida_false_capturas():
    '''
    Todavia tiene fichas capturadas
    '''
    celdas = crear_celdas_vacias()
    capturas = [Ficha("X")]
    assert validaciones.Validaciones.validar_salida(celdas, capturas, "X") is False


def test_validar_salida_false_fichas_en_home():
    '''
    Todavia tiene fichas en las zonas de bloqueo
        - 0-17 para X
        - 6-23 para O
    '''
    celdas = crear_celdas_vacias()
    celdas[10] = [Ficha("X")]
    capturas = []
    assert validaciones.Validaciones.validar_salida(celdas, capturas, "X") is False


def test_validar_salida_true():
    '''
    No tiene fichas capturadas ni en las zonas de bloqueo
    '''
    celdas = crear_celdas_vacias()
    celdas[18] = [Ficha("X")]          
    capturas = []
    assert validaciones.Validaciones.validar_salida(celdas, capturas, "X") is True

def test_validar_salida_true_O():
    '''
    No tiene fichas capturadas ni en las zonas de bloqueo
    '''
    celdas = crear_celdas_vacias()             
    celdas[5] = [Ficha("O")]
    capturas = []
    assert validaciones.Validaciones.validar_salida(celdas, capturas, "O") is True
 
# validar movimiento salida

def test_movimiento_valido_salida():
    celdas = crear_celdas_vacias()
    celdas[22] = [Ficha("X")]
    destino = validaciones.Validaciones.movimiento_valido(celdas, 22, 3, "X", validar_salida=True)
    assert destino is None
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
