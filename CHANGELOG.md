# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

Formato: *Keep a Changelog* — https://keepachangelog.com/es/1.0.0/  
Las entradas están ordenadas por versión y fecha (más recientes primero).

---

## [Unreleased] —   Falta:

---

## [0.3.0] - 2025-09-02
### Added
- Creación del módulo `Backgammon` y replanteo de los módulos para aplicar principios SOLID.
- Modificación de `get_board` (cambio en la forma de presentación / salida).

### Changed
- Reestructuración: planificación para responsabilidades (modulos `Backgammon`, `Board`, `Player`, `Dice`, `Ficha`, `Validaciones`).

### Notes
- Trabajo enfocado en arquitectura y preparación para aplicar SOLID correctamente; archivos pendientes de implementacion.

---

## [0.2.1] - 2025-08-31
### Added
- `Dice` ahora devuelve una tupla de dos valores aleatorios `(d1, d2)` (soporte para dobles).
- Primera reestructuración de `board` para integrar el módulo `ficha` (estructura de puntos como listas de objetos ficha).
### Changed
- Reorganización interna de `board` para facilitar manejo de fichas como objetos (pendiente: mostrar tablero con mejor formato, lógica completa de capturas, refactor de `mover` y nueva función `validar_movimiento`).
### Notes
- Implementaciones incompletas: presentación y validaciones finas pendientes.

---

## [0.2.0] - 2025-08-30
### Added
- Primera implementación de `Ficha` (módulo `ficha.py`): objeto ficha con estado (owner, id, capture flag).
### Changed
- Preparación para que `Board` y `Player` usen objetos `Ficha` en lugar de tuplas (refactor en curso).
### Notes
- Ficha implementada, pero falta integrar totalmente en `board` y `player`.

---

## [0.1.1] - 2025-08-29
### Changed
- Mejora de `get_board`: nuevo formato de salida más legible (dos filas).
- Mejora de `mover`: validaciones adicionales y ajuste del movimiento basado en reglas mínimas del juego.
- Eliminación de atributos y métodos innecesarios para simplificar el diseño.
- Inclusión de consideraciones para la lógica de fichas capturadas (idea/placeholder).
### Fixed
- Limpieza de código y simplificación de API pública del tablero.

---

## [0.1.0] - 2025-08-28
### Added
- `Board` (clase): posiciones iniciales y movientos básicos (esqueleto funcional).
- `Dice` (clase): giro y obtención de resultado (primera API).
- `Player` (clase): manejo básico de jugadores (nombre y dirección).
### Notes
- Versión inicial con el esqueleto POO y la lógica mínima para comenzar a interactuar con el juego.

---
