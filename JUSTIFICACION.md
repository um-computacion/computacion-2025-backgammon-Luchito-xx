# Justificación del Proyecto Backgammon

## 1. Resumen del Diseño General

Arquitectura por capas aplicado:

- **Capa de Negocio** (`core/`): Lógica pura del juego
- **Capa de Presentación** (`cli/`, `pygame_ui/`): Interfaces de usuario
- **Capa de Testing** (`tests/`): Validación de funcionalidad

Esta separación permite que la lógica del juego sea independiente de cómo se presenta, facilitando la extensibilidad y el mantenimiento.

## 2. Diseño de Clases y Responsabilidades

### 2.1. Clase `Backgammon` (Orquestador)
**Responsabilidad**: Coordinar el flujo del juego entre todos los componentes.

**Justificación**: Proporcionan una interfaz simplificada para que las capas de presentación interactúen con el juego sin conocer los detalles internos de Board, Validaciones o Dice.

**Atributos**: 

**Métodos**:

### 2.2. Clase `Board` (Estructura de Datos)
**Responsabilidad**: Mantener y modificar el estado del tablero.

**Justificación**: Enfocarse únicamente en la estructura del tablero, sin validar reglas. 

**Atributos**:

**Metodos**:

### 2.3. Clase `Validaciones` (Reglas del Juego)
**Responsabilidad**: Verificar todas las reglas de Backgammon.

**Justificación**: Centraliza toda la lógica de validación, evitando duplicación. Usa métodos estáticos (`@staticmethod`) porque no requiere mantener estado entre llamadas.

**Atributos**

**Métodos**:


### 2.4. Clase `Ficha` (Entidad)
**Responsabilidad**: Representar una ficha individual.

**Justificación**: Encapsula el concepto de ficha con su propietario y estado. 

**Atributos**:

**Metodos**:

### 2.5. Clase `Player` (Entidad)
**Responsabilidad**: Representar a un jugador.

**Justificación**: Aunque actualmente solo almacena un nombre, permite futuras extensiones como estadísticas, puntuación acumulada, o estrategias de IA.

### 2.6. Clase `Dice` (Generador de Aleatoriedad)
**Responsabilidad**: Generar valores aleatorios de dados.

**Justificación**: Encapsula la lógica de dados dobles (retorna 4 valores) y facilita el testing mediante inyección de dependencias (mock).

### 2.7. Clase `BackgammonCLI` (Interfaz de Usuario)
**Responsabilidad**: Gestionar la interacción por consola.

**Justificación**: Separa completamente la UI de la lógica. No conoce detalles internos de `Board` o `Validaciones`, solo consume la API pública de `Backgammon`.

### 2.8. Clases `PygameUI`, `DadoUI`, `GestorDados` (Interfaz Gráfica)
**Responsabilidad**: Renderizar y gestionar interacción gráfica.

**Justificación**: 
- `PygameUI`: Controlador principal de la UI gráfica
- `DadoUI`: Representa un dado clickeable (componente reutilizable)
- `GestorDados`: Gestiona múltiples dados y su selección (patrón *Manager*)

## 4. Excepciones y Manejo de Errores

### Jerarquía de Excepciones
```
BackgammonError (base)
├── FueraDeRangoError
├── CeldaInvalidaError
├── CeldaBloqueadaError
├── FichasCapturadasError
├── SinFichasCapturadas
├── ReingresoInvalidoError
├── SalidaInvalidaError
└── SaltosError
```

**Justificación**: 
- **Clase base común**: Permite capturar todas las excepciones del dominio con `except BackgammonError`
- **Excepciones específicas**: Facilitan el manejo granular de errores en la UI
- **Semántica clara**: Cada excepción describe exactamente qué regla se violó

**Uso en CLI**: La CLI captura `BackgammonError` para errores esperados del juego y `Exception` genérica para errores inesperados, mostrando mensajes apropiados al usuario.

## 5. Estrategia de Testing y Cobertura

### Cobertura Actual:

### Enfoque de Testing

- **Tests unitarios por módulo**: Cada clase tiene su suite de tests
- **Uso de mocks**: Para aislar componentes (ej: `FakeDice` en tests de `Backgammon`)

### Tests
1. **`test_board.py`**: 
   - Movimientos normales, capturas, reingresos
   - Salidas de tablero permitidas/bloqueadas
   - Representación visual correcta

2. **`test_validaciones.py`**:
   - Todas las reglas de Backgammon
   - Validación de salida con fichas fuera de casa
   - `puede_mover()` con diferentes escenarios

3. **`test_backgammon.py`**:
   - Flujo completo del juego
   - Integración entre componentes
   - Consumo correcto de dados

## 6. Aplicación de Principios SOLID

### S - Single Responsibility Principle 
Cada clase tiene una única razón para cambiar:
- `Board`: Solo cambia si cambia la estructura del tablero
- `Validaciones`: Solo cambia si cambian las reglas
- `Backgammon`: Solo cambia si cambia el flujo del juego
- `CLI`/`PygameUI`: Solo cambian si cambia la interfaz de usuario

### O - Open/Closed Principle 
- Las clases están abiertas a extensión (herencia, composición) pero cerradas a modificación
- Ejemplo: Agregar una nueva UI no requiere modificar `Backgammon`
- `Validaciones` puede extenderse con nuevas reglas sin modificar las existentes

### L - Liskov Substitution Principle 
- No hay jerarquías de herencia complejas (diseño simple)
- Las excepciones heredan correctamente de `BackgammonError`

### I - Interface Segregation Principle 
- `Backgammon` expone solo métodos necesarios para las UIs (`mover()`, `mostrar()`, `tirar_dado()`)
- Las UIs no dependen de métodos que no usan

### D - Dependency Inversion Principle 
- `Backgammon` acepta instancias de `Board`, `Dice`, `Player` en su constructor (inyección de dependencias)
- Facilita testing con mocks (ej: `FakeDice`)
- Las UIs dependen de la abstracción `Backgammon`, no de detalles internos

### 9 Reglas de backgammon cumplidas

### 10 Diagrama de Clases (UML)

### 11 Flujo de un Movimiento

