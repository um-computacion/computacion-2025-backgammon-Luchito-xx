"""
Módulo DadosUI - Componente visual de dados clickeables.

Representa los dados del juego de forma interactiva, permitiendo al
jugador seleccionar qué dado usar para un movimiento.
"""

import pygame


class DadoUI:
    """
    Representa un dado visual clickeable.
    
    Atributos:
        __valor__ (int): Valor del dado (1-6).
        __rect__ (pygame.Rect): Rectángulo de colisión.
        __usado__ (bool): Si el dado ya fue usado.
        __seleccionado__ (bool): Si está actualmente seleccionado.
    """
    
    DADO_SIZE = 50
    DOT_RADIUS = 5
    
    def __init__(self, x, y, valor):
        """
        Inicializa un dado visual.
        
        Args:
            x (int): Posición X del dado.
            y (int): Posición Y del dado.
            valor (int): Valor del dado (1-6).
        """
        self.__valor__ = valor
        self.__rect__ = pygame.Rect(x, y, self.DADO_SIZE, self.DADO_SIZE)
        self.__usado__ = False
        self.__seleccionado__ = False
    
    def get_valor(self):
        """Obtiene el valor del dado."""
        return self.__valor__
    
    def get_rect(self):
        """Obtiene el rectángulo de colisión."""
        return self.__rect__
    
    def is_usado(self):
        """Verifica si el dado fue usado."""
        return self.__usado__
    
    def marcar_usado(self):
        """Marca el dado como usado."""
        self.__usado__ = True
    
    def is_seleccionado(self):
        """Verifica si el dado está seleccionado."""
        return self.__seleccionado__
    
    def set_seleccionado(self, estado):
        """
        Establece el estado de selección.
        
        Args:
            estado (bool): True para seleccionar, False para deseleccionar.
        """
        self.__seleccionado__ = estado
    
    def dibujar(self, pantalla):
        """
        Dibuja el dado en la pantalla.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar.
        """
        # Colores
        if self.__usado__:
            color_fondo = (100, 100, 100)  # Gris
            color_dots = (150, 150, 150)
        elif self.__seleccionado__:
            color_fondo = (255, 215, 0)  # Dorado
            color_dots = (0, 0, 0)
        else:
            color_fondo = (255, 255, 255)  # Blanco
            color_dots = (0, 0, 0)
        
        # Dibujar dado
        pygame.draw.rect(pantalla, color_fondo, self.__rect__, border_radius=8)
        pygame.draw.rect(pantalla, (0, 0, 0), self.__rect__, 2, border_radius=8)
        
        # Dibujar puntos según valor
        self._dibujar_puntos(pantalla, color_dots)
    
    def _dibujar_puntos(self, pantalla, color):
        """
        Dibuja los puntos del dado según su valor.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar.
            color (tuple): Color RGB de los puntos.
        """
        cx = self.__rect__.centerx
        cy = self.__rect__.centery
        offset = 12
        
        # Patrones de puntos para cada valor
        if self.__valor__ == 1:
            pygame.draw.circle(pantalla, color, (cx, cy), self.DOT_RADIUS)
            
        elif self.__valor__ == 2:
            pygame.draw.circle(pantalla, color, (cx - offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy + offset), self.DOT_RADIUS)
            
        elif self.__valor__ == 3:
            pygame.draw.circle(pantalla, color, (cx - offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx, cy), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy + offset), self.DOT_RADIUS)
            
        elif self.__valor__ == 4:
            pygame.draw.circle(pantalla, color, (cx - offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx - offset, cy + offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy + offset), self.DOT_RADIUS)
            
        elif self.__valor__ == 5:
            pygame.draw.circle(pantalla, color, (cx - offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx, cy), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx - offset, cy + offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy + offset), self.DOT_RADIUS)
            
        elif self.__valor__ == 6:
            pygame.draw.circle(pantalla, color, (cx - offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy - offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx - offset, cy), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx - offset, cy + offset), self.DOT_RADIUS)
            pygame.draw.circle(pantalla, color, (cx + offset, cy + offset), self.DOT_RADIUS)


class GestorDados:
    """
    Gestiona múltiples dados y su interacción.
    
    Atributos:
        __dados__ (list[DadoUI]): Lista de dados visuales.
        __dado_seleccionado__ (DadoUI|None): Dado actualmente seleccionado.
    """
    
    def __init__(self):
        """Inicializa el gestor de dados."""
        self.__dados__ = []
        self.__dado_seleccionado__ = None
    
    def actualizar_dados(self, valores, x_inicio, y_inicio):
        """
        Actualiza los dados con nuevos valores.
        
        Args:
            valores (list[int]): Lista de valores de dados.
            x_inicio (int): Posición X inicial.
            y_inicio (int): Posición Y inicial.
        """
        self.__dados__ = []
        self.__dado_seleccionado__ = None
        
        espaciado = 60
        for i, valor in enumerate(valores):
            x = x_inicio + (i % 2) * espaciado
            y = y_inicio + (i // 2) * espaciado
            self.__dados__.append(DadoUI(x, y, valor))
    
    def manejar_click(self, pos):
        """
        Maneja el click en un dado.
        
        Args:
            pos (tuple): Posición (x, y) del click.
            
        Returns:
            int|None: Valor del dado seleccionado o None.
        """
        for dado in self.__dados__:
            if not dado.is_usado() and dado.get_rect().collidepoint(pos):
                # Deseleccionar todos
                for d in self.__dados__:
                    d.set_seleccionado(False)
                
                # Seleccionar el clickeado
                dado.set_seleccionado(True)
                self.__dado_seleccionado__ = dado
                return dado.get_valor()
        
        return None
    
    def marcar_dado_usado(self, valor):
        """
        Marca un dado como usado.
        
        Args:
            valor (int): Valor del dado a marcar.
        """
        for dado in self.__dados__:
            if dado.get_valor() == valor and not dado.is_usado():
                dado.marcar_usado()
                dado.set_seleccionado(False)
                self.__dado_seleccionado__ = None
                break
    
    def get_dado_seleccionado(self):
        """
        Obtiene el dado actualmente seleccionado.
        
        Returns:
            DadoUI|None: Dado seleccionado o None.
        """
        return self.__dado_seleccionado__
    
    def deseleccionar_todos(self):
        """Deselecciona todos los dados."""
        for dado in self.__dados__:
            dado.set_seleccionado(False)
        self.__dado_seleccionado__ = None
    
    def tiene_dados_disponibles(self):
        """
        Verifica si hay dados sin usar.
        
        Returns:
            bool: True si hay al menos un dado disponible.
        """
        return any(not dado.is_usado() for dado in self.__dados__)
    
    def dibujar(self, pantalla):
        """
        Dibuja todos los dados.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar.
        """
        for dado in self.__dados__:
            dado.dibujar(pantalla)