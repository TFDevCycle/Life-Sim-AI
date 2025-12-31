import pygame
import random

class House:
    """
    Repräsentiert ein Haus, das Agenten Schutz bietet.
    """

    def __init__(self, x, y, material="wood", width=40, height=40, capacity=4, tribe=None):
        """
        Initialisiert ein Haus.

        Args:
            x, y (float): Position des Hauses.
            material (str): Baumaterial ("wood" oder "stone").
            width, height (float): Abmessungen.
            capacity (int): Maximale Anzahl an Agenten.
            tribe (Tribe, optional): Zugehöriger Stamm. Default None.
        """
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.capacity = capacity
        self.material = material
        self.occupants = []
        self.has_reproduced = False  # einmal pro Nacht
        self.tribe = tribe  # optional


    def has_space(self):
        """Gibt True zurück, wenn Platz für weitere Agenten ist."""
        return len(self.occupants) < self.capacity

    def enter(self, agent):
        """
        Fügt einen Agenten ins Haus ein.

        Args:
            agent (Agent): Agent, der das Haus betritt.
        """
        if self.has_space() and agent not in self.occupants:
            self.occupants.append(agent)
            agent.in_house = True
            agent.current_house = self
            # Zufällige Position innerhalb des Hauses
            agent.x = random.randint(int(self.x), int(self.x + self.width - 6))
            agent.y = random.randint(int(self.y), int(self.y + self.height - 6))

    def leave(self, agent):
        """Lässt einen Agenten das Haus verlassen."""
        if agent in self.occupants:
            self.occupants.remove(agent)
            agent.in_house = False
            agent.current_house = None

    def reset_occupants(self):
        for agent in self.occupants:
            agent.in_house = False
            agent.current_house = None
        self.occupants.clear()
        self.has_reproduced = False

    def contains(self, agent):
        """Prüft, ob ein Agent im Haus ist."""
        return (self.x <= agent.x <= self.x + self.width and
                self.y <= agent.y <= self.y + self.height)

    def draw(self, surface):
        """Zeichnet das Haus, falls es einem Tribe gehört, in der Tribe-Farbe."""
        color = (150, 75, 0)  # Standard: Braun
        if hasattr(self, "tribe") and self.tribe is not None:
            color = self.tribe.color  # Farbe vom Tribe

        pygame.draw.rect(surface, color, 
                        (int(self.x), int(self.y), int(self.width), int(self.height)))

