import pygame

class Tree:
    """Repräsentiert einen Baum als Ressource."""
    def __init__(self, x, y, size=4, color=(139, 69, 19)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, surface):
        """Zeichnet den Baum."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
