# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),

---

## [1.0.0] - 2025-11-01 / 2025-11-02

### Added
- **Docker completo**:
  - `Dockerfile` con imagen Python 3.10-slim
  - `docker-compose.yml` con servicios: game y test
  - `.dockerignore` configurado

- **Documentación final**:
  - `README.md` completo con instalación, uso y features
  - `JUSTIFICACION.md` con decisiones de diseño y arquitectura
  - `prompts_desarrollo.md`, `prompts_documentacion.md`, `prompts_testing.md`

- **Tests para CLI**:
  - `test_cli.py` con 30+ tests
  - Coverage de CLI aumentado de 0% a 72%

### Changed
- **Pygame UI rediseñada**:
  - Nueva paleta de colores
  - Panel de información mejor organizado
  - Visualización de turno inicial agregada
  - Mejoras en UX: selección ficha → dado

- **Versionado final**:
  - Todos los módulos con cobertura ≥90%
  - Documentación completa
  - CI/CD funcional

### Notes
- **Versión 1.0.0**: Proyecto completo y funcional
- Cumple todos los requisitos de la consigna
- Coverage total: 90%
- Docker permite ejecución en cualquier ambiente

---

## [0.6.0] - 2025-10-31

### Added
- **Interfaz gráfica con Pygame** (`pygame_ui/`):
  - `pygame_ui.py`: UI completa con menú, juego y victoria
  - `dados_ui.py`: Dados clickeables con gestor
  - Tablero visual con celdas triangulares
  - Panel lateral con información y controles
  - Sistema de mensajes temporales
  - Visualización de turno inicial

- **Getters en `backgammon.py`**:
  - `get_board()`, `get_celdas()`, `get_capturas()`
  - Necesarios para integración con Pygame

### Changed
- **Refactor de `backgammon.py`**:
  - `turno_inicial()` ahora retorna diccionario con info del turno
  - `inicio()` retorna resultado de `turno_inicial()`
  - Mejor separación: lógica en core, visualización en UI

- **Mejoras en CLI**:
  - Mejor validación de entrada
  - Ayuda completa implementada
  - UX mejorada con pausas y mensajes claros

### Fixed
- Corrección de flujo de movimientos en Pygame
- Integración correcta entre core y pygame_ui

### Notes
- Pygame UI funcional con selección de fichas y dados por clicks
- Ambas interfaces (CLI y Pygame) comparten la misma lógica de core

---

## [0.5.0] - 2025-10-29 / 2025-10-30

### Added
- **Configuración completa del proyecto**:
  - `.gitignore` implementado (Python, venv, IDEs, tests)
  - `__init__.py` en `core/` y `tests/`
  - Archivos de cache removidos y listados en gitignore

- **Documentación mejorada**:
  - `CHANGELOG.md` actualizado y reestructurado
  - Docstrings limpiados y desarrollados

### Changed
- **CI/CD mejorado**:
  - Workflow ajustado para ejecutar con unittest
  - Corrección en ejecución de Pylint y tests
  - Requirements.txt actualizado

- **Correcciones de Pylint**:
  - Atributos corregidos: `__atr` → `__atr__`
  - Imports corregidos: específicos en lugar de `*`
  - Espacios y líneas largas corregidos
  - Excepciones concretas en lugar de genéricas

### Fixed
- Eliminación de `core/main.py` (innecesario)
- Corrección de imports faltantes en `board.py`

---

## [0.4.0] - 2025-10-23 / 2025-10-26

### Added
- **Documentación completa con docstrings**:
  - Todos los módulos de `core/` documentados (función, args, returns, raises)
  - Formato estándar: descripción → Args → Returns → Raises

- **Tests exhaustivos con unittest**:
  - Migración completa de pytest a unittest
  - `test_cli.py`: 30+ tests para CLI (coverage 72%)
  - `test_board.py`, `test_validaciones.py`, `test_backgammon.py` actualizados
  - Uso de mocks y patches para aislar funcionalidad

- **Manejo de movimientos posibles** (`puede_mover()`):
  - Verificación exhaustiva de movimientos válidos
  - Implementado en CLI: cambio automático de turno si no hay movimientos
  - Tests para escenarios sin movimientos posibles

### Changed
- **Refactor de validaciones** (v0.3.0 continuado):
  - `validar_salida()` y `movimiento_valido()` separados por complejidad (Pylint)
  - Imports específicos en lugar de `import *`
  - Mejor manejo de excepciones concretas

- **Mejoras en CLI**:
  - Separación `BackgammonError` vs `Exception` genérica
  - Mejor UX: validaciones, ayuda y comando salir mejorados
  - Manejo de interrupciones (Ctrl+C)

- **Tests mejorados**:
  - Corrección de tests para unittest
  - Tests para `FakeDice` con lógica determinista
  - Coverage aumentado a 90%

### Fixed
- Corrección de espacios y formato según Pylint
- Eliminación de `pass` innecesario en `exceptions.py`
- Fix en tests por cambios en `validaciones.py`


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