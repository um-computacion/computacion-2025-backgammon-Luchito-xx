# Backgammon - Proyecto Computación 2025

**Alumno**: Luciano Agustín Fernández Actis

## Descripción

Implementación completa del juego Backgammon en Python siguiendo principios de POO y SOLID. El proyecto incluye dos interfaces de usuario: CLI (línea de comandos) y GUI (Pygame).

## Estructura del Proyecto

```
backgammon/
├── core/                   # Lógica del juego
│   ├── backgammon.py      # Orquestador principal
│   ├── board.py           # Tablero y estado
│   ├── dice.py            # Dados
│   ├── ficha.py           # Fichas
│   ├── player.py          # Jugadores
│   ├── validaciones.py    # Reglas del juego
│   └── exceptions.py      # Excepciones personalizadas
├── cli/                    # Interfaz de línea de comandos
│   └── cli.py
├── pygame_ui/              # Interfaz gráfica
│   ├── pygame_ui.py
│   └── dados_ui.py
├── tests/                  # Suite de tests
│   ├── test_backgammon.py
│   ├── test_board.py
│   ├── test_dice.py
│   ├── test_ficha.py
│   ├── test_player.py
│   └── test_validaciones.py
├── assets/                 # Recursos (imágenes, sonidos)
├── requirements.txt        # Dependencias
├── CHANGELOG.md           # Historial de cambios
├── JUSTIFICACION.md       # Justificación de diseño
└── README.md              # Este archivo
```

## Instalación y Ejecución

### Requisitos Previos

- Python 3.10 o superior
- pip

### 1. Clonar el Repositorio

```bash
git clone https://github.com/um-computacion/computacion-2025-backgammon-Luchito-xx.git 
cd backgammon
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Juego

#### Modo CLI (Línea de Comandos)

```bash
python -m cli.cli
```

#### Modo Gráfico (Pygame)

```bash
python -m pygame_ui.pygame_ui
```

## Testing

### Ejecutar Todos los Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Ejecutar Tests con Cobertura

```bash
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
coverage html  
```

### Tests Específicos

```bash
# Test de un módulo específico
python -m unittest tests.test_board

# Test de una clase específica
python -m unittest tests.test_board.TestBoard

# Test de un método específico
python -m unittest tests.test_board.TestBoard.test_mover_destino_vacio
```
## Cómo Jugar

### Reglas Básicas

1. **Objetivo**: Mover todas tus fichas a tu "casa" y sacarlas del tablero antes que tu oponente
2. **Jugadores**:
   - **Jugador X**: Mueve de celdas 0-11 hacia 18-23 (casa en 18-23)
   - **Jugador O**: Mueve de celdas 23-12 hacia 5-0 (casa en 0-5)
3. **Dados**: Se lanzan dos dados por turno. Dobles te dan 4 movimientos
4. **Capturas**: Si una celda tiene solo 1 ficha enemiga, puedes capturarla
5. **Reingreso**: Si tienes fichas capturadas, debes reingresarlas antes de mover otras

### Instrucciones de CLI

- `origen salto`: Mover ficha (ej: `12 3`)
- `-1 dado`: Reingresar ficha capturada (ej: `-1 5`)
- `ayuda`: Mostrar ayuda completa
- `salir`: Salir del juego

### Instrucciones de Pygame

1. Click en "Tirar Dados"
2. Click en una celda con tus fichas
3. Click en un dado para seleccionarlo
4. El movimiento se ejecuta automáticamente
5. ESC: Cancelar selección

## Documentación Adicional

- [CHANGELOG.md](CHANGELOG.md): Historial detallado de cambios
- [JUSTIFICACION.md](JUSTIFICACION.md): Decisiones de diseño y arquitectura(Falta)

## Estado del Proyecto

- **v0.5.0**: CLI completa + Pygame UI + Tests completos
- **Próximas features**:
  - Implementado de Docker
  - Sistema de guardado con Redis (opcional)
  - Mejoras visuales en Pygame
  - Sonidos y animaciones
---
