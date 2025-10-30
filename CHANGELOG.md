# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),

---

## [Unreleased]

### Pendiente
- Interfaz gráfica con Pygame
- Mejoras en la CLI 
---

## [0.5.0] - 2025-10-29

### Added
- **Configuración completa del proyecto**:
  - `.gitignore` configurado correctamente para Python
  - `__init__.py` en módulos `core/` y `tests/`

### Changed
- **CI/CD mejorado**: 
  - Migración a `unittest` para ejecución de tests
  - Ajustes en workflow de GitHub Actions
  - Auto-merge automático de PRs de reportes

### Fixed
- Eliminación de archivos tracked innecesarios (`.pyc`, cache)

---

## [0.4.0] - 2025-10-24 / 2025-10-26

### Added
- **CLI completa y funcional** (`cli/cli.py`):
  - Métodos `obtener_movimiento()`,`mostrar_estado_juego()`,`movimiento()`, `jugar()`
  - Manejo de fichas capturadas
  - Detección automática de victoria
  - Sistema de manejo de errores

- **Funcionalidad `puede_mover()`**:
  - Validación de movimientos posibles antes de solicitar input
  - Paso automático de turno cuando no hay movimientos válidos
  - Implementado en `Validaciones` y usado en CLI

- **Tests exhaustivos**:
  - Suite completa con 93% de cobertura
  - Tests para todos los módulos: `backgammon`, `board`, `dice`, `ficha`, `player`, `validaciones`
  - Casos de borde y escenarios complejos
  - Uso de mocks y patches para aislar funcionalidad

### Changed
- Refactor de manejo de excepciones en CLI:
  - Separación entre `BackgammonError` (errores de dominio esperados)
  - Captura genérica de `Exception` para errores inesperados
  - Mensajes de error más descriptivos

### Fixed
- Corrección en tests de `Dice` con dados dobles
- Fix en tests de `Board` para movimientos
- Ajustes en validaciones de reingreso

---

## [0.3.0] - 2025-10-23 / 2025-10-24

### Added
- **Documentación completa con docstrings**:
  - Todos los módulos documentados (soolo funcion, falta parametros esperados y salida)

- **Sistema de excepciones jerárquico** (`exceptions.py`):
  - `BackgammonError` como clase base
  - Excepciones específicas:
    - `FueraDeRangoError`: índice de celda inválido
    - `CeldaInvalidaError`: celda vacía o no válida
    - `CeldaBloqueadaError`: destino bloqueado por enemigo
    - `FichasCapturadasError`: debe reingresar fichas primero
    - `SinFichasCapturadas`: no hay fichas en la barra
    - `ReingresoInvalidoError`: reingreso no válido
    - `SalidaInvalidaError`: no puede sacar fichas
    - `SaltosError`: problemas con dados/saltos

- **Módulo Backgammon completo**:
  - `turno_inicial()`: Selección aleatoria del primer jugador (dados diferentes)
  - Integración completa con `Validaciones`

- **Refactor de Validaciones**:
  - Unificación de validaciones en `movimiento_valido()`
  - `tiene_capturas()`: método auxiliar privado
  - `validar_salida()` integrado en flujo de validación
  - `validar_reingreso()`: lógica específica para fichas capturadas

- **Mejoras en Board**:
  - Sistema de capturas implementado
  - Eliminación de validaciones (Las agrupo en `Validaciones`)
  - Método `mover()` simplificado (solo ejecuta movimientos, no valida)

### Changed
- **Refactorización SOLID completa**:
  - **Board**: Responsable solo de la estructura y modificación del tablero
  - **Validaciones**: Toda la lógica de reglas del juego
  - **Backgammon**: Orquestación y flujo de juego
  - Separación clara de responsabilidades, Se llegaba a validar 3 veces algunos aspectos entre board-validaciones-Backgammon (Se dejan solo en validaciones)

### Fixed
- Corrección en `validar_salida()`: verificación correcta de destino fuera de rango
- Fix en comparación de fichas con jugadores (uso correcto de `get_jugador()`)
- Corrección de parámetros en llamadas (`jugador` -> `jugador.get_name()`)

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
- **Mejoras en `get_board()`**:
  - Formato visual mejorado (dos filas con separador)
  - Mejor representación de fichas (N°-Ficha -> 4X)
  - Corrección: fichas superiores en orden 23→12 (no 11→0)

### Fixed
- Fix en `validar_destino()`: verificación de celda vacía antes de acceder
- Fix en cálculo de destino para jugador O (dirección incorrecta)
- Corrección en raises de excepciones (ubicación correcta)

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
