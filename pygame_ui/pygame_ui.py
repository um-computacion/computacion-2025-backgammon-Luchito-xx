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
    BOARD_WIDTH = 720
    BOARD_HEIGHT = 600
    POINT_WIDTH = 55
    POINT_HEIGHT = 220
    FICHA_RADIUS = 22
    PANEL_WIDTH = 250
    
    def __init__(self):
        """Inicializa Pygame y configura la ventana del juego."""
        pygame.init()
        
        self.__fullscreen__ = False
        self.__width__ = 1050
        self.__height__ = 700
        self.__screen__ = pygame.display.set_mode((self.__width__, self.__height__))
        pygame.display.set_caption("Backgammon")
        
        self.__clock__ = pygame.time.Clock()
        self.__game__ = Backgammon()
        self.__gestor_dados__ = GestorDados()  
        
        # Configuración de colores 
        self.__colors__ = {
            'background': (45, 52, 58),  # Gris oscuro azulado
            'board': (240, 240, 235),  # Beige muy claro
            'point_light': (220, 220, 215),  # Gris claro
            'point_dark': (140, 140, 135),  # Gris medio
            'ficha_x': (255, 255, 255),  # Blanco
            'ficha_o': (40, 40, 40),  # Negro
            'outline': (80, 80, 80),  # Gris oscuro
            'selected': (255, 200, 50),  # Dorado
            'valid_move': (144, 238, 144),  # Verde claro
            'button': (90, 100, 110),  # Gris azulado
            'button_hover': (120, 130, 145),  # Gris azulado claro
            'text': (255, 255, 255),  # Blanco
            'text_dark': (40, 40, 40),  # Texto oscuro
            'bar': (180, 180, 175),  # Gris claro para barra
            'panel': (55, 62, 68)  # Gris oscuro para panel
        }
        
        # Configuración de fuentes
        self.__fonts__ = {
            'title': pygame.font.Font(None, 56),
            'normal': pygame.font.Font(None, 28),
            'small': pygame.font.Font(None, 22)
        }
        
        # Estado del juego
        self.__celda_seleccionada__ = None
        self.__estado__ = 'menu'
        self.__mensaje__ = ""
        self.__mensaje_timer__ = 0
        
        # Turno inicial
        self.__turno_inicial_info__ = None
        self.__turno_inicial_timer__ = 0
        
        # Posiciones de elementos - Panel a la izquierda
        self.__panel_x__ = 20
        self.__board_offset_x__ = self.__panel_x__ + self.PANEL_WIDTH + 40
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
                if not self._manejar_evento(evento):
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
            
            # Botón "Empezar Partida"
            btn_rect = pygame.Rect(self.__width__//2 - 120, self.__height__//2 - 30, 240, 60)
            if btn_rect.collidepoint(mouse_pos):
                # Resetear juego
                self.__game__ = Backgammon()
                resultado = self.__game__.inicio()
                
                # Guardar info del turno inicial
                self.__turno_inicial_info__ = resultado
                self.__turno_inicial_timer__ = 240  # 4 segundos a 60 FPS
                
                self.__estado__ = 'jugando'
                self.__celda_seleccionada__ = None
                self.__gestor_dados__.actualizar_dados([], self.__panel_x__ + self.PANEL_WIDTH // 2 - 50, 370)
                self.__mensaje__ = "¡Juego iniciado!"
                self.__mensaje_timer__ = 60

            # Botón "Salir"
            btn_salir = pygame.Rect(self.__width__//2 - 120, self.__height__//2 + 40, 240, 60)
            if btn_salir.collidepoint(mouse_pos):
                return False
                
        return True

    def _manejar_juego(self, evento):
        """Maneja eventos durante el juego."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Verificar click en botón "Tirar Dados"
            if not self.__game__.get_saltos():
                btn_dados = pygame.Rect(self.__panel_x__ + 20, 470, self.PANEL_WIDTH - 40, 45)
                if btn_dados.collidepoint(mouse_pos):
                    self.__game__.tirar_dado()
                    
                    # Actualizar dados visuales
                    self.__gestor_dados__.actualizar_dados(self.__game__.get_saltos(), self.__panel_x__ + self.PANEL_WIDTH // 2 - 50, 370)
                    
                    self.__mensaje__ = f"Dados tirados"
                    self.__mensaje_timer__ = 120
                    
                    # Verificar si puede mover
                    if not self.__game__.puede_mover():
                        self.__mensaje__ = "Sin movimientos válidos. Cambiando turno."
                        self.__mensaje_timer__ = 200
                        self.__game__.cambio_turno()
                        self.__gestor_dados__.actualizar_dados([], self.__panel_x__ + self.PANEL_WIDTH // 2 - 50, 370)
                    return True
            
            # Botón Salir (en panel) 
            btn_salir = pygame.Rect(self.__panel_x__ + 20, self.__height__ - 110, self.PANEL_WIDTH - 40, 45)
            if btn_salir.collidepoint(mouse_pos):
                self.__estado__ = 'menu'
                return True
            
            # Click en dados (si ya hay celda seleccionada)
            if self.__game__.get_saltos() and self.__celda_seleccionada__ is not None:
                valor_dado = self.__gestor_dados__.manejar_click(mouse_pos)
                if valor_dado is not None:
                    self._ejecutar_movimiento(self.__celda_seleccionada__, valor_dado)
                    return True
            
            if self._obtener_celda_click(mouse_pos) is not None:
                self._procesar_click_celda(self._obtener_celda_click(mouse_pos))
                
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
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
            btn_rect = pygame.Rect(self.__width__//2 - 120, self.__height__//2 + 60, 240, 60)
            if btn_rect.collidepoint(mouse_pos):
                self.__estado__ = 'menu'

        return True
    
    def _procesar_click_celda(self, celda):
        """
        Procesa el click en una celda del tablero.
        
        Args:
            celda (int): Índice de celda clickeada (0-23) o -1 para barra.
        """
        
        estado = self.__game__.mostrar()
        jugador_actual = estado['turno']
        celdas = self.__game__.get_celdas()
        
        # Manejo de reingreso desde la barra
        if celda == -1:
            capturas = self.__game__.get_capturas()
            tiene_capturas = any(f.get_jugador() == jugador_actual for f in capturas)
            if tiene_capturas:
                self.__celda_seleccionada__ = -1
                self.__mensaje__ = "Barra seleccionada. Elige un dado para reingresar."
                self.__mensaje_timer__ = 90
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
                self.__mensaje_timer__ = 90
            else:
                self.__mensaje__ = "¡No es tu ficha!"
                self.__mensaje_timer__ = 90
        else:
            self.__mensaje__ = "Celda vacía"
            self.__mensaje_timer__ = 90
    
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
                self.__gestor_dados__.actualizar_dados([], self.__panel_x__ + self.PANEL_WIDTH // 2 - 50, 370)
                
            # Si quedan dados pero no hay más movimientos válidos, pasar turno
            elif not self.__game__.puede_mover():
                self.__mensaje__ = "No hay más movimientos válidos. Cambiando turno..."
                self.__mensaje_timer__ = 180
                self.__game__.cambio_turno()
                self.__gestor_dados__.actualizar_dados([], self.__panel_x__ + self.PANEL_WIDTH // 2 - 50, 370)
                
        except BackgammonError as e:
            self.__mensaje__ = f"Ups... {str(e)}"
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
        barra_width = 50
        if barra_x <= x <= barra_x + barra_width:
            if board_y <= y <= board_y + self.BOARD_HEIGHT:
                return -1
        
        # Calcular columna relativa (0-11, saltando la barra)
        if x < board_x or x > board_x + self.BOARD_WIDTH:
            return None
        
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
        
        # Determinar si es celda superior (12-23) o inferior (0-11)
        if board_y <= y <= board_y + self.POINT_HEIGHT:
            # celdas superiores: de derecha a izquierda 23 -> 12
            if col < 6:
                return 12 + col  # 12, 13, 14, 15, 16, 17
            else:
                return 18 + (col - 6)  # 18, 19, 20, 21, 22, 23
                
        elif board_y + self.BOARD_HEIGHT - self.POINT_HEIGHT <= y <= board_y + self.BOARD_HEIGHT:
            # celdas inferiores: de derecha a izquierda 11 -> 0
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
        titulo_rect = titulo.get_rect(center=(self.__width__//2, self.__height__//2 - 120))
        self.__screen__.blit(titulo, titulo_rect)
        
        # Botón "Empezar Partida"
        mouse_pos = pygame.mouse.get_pos()
        btn_rect = pygame.Rect(self.__width__//2 - 120, self.__height__//2 - 30, 240, 60)
        color_btn = self.__colors__['button_hover'] if btn_rect.collidepoint(mouse_pos) else self.__colors__['button']
        pygame.draw.rect(self.__screen__, color_btn, btn_rect, border_radius=8)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_rect, 2, border_radius=8)
        
        texto_btn = self.__fonts__['normal'].render("Empezar Partida", True, self.__colors__['text'])
        texto_rect = texto_btn.get_rect(center=btn_rect.center)
        self.__screen__.blit(texto_btn, texto_rect)

        # Botón "Salir"
        btn_salir = pygame.Rect(self.__width__//2 - 120, self.__height__//2 + 40, 240, 60)
        color_salir = self.__colors__['button_hover'] if btn_salir.collidepoint(mouse_pos) else self.__colors__['button']
        pygame.draw.rect(self.__screen__, color_salir, btn_salir, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_salir, 2, border_radius=10)
        
        texto_salir = self.__fonts__['normal'].render("Salir", True, self.__colors__['text'])
        texto_rect_salir = texto_salir.get_rect(center=btn_salir.center)
        self.__screen__.blit(texto_salir, texto_rect_salir)

    
    def _dibujar_juego(self):
        """Dibuja el tablero de juego y elementos de UI."""
        # Dibujar panel lateral
        self._dibujar_panel_info()
        
        # Dibujar tablero
        self._dibujar_tablero()
        
        # Dibujar dados
        self.__gestor_dados__.dibujar(self.__screen__)
        
        # Dibujar mensaje temporal
        if self.__mensaje_timer__ > 0:
            self._dibujar_mensaje()
            self.__mensaje_timer__ -= 1
        
        # Decrementar timer del turno inicial
        if self.__turno_inicial_timer__ > 0:
            self.__turno_inicial_timer__ -= 1
    
    def _dibujar_tablero(self):
        """Dibuja el tablero de backgammon."""
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        
        # Fondo del tablero
        board_rect = pygame.Rect(board_x, board_y, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        pygame.draw.rect(self.__screen__, self.__colors__['board'], board_rect)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], board_rect, 3)
        
        for i in range(24):
            self._dibujar_celda(i)
        
        # Dibujar barra central
        barra_x = board_x + 6 * self.POINT_WIDTH
        barra_rect = pygame.Rect(barra_x, board_y, 56, self.BOARD_HEIGHT)
        pygame.draw.rect(self.__screen__, self.__colors__['bar'], barra_rect)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], barra_rect, 3)
        
        
        # Destacar barra si está seleccionada
        if self.__celda_seleccionada__ == -1:
            pygame.draw.rect(self.__screen__, self.__colors__['selected'], barra_rect, 4)
        
        # Dibujar fichas
        self._dibujar_fichas()
    
    def _dibujar_celda(self, indice):
        """"
        Dibuja una celda (triángulo) del tablero.
        
        Args:
            indice (int): Índice del celda (0-23).
        """
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        
        # Alternar colores
        color = self.__colors__['point_light'] if indice % 2 == 0 else self.__colors__['point_dark']
        
        # Calcular posición
        if indice >= 12:  
            if indice <= 17:
                col = indice - 12
            else:
                col = 7 + (indice - 18)
            
            x = board_x + col * self.POINT_WIDTH
            y = board_y
            
            # Triángulo apuntando hacia abajo
            points = [
                (x, y),
                (x + self.POINT_WIDTH, y),
                (x + self.POINT_WIDTH // 2, y + self.POINT_HEIGHT)
            ]
        else:  
            # 6-11 en izquierda, 0-5 en derecha
            if indice >= 6:
                col = 11 - indice
            else:
                col = 7 + (5 - indice)
            
            x = board_x + col * self.POINT_WIDTH
            y = board_y + self.BOARD_HEIGHT - 2
            
            # Triángulo apuntando hacia arriba
            points = [
                (x, y),
                (x + self.POINT_WIDTH, y),
                (x + self.POINT_WIDTH // 2, y - self.POINT_HEIGHT)
            ]
        
        pygame.draw.polygon(self.__screen__, color, points)
        pygame.draw.polygon(self.__screen__, self.__colors__['outline'], points, 2)
        
        # Resaltar triángulo completo si está seleccionado
        if self.__celda_seleccionada__ == indice:
            pygame.draw.polygon(self.__screen__, self.__colors__['selected'], points, 5)
    
    def _dibujar_fichas(self):
        """Dibuja todas las fichas en el tablero."""
        celdas = self.__game__.get_celdas()
        
        for i in range(24):
            if celdas[i]:
                self._dibujar_fichas_en_celda(i, celdas[i])
        
        # Dibujar fichas capturadas en la barra
        self._dibujar_fichas_capturadas()
    
    def _dibujar_fichas_en_celda(self, indice, fichas):
        """
        Dibuja las fichas en un celda específico.
        
        Args:
            indice (int): Índice del celda (0-23).
            fichas (list): Lista de fichas en ese celda.
        """
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        
        # Calcular posición base del celda
        if indice >= 12:
            if indice <= 17:
                col = indice - 12
            else:
                col = 7 + (indice - 18)
            
            x = board_x + col * self.POINT_WIDTH + self.POINT_WIDTH // 2
            y = board_y + 25
            direccion = 1
        else:
            if indice >= 6:
                col = 11 - indice
            else:
                col = 7 + (5 - indice)
            
            x = board_x + col * self.POINT_WIDTH + self.POINT_WIDTH // 2
            y = board_y + self.BOARD_HEIGHT - 25
            direccion = -1
        
        # Espaciado entre fichas 
        espaciado = 43
        
        # Dibujar fichas apiladas (máximo 5)
        for j, ficha in enumerate(fichas[:5]):
            color = self.__colors__['ficha_x'] if ficha.get_jugador() == 'X' else self.__colors__['ficha_o']
            pos_y = y + (j * espaciado * direccion)
            
            pygame.draw.circle(self.__screen__, color, (x, pos_y), self.FICHA_RADIUS)
            pygame.draw.circle(self.__screen__, self.__colors__['outline'], (x, pos_y), self.FICHA_RADIUS, 2)
        
        # Si hay más de 5 fichas, mostrar número
        if len(fichas) > 5:
            texto = self.__fonts__['small'].render(str(len(fichas)), True, self.__colors__['text'])
            texto_rect = texto.get_rect(center=(x, y + 4 * espaciado * direccion))
            
            # Fondo para el número
            fondo = pygame.Surface((30, 25))
            fondo.set_alpha(180)
            fondo.fill((0, 0, 0))
            self.__screen__.blit(fondo, (x - 15, y + 4 * espaciado * direccion - 12))
            self.__screen__.blit(texto, texto_rect)
    
    def _dibujar_fichas_capturadas(self):
        """Dibuja las fichas capturadas en la barra central."""
        capturas = self.__game__.get_capturas()
        
        board_x = self.__board_offset_x__
        board_y = self.__board_offset_y__
        barra_x = board_x + 6 * self.POINT_WIDTH + 28
        
        fichas_x = [f for f in capturas if f.get_jugador() == 'X']
        fichas_o = [f for f in capturas if f.get_jugador() == 'O']
        
        espaciado = 43

        # Dibujar fichas X en parte superior de barra
        for i, _ in enumerate(fichas_x[:5]):
            y = board_y + 60 + i * espaciado
            pygame.draw.circle(self.__screen__, self.__colors__['ficha_x'], (barra_x, y), self.FICHA_RADIUS)
            pygame.draw.circle(self.__screen__, self.__colors__['outline'], (barra_x, y), self.FICHA_RADIUS, 2)
        
        if len(fichas_x) > 5:
            texto = self.__fonts__['small'].render(str(len(fichas_x)), True, self.__colors__['text'])
            fondo = pygame.Surface((30, 25))
            fondo.set_alpha(180)
            fondo.fill((0, 0, 0))
            self.__screen__.blit(fondo, (barra_x - 15, board_y + 60 + 4 * espaciado - 12))
            self.__screen__.blit(texto, (barra_x - 10, board_y + 60 + 4 * espaciado - 8))
        
        # Dibujar fichas O en parte inferior de barra
        for i, _ in enumerate(fichas_o[:5]):
            y = board_y + self.BOARD_HEIGHT - 60 - i * espaciado
            pygame.draw.circle(self.__screen__, self.__colors__['ficha_o'], (barra_x, y), self.FICHA_RADIUS)
            pygame.draw.circle(self.__screen__, self.__colors__['outline'], (barra_x, y), self.FICHA_RADIUS, 2)
        
        if len(fichas_o) > 5:
            texto = self.__fonts__['small'].render(str(len(fichas_o)), True, self.__colors__['text'])
            fondo = pygame.Surface((30, 25))
            fondo.set_alpha(180)
            fondo.fill((0, 0, 0))
            self.__screen__.blit(fondo, (barra_x - 15, board_y + self.BOARD_HEIGHT - 60 - 4 * espaciado - 12))
            self.__screen__.blit(texto, (barra_x - 10, board_y + self.BOARD_HEIGHT - 60 - 4 * espaciado - 8))
    
    def _dibujar_panel_info(self):
        """Dibuja el panel de información lateral."""
        panel_x = self.__panel_x__
        panel_y = 50
        
        # Fondo del panel
        panel_rect = pygame.Rect(panel_x, panel_y, self.PANEL_WIDTH, self.__height__ - 100)
        pygame.draw.rect(self.__screen__, self.__colors__['panel'], panel_rect, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], panel_rect, 2, border_radius=10)
        
        estado = self.__game__.mostrar()
        
        # Título del panel
        titulo_panel = self.__fonts__['normal'].render("INFORMACIÓN", True, self.__colors__['text'])
        self.__screen__.blit(titulo_panel, (panel_x + 40, panel_y + 20))
        
        # Línea separadora
        pygame.draw.line(self.__screen__, self.__colors__['outline'], 
                        (panel_x + 20, panel_y + 60), 
                        (panel_x + self.PANEL_WIDTH - 20, panel_y + 60), 2)
        
        # Mostrar información del turno inicial si está disponible
        if self.__turno_inicial_timer__ > 0 and self.__turno_inicial_info__:
            info = self.__turno_inicial_info__
            
            turno_titulo = self.__fonts__['small'].render("TURNO INICIAL:", True, self.__colors__['text'])
            self.__screen__.blit(turno_titulo, (panel_x + 20, panel_y + 80))
            
            dado_x = self.__fonts__['small'].render(f"Jugador X: {info['dados_x']}", True, self.__colors__['text'])
            self.__screen__.blit(dado_x, (panel_x + 30, panel_y + 110))
            
            dado_o = self.__fonts__['small'].render(f"Jugador O: {info['dados_o']}", True, self.__colors__['text'])
            self.__screen__.blit(dado_o, (panel_x + 30, panel_y + 135))
            
            ganador = self.__fonts__['normal'].render(f"¡Empieza {info['ganador']}!", True, self.__colors__['selected'])
            self.__screen__.blit(ganador, (panel_x + 30, panel_y + 165))
            
            # Línea separadora después del turno inicial
            pygame.draw.line(self.__screen__, self.__colors__['outline'], 
                            (panel_x + 20, panel_y + 200), 
                            (panel_x + self.PANEL_WIDTH - 20, panel_y + 200), 1)
            
            offset_y = 220
        else:
            offset_y = 80
        
        # Turno actual
        turno_text = self.__fonts__['normal'].render(f"Turno:", True, self.__colors__['text'])
        self.__screen__.blit(turno_text, (panel_x + 20, panel_y + offset_y))
        
        jugador_text = self.__fonts__['normal'].render(f"Jugador {estado['turno']}", True, self.__colors__['selected'])
        self.__screen__.blit(jugador_text, (panel_x + 20, panel_y + offset_y + 30))
        
        # Instrucciones 
        pygame.draw.line(self.__screen__, self.__colors__['outline'], 
                        (panel_x + 20, panel_y + offset_y + 80), 
                        (panel_x + self.PANEL_WIDTH - 20, panel_y + offset_y + 80), 1)
        
        inst_titulo = self.__fonts__['small'].render("Cómo jugar:", True, self.__colors__['text'])
        self.__screen__.blit(inst_titulo, (panel_x + 20, panel_y + offset_y + 95))
        
        inst1 = self.__fonts__['small'].render("1. Tira los dados", True, self.__colors__['text'])
        inst2 = self.__fonts__['small'].render("2. Selecciona ficha", True, self.__colors__['text'])
        inst3 = self.__fonts__['small'].render("3. Selecciona dado", True, self.__colors__['text'])
        inst4 = self.__fonts__['small'].render("ESC - Cancelar", True, self.__colors__['selected'])
        
        self.__screen__.blit(inst1, (panel_x + 25, panel_y + offset_y + 125))
        self.__screen__.blit(inst2, (panel_x + 25, panel_y + offset_y + 150))
        self.__screen__.blit(inst3, (panel_x + 25, panel_y + offset_y + 175))
        self.__screen__.blit(inst4, (panel_x + 25, panel_y + offset_y + 205))
        
        # Botón tirar dados
        if not estado['saltos']:
            mouse_pos = pygame.mouse.get_pos()
            btn_dados = pygame.Rect(panel_x + 20, 470, self.PANEL_WIDTH - 40, 45)
            color = self.__colors__['button_hover'] if btn_dados.collidepoint(mouse_pos) else self.__colors__['button']
            pygame.draw.rect(self.__screen__, color, btn_dados, border_radius=6)
            pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_dados, 2, border_radius=6)
            
            texto = self.__fonts__['small'].render("TIRAR DADOS", True, self.__colors__['text'])
            texto_rect = texto.get_rect(center=btn_dados.center)
            self.__screen__.blit(texto, texto_rect)
        
        # Botón Menu
        mouse_pos = pygame.mouse.get_pos()
        btn_salir = pygame.Rect(panel_x + 20, self.__height__ - 110, self.PANEL_WIDTH - 40, 45)
        color_salir = self.__colors__['button_hover'] if btn_salir.collidepoint(mouse_pos) else self.__colors__['button']
        pygame.draw.rect(self.__screen__, color_salir, btn_salir, border_radius=6)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_salir, 2, border_radius=6)
        
        texto_salir = self.__fonts__['small'].render("Menu", True, self.__colors__['text'])
        texto_rect_salir = texto_salir.get_rect(center=btn_salir.center)
        self.__screen__.blit(texto_salir, texto_rect_salir)
    
    def _dibujar_mensaje(self):
        """Dibuja mensaje temporal en pantalla."""
        texto = self.__fonts__['small'].render(self.__mensaje__, True, self.__colors__['text'])
        
        # Fondo semi-transparente
        superficie = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20))
        superficie.set_alpha(220)
        superficie.fill((30, 30, 30))
        
        x = self.__width__ // 2 - superficie.get_width() // 2
        y = self.__height__ - 80
        
        self.__screen__.blit(superficie, (x, y))
        pygame.draw.rect(self.__screen__, self.__colors__['selected'], 
                        (x, y, superficie.get_width(), superficie.get_height()), 2)
        self.__screen__.blit(texto, (x + 20, y + 10))
    
    def _dibujar_victoria(self):
        """Dibuja la pantalla de victoria."""
        estado = self.__game__.mostrar()
        ganador = estado['ganador']
        
        # Título
        titulo = self.__fonts__['title'].render(f"¡Jugador {ganador} Gana!", True, self.__colors__['selected'])
        titulo_rect = titulo.get_rect(center=(self.__width__//2, self.__height__//2 - 80))
        self.__screen__.blit(titulo, titulo_rect)
        
        # Botón volver al menú
        mouse_pos = pygame.mouse.get_pos()
        btn_rect = pygame.Rect(self.__width__//2 - 120, self.__height__//2 + 60, 240, 60)
        color = self.__colors__['button_hover'] if btn_rect.collidepoint(mouse_pos) else self.__colors__['button']
        pygame.draw.rect(self.__screen__, color, btn_rect, border_radius=8)
        pygame.draw.rect(self.__screen__, self.__colors__['outline'], btn_rect, 2, border_radius=8)
        
        texto = self.__fonts__['normal'].render("Volver al Menú", True, self.__colors__['text'])
        texto_rect = texto.get_rect(center=btn_rect.center)
        self.__screen__.blit(texto, texto_rect)


def main():
    """celda de entrada para la interfaz gráfica."""
    ui = PygameUI()
    ui.ejecutar()


if __name__ == "__main__":
    main()