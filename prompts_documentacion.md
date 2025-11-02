## prompt 

Ayudame a realizar JUSTIFICACION.md (Adjunto contexto)

### Claude-Sonnet-4.5

### Respuesta

````
# Justificación del Proyecto Backgammon

**Alumno**: Luciano Agustín Fernández Actis  
**Materia**: Computación 2025

---

## 1. Resumen del Diseño General

El proyecto implementa un juego completo de Backgammon en Python siguiendo una arquitectura por capas que separa claramente:

- **Lógica de Negocio** (`core/`): Contiene todas las clases que implementan las reglas y mecánicas del juego
- **Interfaces de Usuario** (`cli/`, `pygame_ui/`): Dos modalidades de interacción totalmente independientes de la lógica
- **Testing** (`tests/`): Suite completa de pruebas unitarias

Esta separación permite que la lógica del juego sea completamente independiente de cómo se presenta al usuario, cumpliendo con los requisitos del proyecto de tener tanto una interfaz CLI (obligatoria) como una interfaz gráfica con Pygame (obligatoria).

El diseño se basa en el principio de **separación de concerns**, donde cada módulo tiene una responsabilidad bien definida y puede evolucionar independientemente.

---

## 2. Justificación de las Clases Elegidas

### 2.1. Clase `Backgammon` (Orquestador Principal)

**Ubicación**: `core/backgammon.py`

**Responsabilidad Única**: Coordinar el flujo general del juego entre todos los componentes (Board, Dice, Player, Validaciones).

**Justificación de su Existencia**:
Esta clase actúa como **Controlador/Coordinador** del juego. Su existencia es fundamental porque:
- Encapsula la lógica de flujo (turnos, inicio, fin de partida)
- Proporciona una API unificada para las interfaces de usuario
- Gestiona el estado global del juego (quién juega, dados disponibles, ganador)
- Permite que las UIs no tengan que conocer los detalles internos de Board o Validaciones

**Por qué NO fusionarla con otras clases**:
- Si estuviera en `Board`: La clase Board se encargaría de estructura Y flujo (viola SRP)
- Si estuviera en `CLI`: No podríamos tener múltiples interfaces
- Solución adoptada: Clase independiente que coordina sin implementar lógica de negocio

**Métodos clave y su justificación**:
- `inicio()`: Inicializa el juego y determina primer jugador (lógica compleja que no corresponde a Board)
- `mover(celda, salto)`: Coordina validación → ejecución → verificación de victoria
- `puede_mover()`: Delega en Validaciones para saber si hay jugadas posibles (necesario para cambio automático de turno)
- `mostrar()`: Retorna estado completo en formato agnóstico a la UI

### 2.2. Clase `Board` (Estructura y Estado del Tablero)

**Ubicación**: `core/board.py`

**Responsabilidad Única**: Mantener y modificar el estado físico del tablero (posiciones de fichas, capturas).

**Justificación de su Existencia**:
Representa la estructura de datos del tablero de Backgammon. Su existencia es necesaria porque:
- El tablero es una entidad compleja (24 posiciones + barra de capturas)
- Requiere operaciones específicas (mover fichas, capturar, reingresar)
- Necesita una representación visual (`get_board()`)

**Evolución de Diseño** (ver CHANGELOG v0.3.0):
Originalmente `Board` contenía validaciones de reglas, lo que generaba:
- Duplicación con la clase `Validaciones`
- Responsabilidades mezcladas (estructura + reglas)
- Dificultad para testear independientemente

**Refactor realizado**: Se extrajeron todas las validaciones a `Validaciones`, dejando a `Board` con responsabilidad única de estructura.

**Métodos clave**:
- `inicio()`: Configura posiciones iniciales según reglas oficiales
- `mover(celda, salto, jugador)`: Ejecuta el movimiento (sin validar, eso es responsabilidad de Validaciones)
- `get_board()`: Genera representación visual del tablero para la CLI
- `get_celdas()`, `get_capturas()`: Exponen estado para validación

### 2.3. Clase `Validaciones` (Motor de Reglas)

**Ubicación**: `core/validaciones.py`

**Responsabilidad Única**: Verificar todas las reglas del juego de Backgammon.

**Justificación de su Existencia**:
Las reglas de Backgammon son complejas y requieren centralización:
- Validación de movimientos normales
- Reglas especiales de captura
- Condiciones de reingreso desde la barra
- Reglas de salida del tablero
- Detección de victoria
- Verificación de movimientos posibles

