import pygame

class Bush:
    """Repräsentiert einen Busch, der gegessen werden kann."""
    def __init__(self, x, y, size=4):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 180, 0)

    def draw(self, surface):
        """Zeichnet den Busch."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
