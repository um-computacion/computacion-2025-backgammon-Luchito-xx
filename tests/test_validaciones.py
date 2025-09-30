
import pytest
from core import validaciones
from core.ficha import Ficha


def crear_celdas_vacias():
    return [[] for _ in range(24)]


# celda
def test_validar_celda_valida():
    validaciones.Validaciones.validar_celda(0)
    validaciones.Validaciones.validar_celda(23)


@pytest.mark.parametrize("bad", [-1, 24, "a", 3.5])
def test_validar_celda_invalida(bad):
    with pytest.raises(validaciones.FueraDeRangoError):
        validaciones.Validaciones.validar_celda(bad)


# ficha - celda
def test_validar_ficha_celda_empty_raises():
    with pytest.raises(validaciones.CeldaInvalidaError):
        validaciones.Validaciones.validar_ficha_celda([], "X")


def test_validar_ficha_celda_other_player_raises():
    celda = [Ficha("O")]
    with pytest.raises(validaciones.CeldaBloqueadaError):
        validaciones.Validaciones.validar_ficha_celda(celda, "X")


def test_validar_ficha_celda_ok():
    celda = [Ficha("X"), Ficha("X")]
    validaciones.Validaciones.validar_ficha_celda(celda, "X")