**Decisión de Diseño: Métodos Estáticos (`@staticmethod`)**

**Justificación**:
- Las validaciones son funciones puras: mismo input → mismo output
- No requieren mantener estado entre llamadas
- Facilitan el testing (no necesitan instanciar objeto)
- Permiten llamadas directas sin crear instancias innecesarias

**Alternativas consideradas y descartadas**:
1. **Validaciones dentro de Board**: Rechazada porque viola SRP
2. **Validaciones como funciones libres**: Rechazada porque no hay encapsulamiento ni namespace claro
3. **Instancia de Validaciones**: Rechazada porque agregaría complejidad sin beneficio (no hay estado)

**Métodos clave**:
- `movimiento_valido()`: Punto de entrada principal, orquesta todas las validaciones
- `validar_reingreso()`: Lógica específica para fichas capturadas
- `validar_salida()`: Verifica condiciones para sacar fichas (todas en casa, sin capturas)
- `validar_victoria()`: Determina si un jugador ganó (0 fichas en juego)
- `puede_mover()`: Busca exhaustivamente si existe algún movimiento legal (clave para UX)

### 2.4. Clase `Ficha` (Entidad Mínima)

**Ubicación**: `core/ficha.py`

**Responsabilidad Única**: Representar una ficha individual del juego.

**Justificación de su Existencia**:
Aunque es una clase simple, encapsula el concepto de "ficha" con:
- Identidad del propietario (jugador X u O)
- Estado (en juego o capturada)

**¿Por qué no usar simplemente strings?**

Alternativa descartada: `celdas[0] = ["X", "X", "X"]`

**Problemas**:
- No hay manera de marcar fichas como capturadas
- No hay encapsulamiento
- Dificulta futuras extensiones

**Solución adoptada**: Clase `Ficha` con atributos privados

**Beneficios**:
- Permite atributo `__capturada__` para lógica de barra
- Facilita extensiones futuras (ej: fichas con colores, efectos)
- Mejor semántica: `ficha.get_jugador()` vs `string[0]`

### 2.5. Clase `Player` (Representación de Jugador)

**Ubicación**: `core/player.py`

**Responsabilidad Única**: Representar a un jugador del juego.

**Justificación de su Existencia**:
Actualmente solo almacena el nombre/identificador, pero existe porque:
- Encapsula el concepto de "jugador"
- Facilita futuras extensiones sin romper código existente
- Mejora la legibilidad: `player.get_name()` vs acceder directamente a string

**Extensiones futuras posibles**:
- Estadísticas (partidas ganadas, movimientos realizados)
- Estrategia de juego (humano vs IA)
- Configuración de colores/avatares en UI

### 2.6. Clase `Dice` (Generador de Aleatoriedad)

**Ubicación**: `core/dice.py`

**Responsabilidad Única**: Generar valores aleatorios de dados.

**Justificación de su Existencia**:
- Encapsula la lógica de dados dobles (si sale 3-3, retorna `[3, 3, 3, 3]`)
- Facilita el testing mediante inyección de dependencias
- Centraliza el comportamiento de aleatoriedad

**Beneficio clave para Testing**:
```python
# En producción
game = Backgammon()  # Usa Dice real

# En tests
fake_dice = FakeDice([[4, 1]])  # Dados predecibles
game = Backgammon(dice=fake_dice)
```

### 2.7. Clase `BackgammonCLI` (Interfaz de Línea de Comandos)

**Ubicación**: `cli/cli.py`

**Responsabilidad Única**: Gestionar la interacción del usuario por consola.

**Justificación de su Existencia**:
Separa completamente la presentación de la lógica:
- Maneja input/output de consola
- Formatea mensajes para el usuario
- Traduce comandos de texto a llamadas a `Backgammon`
- Gestiona el loop de juego en modo CLI

**Cumplimiento de Requisitos**: Modalidad CLI es **obligatoria** según consigna (punto 3.5.1).

**Métodos clave**:
- `jugar()`: Bucle principal del juego
- `obtener_movimiento()`: Parser de comandos del usuario
- `mostrar_estado_juego()`: Formatea y muestra tablero + información
- `movimiento()`: Procesa el movimiento y maneja errores

### 2.8. Clases de Pygame UI (Interfaz Gráfica)

