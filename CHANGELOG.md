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

### Pendiente
- Interfaz gráfica con Pygame
- Mejoras en la CLI 
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
- **Configuración completa del proyecto**:
  - `.gitignore` configurado correctamente para Python
  - `__init__.py` en módulos `core/` y `tests/`

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

## [0.2.0] - 2025-10-10 / 2025-10-14

### Added
- **tests inicial**:
  - `test_backgammon.py`: Tests de inicialización, turnos, dados
  - `test_board.py`: Tests de `get_board()`, `mover()`, capturas
  - `test_dice.py`: Tests de generación de valores aleatorios
  - `test_ficha.py`: Tests de estado de fichas
  - `test_player.py`: Tests de jugadores
  - `test_validaciones.py`: Tests de reglas del juego
  - Uso de `@staticmethod` para validaciones

- **Primera CLI de prueba** (`cli/cli.py`):
  - Interfaz básica con turnos
  - Input de valores de celda
  - Visualización del tablero en cada jugada

### Changed
- `get_board`: nuevo formato de salida más legible (dos filas).
- `mover`: validaciones adicionales y movimiento basado en reglas backgammon

---

## [0.1.0] - 2025-09-11 / 2025-09-30

### Added
- **CI/CD con GitHub Actions**:
  - Workflow inicial con Coverage y Pylint
  - Configuración de `.pylintrc`
  - Generación automática de reportes
  - Integración con SonarCloud (configuración inicial)

- **Módulo Validaciones** (`validaciones.py`):
  - `movimiento_valido()`: Validación básica de movimientos
  - `validar_salida()`: Condiciones para sacar fichas del tablero
  - `validar_victoria()`: Detección de ganador
  - Uso de `@staticmethod` para métodos sin estado

- **Módulo Exceptions** (`exceptions.py`):
  - Primera versión con excepciones básicas

---

## [0.0.3] - 2025-09-02 / 2025-09-17

### Added
- **Módulo Backgammon** (`backgammon.py`):
  - Clase principal que coordina el juego
  - Integración de Board, Player, Dice
  - Métodos: `inicio()`, `mover()`, `cambio_turno()`, `mostrar()`

- **Inicio de Validaciones**:
  - Primera implementación de `validar_movimiento()`

---

## [0.0.2] - 2025-08-29 / 2025-08-31

### Added
- **Módulo Ficha** (`ficha.py`):
  - Clase `Ficha` con atributos `jugador` y `capturada`
  - Métodos getter/setter

- **Soporte para dados dobles**:
  - `Dice.roll()` retorna 4 valores cuando salen dobles, doble 3 -> `[3, 3, 3, 3]`

### Changed
- **Reestructuración de Board**:
  - Integración de objetos `Ficha` en lugar de strings, se usa estructura de puntos como listas de objetos
  - Preparación para lógica de capturas

- **Mejoras en Board y Player**:
  - `get_board()`: Formato mejorado con dos filas
  - `mover()`: Validaciones adicionales y manejo de capturas (básico)

---

## [0.0.1] - 2025-08-27 / 2025-08-28

### Added
- **Configuración inicial del proyecto**:
  - Estructura de directorios: `core/`, `cli/`, `tests/`, `assets/`, `pygame_ui/`
  - Archivos base: `README.md`, `CHANGELOG.md`, `JUSTIFICACION.md`, `prompts.md`
  - `requirements.txt` con dependencias: `coverage`, `pylint`, `pygame`, `redis`

- **Clase Dice** (`dice.py`):
  - Método `roll()`: Genera dos valores aleatorios 1-6
  - Método `get_valor()`: Obtiene valores actuales
  - Método `__str__()`: Representación textual

- **Clase Board** (`board.py`):
  - Configuración inicial de 24 posiciones
  - Distribución inicial de fichas según reglas de Backgammon
  - Método `mover()` básico (esqueleto)
  - Método `get_board()` para representación visual

- **Clase Player** (`player.py`):
  - Atributo `name`: identificador del jugador
  - Métodos getter/setter
  - Método `__repr__()` para representación

### Notes
- Primera versión funcional mínima con POO

---
