"""
Módulo PygameUI - Interfaz gráfica para Backgammon.

Implementa la interfaz gráfica del juego usando Pygame, permitiendo
interacción visual con el tablero mediante mouse y teclado.
"""

import sys
import pygame

from core.backgammon import Backgammon
from core.exceptions import BackgammonError
from pygame_ui.dados_ui import GestorDados 


class PygameUI:
    """
    Interfaz gráfica para el juego de Backgammon usando Pygame.
    
    Atributos:
        __game__ (Backgammon): Instancia del juego.
        __screen__ (pygame.Surface): Superficie principal de dibujo.
        __clock__ (pygame.Clock): Reloj para controlar FPS.
        __width__ (int): Ancho de la ventana.
        __height__ (int): Alto de la ventana.
        __colors__ (dict): Diccionario de colores para el UI.
        __fonts__ (dict): Diccionario de fuentes.
        __celda_seleccionada__ (int|None): Celda actualmente seleccionada.
        __gestor_dados__ (GestorDados): Gestor de dados visuales.
        __estado__ (str): Estado actual de la UI ('menu', 'jugando', 'victoria').
    """
    
    # Constantes de diseño
    BOARD_WIDTH = 800
    BOARD_HEIGHT = 600
    POINT_WIDTH = 60
    POINT_HEIGHT = 200
    FICHA_RADIUS = 25
    
    def __init__(self):
        """Inicializa Pygame y configura la ventana del juego."""
        pygame.init()
        
        self.__width__ = 1000
        self.__height__ = 700
        self.__screen__ = pygame.display.set_mode((self.__width__, self.__height__))
        pygame.display.set_caption("Backgammon")
        
        self.__clock__ = pygame.time.Clock()
        self.__game__ = Backgammon()
        self.__gestor_dados__ = GestorDados()  
        
        # Configuración de colores
        self.__colors__ = {
            'background': (34, 139, 34),  # Verde oscuro
            'board': (139, 69, 19),  # Marrón
            'point_light': (222, 184, 135),  # Beige claro
            'point_dark': (139, 90, 43),  # Marrón oscuro
            'ficha_x': (255, 255, 255),  # Blanco
            'ficha_o': (0, 0, 0),  # Negro
            'outline': (0, 0, 0),  # Negro
            'selected': (255, 215, 0),  # Dorado
            'valid_move': (144, 238, 144),  # Verde claro
            'button': (70, 130, 180),  # Azul acero
            'button_hover': (100, 149, 237),  # Azul más claro
            'text': (255, 255, 255),  # Blanco
            'bar': (101, 67, 33)  # Marrón medio
        }
        
        # Configuración de fuentes
        self.__fonts__ = {
            'title': pygame.font.Font(None, 48),
            'normal': pygame.font.Font(None, 32),
            'small': pygame.font.Font(None, 24)
        }
        
        # Estado del juego
        self.__celda_seleccionada__ = None
        self.__estado__ = 'menu'
        self.__mensaje__ = ""
        self.__mensaje_timer__ = 0
        
        # Posiciones de elementos
        self.__board_offset_x__ = 100
        self.__board_offset_y__ = 50
        
    def ejecutar(self):
        """Bucle principal del juego con Pygame."""
        ejecutando = True
        
        while ejecutando:
            # Procesar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                    
                ejecutando = self._manejar_evento(evento)
                if not ejecutando:
                    break
            
            # Actualizar pantalla
            self._dibujar()
            pygame.display.flip()
            self.__clock__.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()
    
    def _manejar_evento(self, evento):
        """
        Maneja eventos de pygame según el estado actual.
        
        Args:
            evento: Evento de pygame a procesar.
            
        Returns:
            bool: False si se debe salir, True para continuar.
        """
        if self.__estado__ == 'menu':
            return self._manejar_menu(evento)
        elif self.__estado__ == 'jugando':
            return self._manejar_juego(evento)
        elif self.__estado__ == 'victoria':
            return self._manejar_victoria(evento)
        
        return True
    
    def _manejar_menu(self, evento):
        """Maneja eventos en el menú principal."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Botón "Nuevo Juego"
            btn_rect = pygame.Rect(self.__width__//2 - 100, 300, 200, 50)
            if btn_rect.collidepoint(mouse_pos):
                self.__game__ = Backgammon()
                self.__game__.inicio()
                self.__estado__ = 'jugando'
                self.__celda_seleccionada__ = None
                self.__mensaje__ = "¡Juego iniciado!"
                self.__mensaje_timer__ = 60
                
            # Botón "Salir"
            btn_salir = pygame.Rect(self.__width__//2 - 100, 380, 200, 50)
            if btn_salir.collidepoint(mouse_pos):
                return False
                
        return True
    
    def _manejar_juego(self, evento):
        """Maneja eventos durante el juego."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # ✅ LÓGICA MEJORADA: Verificar click en botón "Tirar Dados"
            if not self.__game__.get_saltos():
                btn_dados = pygame.Rect(850, 250, 120, 40)
                if btn_dados.collidepoint(mouse_pos):
                    self.__game__.tirar_dado()
                    saltos = self.__game__.get_saltos()
                    
                    # ✅ Actualizar dados visuales
                    self.__gestor_dados__.actualizar_dados(saltos, 860, 310)
                    
                    self.__mensaje__ = f"Dados: {saltos}"
                    self.__mensaje_timer__ = 120
                    
                    # Verificar si puede mover - si no, cambiar turno automáticamente
                    if not self.__game__.puede_mover():
                        self.__mensaje__ = "Sin movimientos válidos. Cambiando turno..."
                        self.__mensaje_timer__ = 180
                        self.__game__.cambio_turno()
                        self.__gestor_dados__.actualizar_dados([], 860, 310)
                    return True
            
            # Click en dados (para seleccionar cuál usar)
            if self.__game__.get_saltos():
                valor_dado = self.__gestor_dados__.manejar_click(mouse_pos)
                if valor_dado is not None:
                    # Si hay celda seleccionada, intentar mover
                    if self.__celda_seleccionada__ is not None:
                        self._ejecutar_movimiento(self.__celda_seleccionada__, valor_dado)
                    else:
                        self.__mensaje__ = f"Dado {valor_dado} seleccionado. Elige una ficha."
                        self.__mensaje_timer__ = 60
                    return True
            
            # Click en tablero
            celda = self._obtener_celda_click(mouse_pos)
            if celda is not None:
                self._procesar_click_celda(celda)
                
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                # Deseleccionar todo
                self.__celda_seleccionada__ = None
                self.__gestor_dados__.deseleccionar_todos()
                self.__mensaje__ = "Selección cancelada"
                self.__mensaje_timer__ = 60
                
        return True
    
    def _manejar_victoria(self, evento):
        """Maneja eventos en pantalla de victoria."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Botón "Volver al Menú"
            btn_rect = pygame.Rect(self.__width__//2 - 100, 400, 200, 50)
            if btn_rect.collidepoint(mouse_pos):
                self.__estado__ = 'menu'
                
        return True
    
    def _procesar_click_celda(self, celda):
        """
        Procesa el click en una celda del tablero.
        
        Args:
            celda (int): Índice de celda clickeada (0-23) o -1 para barra.
        """
        if not self.__game__.get_saltos():
            self.__mensaje__ = "¡Tira los dados primero!"
            self.__mensaje_timer__ = 60
            return
        
        estado = self.__game__.mostrar()
        jugador_actual = estado['turno']
        celdas = self.__game__.get_celdas()
        
        # Manejo de reingreso desde la barra
        if celda == -1:
            capturas = self.__game__.get_capturas()
            tiene_capturas = any(f.get_jugador() == jugador_actual for f in capturas)
            if tiene_capturas:
                self.__celda_seleccionada__ = -1
                self.__mensaje__ = "Selecciona dado para reingresar"
                self.__mensaje_timer__ = 60
            else:
                self.__mensaje__ = "No tienes fichas capturadas"
                self.__mensaje_timer__ = 60
            return
        
        # Verificar que la celda tenga fichas del jugador actual
        if 0 <= celda <= 23 and celdas[celda]:
            if celdas[celda][0].get_jugador() == jugador_actual:
                self.__celda_seleccionada__ = celda
                self.__gestor_dados__.deseleccionar_todos()  # Reset dados
                self.__mensaje__ = f"Celda {celda} seleccionada. Elige un dado."
                self.__mensaje_timer__ = 60
            else:
                self.__mensaje__ = "¡No es tu ficha!"
                self.__mensaje_timer__ = 60
        else:
            self.__mensaje__ = "Celda vacía"
            self.__mensaje_timer__ = 60
    
    def _ejecutar_movimiento(self, origen, salto):
        """
        Ejecuta un movimiento en el juego.
        
        Args:
            origen (int): Celda origen.
            salto (int): Valor del dado.
        """
        try:
            self.__game__.mover(origen, salto)
            self.__mensaje__ = "¡Movimiento exitoso!"
            self.__mensaje_timer__ = 60
            self.__celda_seleccionada__ = None
            
            # Marcar dado como usado
            self.__gestor_dados__.marcar_dado_usado(salto)
            
            # Verificar victoria
            estado = self.__game__.mostrar()
            if estado['ganador']:
                self.__estado__ = 'victoria'
                return
            
            # Si no quedan dados, resetear visuales
            if not self.__game__.get_saltos():
                self.__gestor_dados__.actualizar_dados([], 860, 310)
                
            # Si quedan dados pero no hay más movimientos válidos, pasar turno
            elif not self.__game__.puede_mover():
                self.__mensaje__ = "No hay más movimientos válidos. Cambiando turno..."
                self.__mensaje_timer__ = 120
                self.__game__.cambio_turno()
                self.__gestor_dados__.actualizar_dados([], 860, 310)
                
        except BackgammonError as e:
            self.__mensaje__ = f"Error: {str(e)}"
            self.__mensaje_timer__ = 120
            self.__celda_seleccionada__ = None
            self.__gestor_dados__.deseleccionar_todos()
    
    def _obtener_celda_click(self, pos):
        """
        Determina qué celda fue clickeada según posición del mouse.
        
        Args:
            pos (tuple): Posición (x, y) del mouse.
            
        Returns:
            int|None: Índice de celda (0-23) o -1 para barra, None si fuera del tablero.
        """
        x, y = pos
        
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        
        # Barra central (entre columnas 6 y 7)
        barra_x = board_x + 6 * self.POINT_WIDTH
        barra_width = 40
        if barra_x <= x <= barra_x + barra_width:
            if board_y <= y <= board_y + self.BOARD_HEIGHT:
                return -1
        
        # Calcular columna relativa (0-11, saltando la barra)
        if x < board_x or x > board_x + self.BOARD_WIDTH:
            return None
        
        # MAPEO 
        x_rel = x - board_x
        
        # Columnas 0-5 (antes de la barra)
        if x_rel < 6 * self.POINT_WIDTH:
            col = x_rel // self.POINT_WIDTH
        # Después de la barra (columnas 6-11)
        elif x_rel >= (6 * self.POINT_WIDTH + barra_width):
            col = 6 + (x_rel - 6 * self.POINT_WIDTH - barra_width) // self.POINT_WIDTH
        else:
            return None  # Click en la barra
        
        if col >= 12:
            return None
        
        # Determinar si es punto superior (12-23) o inferior (0-11)
        if board_y <= y <= board_y + self.POINT_HEIGHT:
            # Puntos superiores: 23,22,21... hacia la derecha
            if col < 6:
                return 23 - col  # 23, 22, 21, 20, 19, 18
            else:
                return 17 - (col - 6)  # 17, 16, 15, 14, 13, 12
                
        elif board_y + self.BOARD_HEIGHT - self.POINT_HEIGHT <= y <= board_y + self.BOARD_HEIGHT:
            # Puntos inferiores: 11,10,9... hacia la derecha
            if col < 6:
                return 11 - col  # 11, 10, 9, 8, 7, 6
            else:
                return 5 - (col - 6)  # 5, 4, 3, 2, 1, 0
        
        return None
    
    def _dibujar(self):
        """Dibuja la pantalla según el estado actual."""
        self.__screen__.fill(self.__colors__['background'])
        
        if self.__estado__ == 'menu':
            self._dibujar_menu()
        elif self.__estado__ == 'jugando':
            self._dibujar_juego()
        elif self.__estado__ == 'victoria':
            self._dibujar_victoria()
    
    def _dibujar_menu(self):
        """Dibuja el menú principal."""
        # Título
        titulo = self.__fonts__['title'].render("BACKGAMMON", True, self.__colors__['text'])
        titulo_rect = titulo.get_rect(center=(self.__width__//2, 150))
        self.__screen__.blit(titulo, titulo_rect)
        
        # Botón "Nuevo Juego"
        mouse_pos = pygame.mouse.get_pos()
        btn_rect = pygame.Rect(self.__width__//2 - 100, 300, 200, 50)
        color_btn = self.__colors__['button_hover'] if btn_rect.collidepoint(mouse_pos) else self.__colors__['button']
        pygame.draw.rect(self.__screen__, color_btn, btn_rect, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_rect, 2, border_radius=10)
        
        texto_btn = self.__fonts__['normal'].render("Nuevo Juego", True, self.__colors__['text'])
        texto_rect = texto_btn.get_rect(center=btn_rect.center)
        self.__screen__.blit(texto_btn, texto_rect)
        
        # Botón "Salir"
        btn_salir = pygame.Rect(self.__width__//2 - 100, 380, 200, 50)
        color_salir = self.__colors__['button_hover'] if btn_salir.collidepoint(mouse_pos) else self.__colors__['button']
        pygame.draw.rect(self.__screen__, color_salir, btn_salir, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_salir, 2, border_radius=10)
        
        texto_salir = self.__fonts__['normal'].render("Salir", True, self.__colors__['text'])
        texto_rect_salir = texto_salir.get_rect(center=btn_salir.center)
        self.__screen__.blit(texto_salir, texto_rect_salir)
    
    def _dibujar_juego(self):
        """Dibuja el tablero de juego y elementos de UI."""
        # Dibujar tablero
        self._dibujar_tablero()
        
        # Dibujar panel lateral
        self._dibujar_panel_info()
        
        # ✅ Dibujar dados
        self.__gestor_dados__.dibujar(self.__screen__)
        
        # Dibujar mensaje temporal
        if self.__mensaje_timer__ > 0:
            self._dibujar_mensaje()
            self.__mensaje_timer__ -= 1
    
    def _dibujar_tablero(self):
        """Dibuja el tablero de backgammon."""
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        
        # Fondo del tablero
        board_rect = pygame.Rect(board_x, board_y, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        pygame.draw.rect(self.__screen__, self.__colors__['board'], board_rect)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], board_rect, 3)
        
        # Dibujar puntos (triángulos)
        for i in range(24):
            self._dibujar_punto(i)
        
        # Dibujar barra central
        barra_x = board_x + 6 * self.POINT_WIDTH
        barra_rect = pygame.Rect(barra_x, board_y, 40, self.BOARD_HEIGHT)
        pygame.draw.rect(self.__screen__, self.__colors__['bar'], barra_rect)
        
        # Destacar barra si está seleccionada
        if self.__celda_seleccionada__ == -1:
            pygame.draw.rect(self.__screen__, self.__colors__['selected'], barra_rect, 3)
        
        # Dibujar fichas
        self._dibujar_fichas()
    
    def _dibujar_punto(self, indice):
        """
        Dibuja un punto (triángulo) del tablero.
        
        Args:
            indice (int): Índice del punto (0-23).
        """
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        
        # Determinar color alternante
        color = self.__colors__['point_light'] if indice % 2 == 0 else self.__colors__['point_dark']
        
        # Calcular posición
        if indice >= 12:  # Puntos superiores (12-23)
            col = 23 - indice
            if col >= 6:
                col += 1  # Saltar espacio de barra
            x = board_x + col * self.POINT_WIDTH
            y = board_y
            
            # Triángulo apuntando hacia abajo
            points = [
                (x, y),
                (x + self.POINT_WIDTH, y),
                (x + self.POINT_WIDTH // 2, y + self.POINT_HEIGHT)
            ]
        else:  # Puntos inferiores (0-11)
            col = 11 - indice
            if col >= 6:
                col += 1
            x = board_x + col * self.POINT_WIDTH
            y = board_y + self.BOARD_HEIGHT
            
            # Triángulo apuntando hacia arriba
            points = [
                (x, y),
                (x + self.POINT_WIDTH, y),
                (x + self.POINT_WIDTH // 2, y - self.POINT_HEIGHT)
            ]
        
        pygame.draw.polygon(self.__screen__, color, points)
        pygame.draw.polygon(self.__screen__, self.__colors__['outline'], points, 1)
        
        # Resaltar si está seleccionado
        if self.__celda_seleccionada__ == indice:
            pygame.draw.polygon(self.__screen__, self.__colors__['selected'], points, 4)
    
    def _dibujar_fichas(self):
        """Dibuja todas las fichas en el tablero."""
        celdas = self.__game__.get_celdas()
        
        for i in range(24):
            if celdas[i]:
                self._dibujar_fichas_en_punto(i, celdas[i])
        
        # Dibujar fichas capturadas en la barra
        self._dibujar_fichas_capturadas()
    
    def _dibujar_fichas_en_punto(self, indice, fichas):
        """
        Dibuja las fichas en un punto específico.
        
        Args:
            indice (int): Índice del punto (0-23).
            fichas (list): Lista de fichas en ese punto.
        """
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        
        # Calcular posición base del punto
        if indice >= 12:
            col = 23 - indice
            if col >= 6:
                col += 1
            x = board_x + col * self.POINT_WIDTH + self.POINT_WIDTH // 2
            y = board_y + 35
            direccion = 1
        else:
            col = 11 - indice
            if col >= 6:
                col += 1
            x = board_x + col * self.POINT_WIDTH + self.POINT_WIDTH // 2
            y = board_y + self.BOARD_HEIGHT - 35
            direccion = -1
        
        # ESPACIADO
        espaciado = 45
        
        # Dibujar fichas apiladas
        for j, ficha in enumerate(fichas[:5]):  # Máximo 5 fichas visibles
            color = self.__colors__['ficha_x'] if ficha.get_jugador() == 'X' else self.__colors__['ficha_o']
            pos_y = y + (j * espaciado * direccion)
            
            pygame.draw.circle(self.__screen__, color, (x, pos_y), self.FICHA_RADIUS)
            pygame.draw.circle(self.__screen__, self.__colors__['outline'], (x, pos_y), self.FICHA_RADIUS, 2)
        
        # Si hay más de 5 fichas, mostrar número
        if len(fichas) > 5:
            texto = self.__fonts__['small'].render(str(len(fichas)), True, self.__colors__['text'])
            texto_rect = texto.get_rect(center=(x, y + 4 * espaciado * direccion))
            self.__screen__.blit(texto, texto_rect)
    
    def _dibujar_fichas_capturadas(self):
        """Dibuja las fichas capturadas en la barra central."""
        capturas = self.__game__.get_capturas()
        
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        barra_x = board_x + 6 * self.POINT_WIDTH + 20
        
        fichas_x = [f for f in capturas if f.get_jugador() == 'X']
        fichas_o = [f for f in capturas if f.get_jugador() == 'O']
        
        espaciado = 45  # Espaciado

        # Dibujar fichas X en parte superior de barra
        for i, _ in enumerate(fichas_x[:5]):
            y = board_y + 50 + i * espaciado
            pygame.draw.circle(self.__screen__, self.__colors__['ficha_x'], (barra_x, y), self.FICHA_RADIUS)
            pygame.draw.circle(self.__screen__, self.__colors__['outline'], (barra_x, y), self.FICHA_RADIUS, 2)
        
        if len(fichas_x) > 5:
            texto = self.__fonts__['small'].render(str(len(fichas_x)), True, self.__colors__['text'])
            self.__screen__.blit(texto, (barra_x - 10, board_y + 50 + 4 * espaciado))
        
        # Dibujar fichas O en parte inferior de barra
        for i, _ in enumerate(fichas_o[:5]):
            y = board_y + self.BOARD_HEIGHT - 50 - i * espaciado
            pygame.draw.circle(self.__screen__, self.__colors__['ficha_o'], (barra_x, y), self.FICHA_RADIUS)
            pygame.draw.circle(self.__screen__, self.__colors__['outline'], (barra_x, y), self.FICHA_RADIUS, 2)
        
        if len(fichas_o) > 5:
            texto = self.__fonts__['small'].render(str(len(fichas_o)), True, self.__colors__['text'])
            self.__screen__.blit(texto, (barra_x - 10, board_y + self.BOARD_HEIGHT - 50 - 4 * espaciado))
    
    def _dibujar_panel_info(self):
        """Dibuja el panel de información lateral."""
        panel_x = 850
        panel_y = 50
        
        estado = self.__game__.mostrar()
        
        # Turno actual
        turno_text = self.__fonts__['normal'].render(f"Turno: {estado['turno']}", True, self.__colors__['text'])
        self.__screen__.blit(turno_text, (panel_x, panel_y))
        
        # Instrucciones 
        inst1 = self.__fonts__['small'].render("1. Tira los dados", True, self.__colors__['text'])
        inst2 = self.__fonts__['small'].render("2. Selecciona celda a usar", True, self.__colors__['text'])
        inst3 = self.__fonts__['small'].render("3. Seleccoina dado a usar", True, self.__colors__['text'])
        inst4 = self.__fonts__['small'].render("ESC: Cancelar", True, self.__colors__['text'])
        
        self.__screen__.blit(inst1, (panel_x, panel_y + 100))
        self.__screen__.blit(inst2, (panel_x, panel_y + 125))
        self.__screen__.blit(inst3, (panel_x, panel_y + 150))
        self.__screen__.blit(inst4, (panel_x, panel_y + 175))
        
        # Botón tirar dados (solo si no hay dados activos)
        if not estado['saltos']:
            mouse_pos = pygame.mouse.get_pos()
            btn_dados = pygame.Rect(panel_x, 250, 120, 40)
            color = self.__colors__['button_hover'] if btn_dados.collidepoint(mouse_pos) else self.__colors__['button']
            pygame.draw.rect(self.__screen__, color, btn_dados, border_radius=5)
            pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_dados, 2, border_radius=5)
            
            texto = self.__fonts__['small'].render("Tirar Dados", True, self.__colors__['text'])
            texto_rect = texto.get_rect(center=btn_dados.center)
            self.__screen__.blit(texto, texto_rect)
    
    def _dibujar_mensaje(self):
        """Dibuja mensaje temporal en pantalla."""
        texto = self.__fonts__['small'].render(self.__mensaje__, True, self.__colors__['text'])
        
        # Fondo semi-transparente
        superficie = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20))
        superficie.set_alpha(200)
        superficie.fill((0, 0, 0))
        
        x = self.__width__ // 2 - superficie.get_width() // 2
        y = self.__height__ - 100
        
        self.__screen__.blit(superficie, (x, y))
        self.__screen__.blit(texto, (x + 20, y + 10))
    
    def _dibujar_victoria(self):
        """Dibuja la pantalla de victoria."""
        estado = self.__game__.mostrar()
        ganador = estado['ganador']
        
        # Título
        titulo = self.__fonts__['title'].render(f"¡Jugador {ganador} Gana!", True, self.__colors__['text'])
        titulo_rect = titulo.get_rect(center=(self.__width__//2, 200))
        self.__screen__.blit(titulo, titulo_rect)
        
        # Botón volver al menú
        mouse_pos = pygame.mouse.get_pos()
        btn_rect = pygame.Rect(self.__width__//2 - 100, 400, 200, 50)
        color = self.__colors__['button_hover'] if btn_rect.collidepoint(mouse_pos) else self.__colors__['button']
        pygame.draw.rect(self.__screen__, color, btn_rect, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_rect, 2, border_radius=10)
        
        texto = self.__fonts__['normal'].render("Volver al Menú", True, self.__colors__['text'])
        texto_rect = texto.get_rect(center=btn_rect.center)
        self.__screen__.blit(texto, texto_rect)


def main():
    """Punto de entrada para la interfaz gráfica."""
    ui = PygameUI()
    ui.ejecutar()


if __name__ == "__main__":
    main()