**Ubicación**: `pygame_ui/`

**Clases**:
1. `PygameUI`: Controlador principal de la UI gráfica
2. `DadoUI`: Representa un dado clickeable
3. `GestorDados`: Gestiona múltiples dados y su selección

**Responsabilidad**: Renderizar el juego gráficamente y capturar eventos de mouse/teclado.

**Justificación de Múltiples Clases**:
- `PygameUI`: Demasiado complejo para una sola clase (pantallas, eventos, dibujo)
- `DadoUI`: Componente reutilizable con estado propio (seleccionado, usado)
- `GestorDados`: Patrón Manager para coordinar múltiples dados

**Cumplimiento de Requisitos**: Modalidad Pygame es **obligatoria** según consigna (punto 3.5.2).

**Decisión de Diseño: Dados Clickeables**:
En lugar de input de texto, el usuario:
1. Hace click en una celda
2. Hace click en un dado
3. El movimiento se ejecuta automáticamente

Esto mejora la UX y demuestra manejo de eventos en Pygame.

---

## 3. Justificación de Atributos

### 3.1. Convención de Nomenclatura: `__atributo__`

**Requisito de la Consigna** (punto 6):
> "Todos los atributos de todas las clases deben contener como prefijo y postfijo los símbolos "__""

**Cumplimiento**: Todos los atributos usan `__nombre__`.

**Ejemplo**:
```python
class Board:
    def __init__(self):
        self.__celdas__ = [[] for _ in range(24)]  # ✅ Correcto
        self.__capturas__ = []                      # ✅ Correcto
```

**Justificación Técnica**:
- Refuerza el encapsulamiento
- Obliga al uso de getters/setters
- Evita acceso directo desde fuera de la clase
- Cumple con la consigna del proyecto

### 3.2. Atributos de la Clase `Backgammon`

```python
self.__board__ = Board()
self.__players__ = [Player("X"), Player("O")]
self.__dice__ = Dice()
self.__turno__ = 0  # Índice del jugador actual
self.__saltos__ = []  # Dados disponibles
self.__ganador__ = None  # Player o None
```

**Justificación de cada atributo**:

1. **`__board__`**: Instancia de Board
   - **Tipo**: Objeto
   - **Por qué**: El tablero es una entidad compleja que merece su propia clase
   - **Alternativa descartada**: Lista plana de 24 elementos (no encapsula comportamiento)

2. **`__players__`**: Lista de 2 jugadores
   - **Tipo**: `list[Player]`
   - **Por qué**: Permite iterar fácilmente y extender a más jugadores en el futuro
   - **Por qué lista y no tupla**: Aunque actualmente son 2 jugadores fijos, lista da flexibilidad

3. **`__dice__`**: Instancia de Dice
   - **Tipo**: Objeto
   - **Por qué**: Permite inyección de dependencias para testing (FakeDice)
   - **Por qué no usar random.randint directamente**: No sería testeable

4. **`__turno__`**: Índice del jugador actual (0 o 1)
   - **Tipo**: `int`
   - **Por qué int y no Player**: Más simple para alternar (`1 - turno`)
   - **Alternativa descartada**: Almacenar Player directamente (más complejo de alternar)

5. **`__saltos__`**: Lista de movimientos disponibles
   - **Tipo**: `list[int]`
   - **Por qué lista**: Los dados se consumen uno por uno (mutabilidad necesaria)
   - **Ejemplo**: `[3, 5]` o `[4, 4, 4, 4]` para dobles

6. **`__ganador__`**: Jugador que ganó o None
   - **Tipo**: `Player | None`
   - **Por qué nullable**: Indica si hay ganador o sigue la partida

### 3.3. Atributos de la Clase `Board`

```python
self.__celdas__ = [[] for _ in range(24)]
self.__capturas__ = []
```

**Justificación**:

1. **`__celdas__`**: Lista de 24 listas (posiciones del tablero)
   - **Tipo**: `list[list[Ficha]]`
   - **Por qué lista de listas**: Cada posición puede tener múltiples fichas apiladas
   - **Por qué no diccionario**: Los índices 0-23 mapean naturalmente a posiciones
   - **Ejemplo**: `celdas[0] = [Ficha("X"), Ficha("X")]` (2 fichas X en posición 0)

