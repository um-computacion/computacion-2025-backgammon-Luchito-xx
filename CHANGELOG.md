# Changelog

Registro de cambios importantes del proyecto. Cada versión contiene cambios relevantes.

Formato: *Keep a Changelog* — [https://keepachangelog.com/es/1.0.0/](https://keepachangelog.com/es/1.0.0/)

---

## [0.3.2] - 2025-09-28

### Changed

- `cli.py`:  inicialización `saltos -> []` y mostrar turno actual.
- Estructura: añadido `__init__.py` en el paquete core para importar módulos correctamente.
- Limpieza: eliminación de pruebas locales en `dice.py`, `player.py` y `ficha.py`.
- `player.py`: añadido método `set_name()`.

### Fixed

- Corrigido commit accidental de `board.py` pushado en la rama de CI.
- `backgammon.py` y `validaciones.py`: imports y eliminación de demos.
- `backgammon.py`: parámetro que tiraba error (`jugador` → `jugador.get_name()`).
- `ficha.py`: renombrado atributo `dueño` → `jugador`
- `cli.py`:`get_state()` → `mostrar()`

---

## [0.3.1] - 2025-09-16

### Added

- `board.py`: `validar_movimiento` y `mover` implementados (implementación funcional básica, queda corregir integración con CLI).
- `backgammon.py`: manejo de victoria y mejoras en `mover` 

### Changed

- `player.py`: clase renombrada a `Player`.
- Se subieron demos temporales en `board.py` y `backgammon.py` para pruebas locales.

---

## [0.3.0] - 2025-09-14

### Added

- `dice.py`: lógica para manejar dobles.
- `validaciones.py`: planteo de validaciones con `@staticmethod` y corrección de `movimiento_valido`.

### Changed

- `board.py`: replanteo de `mover` y `get_board` 
- `backgammon.py`: desarrollo inicial (esqueleto y lógica básica incompleta).

### Notes

- validaciones y la integración de `validaciones` dentro del juego faltan completar.

---

## [0.2.1] - 2025-09-11

### Added

- Integración inicial de CI: GitHub Actions y SonarCloud (configuración base y corrección de `ci.yml`).
- Archivos de configuración añadidos: `.pylintrc`, `requirements.txt`
- Implementación inicial del CLI (estructura y comandos básicos).

---

## [0.2.0] - 2025-09-02
### Added
- Creación del módulo `Backgammon` y replanteo de los módulos para aplicar principios SOLID.
- Modificación de `get_board` (cambio en la forma de presentación / salida).

### Changed
- Reestructuración:(modulos `Backgammon`, `Board`, `Player`, `Dice`, `Ficha`, `Validaciones`).


---

## [0.1.3] - 2025-08-31
### Added
- `Dice` ahora devuelve una tupla de dos valores aleatorios `(d1, d2)` 
- Primera reestructuración de `board` para integrar el módulo `ficha` 
### Changed
- `board` para facilitar manejo de fichas como objetos

### Notes
- Implementaciones incompletas: presentación y validaciones finas pendientes.

---

## [0.1.2] - 2025-08-30
### Added
- Primera implementación de `Ficha` (módulo `ficha.py`)
### Changed
- Preparación para que `Board` y `Player` usen objetos `Ficha` en lugar de tuplas.

### Notes
- Ficha implementada, pero falta implementar en `board` y `player`.

---

## [0.1.1] - 2025-08-29
### Changed
- `get_board`: nuevo formato de salida más legible (dos filas).
- `mover`: validaciones adicionales y movimiento basado en reglas backgammon

---

## [0.1.0] - 2025-08-28
### Added
- `Board` (clase): posiciones iniciales y movientos básicos (esqueleto funcional).
- `Dice` (clase): giro y obtención de resultado (primera API).
- `Player` (clase): manejo básico de jugadores (nombre y dirección).
### Notes
- Versión inicial con el esqueleto POO y la lógica mínima para comenzar a interactuar con el juego.

---
