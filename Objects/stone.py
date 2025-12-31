import pygame

class Stone:
    """Repräsentiert einen Stein als Ressource."""
    def __init__(self, x, y, size=4, color=(120, 120, 120)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, surface):
        """Zeichnet den Stein."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