2. **`__capturas__`**: Lista de fichas en la barra
   - **Tipo**: `list[Ficha]`
   - **Por qué lista**: Puede haber múltiples fichas capturadas de ambos jugadores
   - **Alternativa descartada**: Dict por jugador (más complejo sin beneficio)

### 3.4. Atributos de `PygameUI`

```python
self.__screen__ = pygame.display.set_mode((1000, 700))
self.__colors__ = {...}  # Diccionario de colores
self.__fonts__ = {...}   # Diccionario de fuentes
self.__celda_seleccionada__ = None
self.__gestor_dados__ = GestorDados()
self.__estado__ = 'menu'  # 'menu', 'jugando', 'victoria'
```

**Justificación**:

- **`__colors__`**: Diccionario en lugar de constantes
  - **Por qué**: Centraliza paleta de colores, fácil de modificar
  - **Beneficio**: `self.__colors__['background']` es más legible que `BACKGROUND_COLOR`

- **`__estado__`**: String en lugar de enum
  - **Por qué**: Python no requiere enums para valores simples
  - **Valores**: 'menu', 'jugando', 'victoria'

---

## 4. Decisiones de Diseño Relevantes

### 4.1. Separación Core / UI (Arquitectura Fundamental)

**Decisión**: Lógica de negocio (`core/`) completamente independiente de las interfaces.

**Justificación**:
- Requisito explícito de la consigna (punto 1 y 3.1)
- Permite tener múltiples UIs sin duplicar lógica
- Facilita testing (la lógica se testea sin UI)

**Implementación**:
```
core/          → Lógica pura (no imports de cli ni pygame)
cli/           → Solo importa de core
pygame_ui/     → Solo importa de core
```

**Beneficio Real**: Ambas interfaces comparten exactamente la misma lógica validada.

### 4.2. Validaciones Centralizadas (Refactor Importante)

**Problema Original** (v0.0.1 - v0.2.0):
- Validaciones en `Board.mover()`
- Validaciones en `Backgammon.mover()`
- Validaciones en `Validaciones`
- **Resultado**: Código duplicado, inconsistencias

**Decisión** (v0.3.0):
- **Todas** las validaciones en `Validaciones`
- `Board.mover()` solo ejecuta (asume válido)
- `Backgammon.mover()` delega validación

**Implementación**:
```python
# En Backgammon.mover()
if not Validaciones.movimiento_valido(...):
    raise ValueError("Movimiento inválido")

self.__board__.mover(celda, salto, jugador)  # Ya validado
```

**Beneficio**:
- Una sola fuente de verdad para reglas
- Testing más simple (solo testear Validaciones)
- Cambios en reglas solo requieren modificar Validaciones

### 4.3. Inyección de Dependencias para Testing

**Decisión**: Constructor de `Backgammon` acepta parámetros opcionales.

**Implementación**:
```python
def __init__(self, board=None, players=None, dice=None):
    self.__board__ = board if board else Board()
    self.__dice__ = dice if dice else Dice()
    # ...
```

**Justificación**:
- En producción: `Backgammon()` usa implementaciones reales
- En testing: `Backgammon(dice=FakeDice([3, 5]))` usa mock

**Beneficio**:
```python
# Test predecible
class FakeDice:
    def roll(self):
        return [4, 1]  # Siempre retorna esto

game = Backgammon(dice=FakeDice())
# Ahora podemos testear sin aleatoriedad
```

### 4.4. Sistema Jerárquico de Excepciones

**Decisión**: Todas las excepciones del dominio heredan de `BackgammonError`.

**Implementación**:
```python
class BackgammonError(Exception):
    """Clase base"""

class FueraDeRangoError(BackgammonError):
    """Celda fuera de 0-23"""

class CeldaBloqueadaError(BackgammonError):
    """Destino bloqueado por enemigo"""
```

**Justificación**:
- Permite captura genérica: `except BackgammonError`
- Permite captura específica: `except CeldaBloqueadaError`
- Separa errores de dominio de errores técnicos

**Uso en CLI**:
```python
try:
    self.game.mover(origen, salto)
except BackgammonError as e:
    print(f"Movimiento inválido: {e}")  # Esperado
except Exception as e:
    print(f"Error inesperado: {e}")  # Bug
```

### 4.5. Método `puede_mover()` para UX

**Problema**: Usuario sin movimientos posibles quedaba atascado.

