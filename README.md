# Backgammon - Proyecto Computación 2025

**Alumno**: Luciano Agustín Fernández Actis

## Descripción

Implementación completa del juego Backgammon en Python siguiendo principios de POO y SOLID. El proyecto incluye dos interfaces de usuario: CLI (línea de comandos) y GUI (Pygame), con soporte completo para Docker.

## Características

- ✅ **Lógica completa del juego** con reglas oficiales de Backgammon
- ✅ **Interfaz CLI** interactiva y amigable
- ✅ **Interfaz gráfica** con Pygame (dados clickeables, animaciones)
- ✅ **Tests exhaustivos** con 90% de cobertura
- ✅ **Docker** y Docker Compose para fácil despliegue
- ✅ **CI/CD** con GitHub Actions (tests automáticos, coverage, pylint)
- ✅ **Documentación completa** con docstrings

---

## Instalación y Ejecución

### Opción 1: Docker (Recomendado)

#### Requisitos Previos
- Docker
- Docker Compose

#### Ejecutar el Juego

```bash
# Clonar repositorio
git clone https://github.com/um-computacion/computacion-2025-backgammon-Luchito-xx.git
cd backgammon

# Construir y ejecutar modo CLI
docker-compose up backgammon-game

# Ejecutar tests
docker-compose up backgammon-test
```

#### Comandos Docker Útiles

```bash
# Construir imagen
docker build -t backgammon:latest .

# Ejecutar CLI interactivo
docker run -it backgammon:latest

# Ejecutar tests con coverage
docker run backgammon:latest sh -c "coverage run -m unittest discover -s tests && coverage report"

# Limpiar contenedores
docker-compose down
```

---

### Opción 2: Instalación Local

#### Requisitos Previos
- Python 3.10 o superior
- pip

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/um-computacion/computacion-2025-backgammon-Luchito-xx.git
cd backgammon
```

#### 2. Crear Entorno Virtual (Recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 4. Ejecutar el Juego

**Modo CLI (Línea de Comandos)**
```bash
python -m cli.cli
```

**Modo Gráfico (Pygame)**
```bash
python -m pygame_ui.pygame_ui
```

---

## Testing

### Ejecutar Tests

```bash
# Todos los tests
python -m unittest discover -s tests -p "test_*.py"

# Test con cobertura
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
coverage html  # Genera reporte HTML en htmlcov/

# Tests específicos
python -m unittest tests.test_board
python -m unittest tests.test_board.TestBoard.test_mover_destino_vacio
```

### Cobertura Actual

```
TOTAL: 990 statements, 90% coverage
```

---

## Cómo Jugar

### Reglas Básicas

1. **Objetivo**: Mover todas tus fichas a tu "casa" y sacarlas del tablero antes que tu oponente

2. **Jugadores**:
   - **Jugador X**: Mueve de celdas 0-11 → 18-23 (casa en 18-23)
   - **Jugador O**: Mueve de celdas 23-12 → 5-0 (casa en 0-5)

3. **Dados**: Se lanzan dos dados por turno. Dobles te dan 4 movimientos

4. **Capturas**: Si una celda tiene solo 1 ficha enemiga, puedes capturarla

5. **Reingreso**: Si tienes fichas capturadas, debes reingresarlas antes de mover otras

### Comandos CLI

```
origen salto    - Mover ficha (ej: 12 3)
-1 dado         - Reingresar ficha capturada (ej: -1 5)
ayuda           - Mostrar ayuda completa
salir           - Salir del juego
```

### Controles Pygame

1. Click en "Tirar Dados"
2. Click en una celda con tus fichas
3. Click en un dado para seleccionarlo
4. El movimiento se ejecuta automáticamente
5. **ESC**: Cancelar selección

---

## Estructura del Proyecto

```
/backgammon/
│
├── core/                  # Lógica de negocio
│   ├── backgammon.py     # Clase principal del juego
│   ├── board.py          # Tablero (24 celdas + capturas)
│   ├── validaciones.py   # Reglas del Backgammon
│   ├── dice.py           # Generador de dados
│   ├── ficha.py          # Entidad ficha
│   ├── player.py         # Entidad jugador
│   └── exceptions.py     # Excepciones del dominio
│
├── cli/                   # Interfaz de línea de comandos
│   └── cli.py            # CLI completa
│
├── pygame_ui/            # Interfaz gráfica con Pygame
│   ├── pygame_ui.py      # UI principal
│   └── dados_ui.py       # Componentes de dados clickeables
│
├── tests/                 # Tests unitarios (90% coverage)
│   ├── test_backgammon.py
│   ├── test_board.py
│   ├── test_validaciones.py
│   ├── test_cli.py
│   ├── test_dice.py
│   ├── test_ficha.py
│   └── test_player.py
│
├── .github/workflows/    # CI/CD con GitHub Actions
│   └── ci.yml
│
├── Dockerfile            # Imagen Docker del juego
├── docker-compose.yml    # Servicios Docker
├── requirements.txt      # Dependencias Python
│
├── CHANGELOG.md          # Historial de versiones
├── JUSTIFICACION.md      # Decisiones de diseño
├── README.md             # Este archivo
└── REPORTS.md            # Reportes automáticos
```

---

## Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje principal
- **Pygame 2.5.0**: Interfaz gráfica
- **unittest**: Framework de testing
- **coverage**: Medición de cobertura de tests
- **pylint**: Análisis estático de código
- **Docker**: Containerización
- **GitHub Actions**: CI/CD automático

---

## CI/CD

El proyecto incluye integración continua con GitHub Actions:

-  Ejecución automática de tests en cada push
-  Generación de reportes de cobertura
-  Análisis con Pylint
-  Auto-merge de PRs de reportes
-  Actualización automática de REPORTS.md

---

## Documentación Adicional

- [CHANGELOG.md](CHANGELOG.md): Historial detallado de cambios (v0.0.1 → v0.5.0)
- [JUSTIFICACION.md](JUSTIFICACION.md): Decisiones de diseño y arquitectura
- [REPORTS.md](REPORTS.md): Reportes automáticos de coverage y pylint


---

## Licencia

Proyecto académico - Universidad de Mendoza
Computación 2025

---

## Contacto

**Alumno**: Luciano Agustín Fernández Actis  
**Repositorio**: [github.com/um-computacion/computacion-2025-backgammon-Luchito-xx](https://github.com/um-computacion/computacion-2025-backgammon-Luchito-xx)