**Decisión**: Implementar `Validaciones.puede_mover()` que busca exhaustivamente.

**Implementación**:
```python
def puede_mover(celdas, capturas, saltos, jugador):
    if not saltos:
        return False
    
    # Probar todas las combinaciones origen-salto
    for salto in saltos:
        for origen in range(24):
            try:
                if movimiento_valido(celdas, capturas, origen, salto, jugador):
                    return True
            except BackgammonError:
                continue
    
    return False
```

**Uso en Backgammon**:
```python
if not self.puede_mover():
    print("Sin movimientos, cambiando turno")
    self.cambio_turno()
```

**Beneficio**: El juego avanza automáticamente cuando no hay opciones.

### 4.6. Representación Visual del Tablero (`Board.get_board()`)

**Decisión**: Generar string formateado para CLI.

**Implementación**:
```python
def get_board(self):
    # Fila superior: 23, 22, 21... 18 | 17, 16... 12
    # Barra central
    # Fila inferior: 11, 10, 9... 6 | 5, 4... 0
```

**Salida**:
```
 23  22  21  20  19  18 |  17  16  15  14  13  12
 O2  --  --  --  X5  -- |  X3  --  --  --  --  O5
                        |
------------------------------------------------
                        |
 X2  --  --  --  O5  -- |  O3  --  --  --  --  X5
 11  10   9   8   7   6 |   5   4   3   2   1   0
```

**Justificación**:
- Visualización clara de ambos lados del tablero
- Barra central visible (donde van fichas capturadas)
- Numeración correcta según convención de Backgammon

---

## 5. Excepciones y Manejo de Errores

### 5.1. Jerarquía Completa

```
Exception
└── BackgammonError (base del dominio)
    ├── FueraDeRangoError (índice < 0 o > 23)
    ├── CeldaInvalidaError (celda vacía)
    ├── ValidacionError (error genérico de validación)
    ├── CeldaBloqueadaError (destino bloqueado por 2+ fichas enemigas)
    ├── FichasCapturadasError (debe reingresar primero)
    ├── SinFichasCapturadas (intentó reingresar sin capturas)
    ├── ReingresoInvalidoError (reingreso bloqueado)
    ├── SalidaInvalidaError (no puede sacar fichas)
    └── SaltosError (no tiró dados)
```

### 5.2. Justificación de Cada Excepción

**`BackgammonError`**: Clase base
- **Por qué**: Permite `except BackgammonError` para capturar cualquier error del juego
- **Uso**: En CLI para distinguir errores esperados de bugs

**`FueraDeRangoError`**: Celda fuera de rango 0-23
- **Cuándo se lanza**: `validaciones.py` línea 74 si celda < 0 o > 23
- **Ejemplo**: Usuario ingresa `25 3`

**`CeldaBloqueadaError`**: Destino ocupado por 2+ fichas enemigas
- **Cuándo se lanza**: `validaciones.py` línea 64-66 si destino bloqueado
- **Ejemplo**: Jugador X intenta mover a celda con O-O

**`FichasCapturadasError`**: Jugador tiene fichas en barra
- **Cuándo se lanza**: `validaciones.py` línea 38 si intenta mover sin reingresar
- **Ejemplo**: Jugador X tiene ficha capturada e intenta mover desde celda 5

**`SalidaInvalidaError`**: No cumple condiciones para sacar fichas
- **Cuándo se lanza**: `validaciones.py` línea 182, 192-193
- **Ejemplo**: Jugador X intenta sacar fichas pero tiene una en celda 10

**`SaltosError`**: No tiró dados antes de mover
- **Cuándo se lanza**: `backgammon.py` línea 128
- **Ejemplo**: Usuario intenta mover sin tirar dados primero

### 5.3. Estrategia de Manejo en CLI

```python
def _procesar_movimiento(self, entrada):
    try:
        origen = int(partes[0])
        salto = int(partes[1])
        self.game.mover(origen, salto)
        
    except BackgammonError as e:
        # Errores de dominio (esperados)
        print(f"Movimiento inválido: {e}")
        self.pausar()
        return True  # Continuar turno
        
    except ValueError:
        # Entrada no numérica
        print("Debes usar números enteros")
        return True
        
    except KeyboardInterrupt:
        # Usuario presionó Ctrl+C
        print("¿Quieres salir? (s/n)")
        return None if input() == 's' else True
```

**Justificación**:
- Errores de dominio: Mensaje amigable, usuario reintenta
- Errores de sintaxis: Mensaje educativo sobre formato
- Interrupciones: Confirmación antes de salir

---

## 6. Estrategias de Testing y Cobertura

### 6.1. Cobertura Actual: 92%

**Distribución**:
```
core/backgammon.py     → 80%  (líneas 68, 107, 117, 128, etc.)
core/board.py          → 88%  (líneas 53, 80-83, 153-155)
core/dice.py           → 100%
core/ficha.py          → 100%
core/player.py         → 100%
core/validaciones.py   → 80%  (líneas 38, 68, 71, 86, etc.)
core/exceptions.py     → 100%
──────────────────────────────
TOTAL                  → 92%
```

**Cumplimiento de Requisito** (punto 4.1):
> "Se deberá alcanzar al menos 90% de cobertura con pruebas unitarias"

✅ **92% > 90%** - Requisito cumplido

### 6.2. Estrategia de Testing por Módulo

#### 6.2.1. `test_backgammon.py` (47 statements, 96% coverage)

**Qué se probó**:
- Inicialización del juego con todas las dependencias
- Selección de turno inicial (dados diferentes)
- Flujo completo: tirar dados → mover → consumir dado
- Error `SaltosError` al mover sin tirar dados

**Por qué estos tests**:
- `turno_inicial()` tiene lógica compleja (loop hasta dados diferentes)
- `mover()` coordina múltiples componentes (debe integrarse correctamente)
- Verificar que saltos se consumen es crítico para la jugabilidad

**Técnicas usadas**:
```python
class FakeDice:
    def __init__(self, rolls):
        self._rolls = list(rolls)
    
    def roll(self):
        return self._rolls.pop(0)

# Uso en test
game = Backgammon(dice=FakeDice([[4, 1]]))
```

**Justificación**: Inyección de dependencias permite tests predecibles sin aleatoriedad.

#### 6.2.2. `test_board.py` (134 statements, 96% coverage)

**Qué se probó**:
- Representación visual correcta del tablero (`get_board()`)
- Movimiento a destino vacío
- Movimiento a destino con fichas propias (apilado)
- Captura de ficha enemiga solitaria
- Reingreso desde barra
- Salida de tablero (sacar fichas)

**Por qué estos tests**:
- `get_board()` es usado en CLI (debe ser legible)
- Capturas son parte fundamental del juego
- Reingresos tienen lógica especial (inversión de dirección)

**Tests destacados**:
```python
def test_mover_destino_capturar_enemigo(self):
    c[origen] = [Ficha("X")]
    c[destino] = [Ficha("O")]  # Una sola ficha enemiga
    
    b.mover(origen, destino - origen, "X")
    
    # Verificar que O fue capturada
    self.assertEqual(len(b.get_capturas()), 1)
    self.assertEqual(b.get_capturas()[0].get_jugador(), "O")
```

**Justificación**: Las capturas deben mover la ficha enemiga a la barra (no eliminarla).

#### 6.2.3. `test_validaciones.py` (84 statements, 100% coverage)

**Qué se probó**:
- Movimientos válidos para X y O (direcciones opuestas)
- Validación de salida (con/sin capturas, con/sin fichas fuera de casa)
- Validación de victoria (sin fichas en tablero ni capturas)
- `puede_mover()` en múltiples escenarios

**Por qué 100% de cobertura**:
- `Validaciones` es el corazón del juego (todas las reglas)
- Errores en validaciones rompen la jugabilidad
- Tests exhaustivos garantizan consistencia

**Test crítico**:
```python
def test_puede_mover_false_no_movimientos_validos(self):
    celdas[1] = [Ficha("O"), Ficha("O")]  # Bloqueado
    celdas[0] = [Ficha("X")]
    saltos = [1, 1]
    
    # X no puede moverse (única salida bloqueada)
    self.assertFalse(Validaciones.puede_mover(...))
```

**Justificación**: Evita que el juego se atasque cuando no hay movimientos.

#### 6.2.4. `test_dice.py` (26 statements, 96% coverage)

**Qué se probó**:
- Creación de dados con valores por defecto
- Valores dentro de rango 1-6
- Dados dobles

````

#### Implementacion

Se cambian varias cosas pero es muy buen punto de partida

implementacion final en JUSTIFIACION.md del repo

