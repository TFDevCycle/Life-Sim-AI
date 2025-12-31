import pygame
import math
import random

class Enemy:
    """
    Repräsentiert einen Gegner in der Simulation.

    Attributes:
        x (float): X-Position.
        y (float): Y-Position.
        speed (float): Bewegungsgeschwindigkeit.
        sight (float): Sichtweite des Gegners.
        target (object): Aktuelles Zielobjekt.
    """
    def __init__(self, x, y):
        """Initialisiert den Enemy an einer Position."""
        self.x = float(x)
        self.y = float(y)
        self.speed = 0.6
        self.sight = 120
        self.target = None

    def distance(self, x, y):
        """Berechnet die Distanz zu einem Punkt."""
        return math.hypot(self.x - x, self.y - y)

    def move_towards(self, x, y):
        """Bewegt den Enemy auf ein Ziel zu."""
        dx = x - self.x
        dy = y - self.y
        dist = max(1, math.hypot(dx, dy))
        self.x += self.speed * dx / dist
        self.y += self.speed * dy / dist

    def move_random(self):
        """Bewegt den Enemy zufällig, z. B. wenn kein Ziel vorhanden."""
        self.x += random.uniform(-1,1)
        self.y += random.uniform(-1,1)

    def choose_target(self, agents, houses):
        """
        Wählt das aktuelle Ziel für den Enemy.
        
        Priorität:
            1. Sichtbare Agenten
            2. Patrouille um nächstes Haus
            3. Zufällig
        """
        # Sichtbare Agenten
        visible_agents = [
            a for a in agents 
            if self.distance(a.x, a.y) <= self.sight 
            and not any(h.contains(a) for h in houses)
        ]
        if visible_agents:
            self.target = min(visible_agents, key=lambda a: self.distance(a.x, a.y))
            return

        # Patrouille um nächstes Haus
        if houses:
            nearest_house = min(houses, key=lambda h: self.distance(h.x + h.width/2, h.y + h.height/2))
            angle = random.uniform(0, 2*math.pi)
            patrol_radius = max(nearest_house.width, nearest_house.height)/2 + 1  # 1 Pixel Abstand
            patrol_x = nearest_house.x + nearest_house.width/2 + patrol_radius * math.cos(angle)
            patrol_y = nearest_house.y + nearest_house.height/2 + patrol_radius * math.sin(angle)
            self.target = type('Point', (), {'x': patrol_x, 'y': patrol_y})()
            return

        # Kein Ziel
        self.target = None

    def update(self, agents, houses):
        """
        Aktualisiert die Position des Enemy und prüft Angriffe.

        Args:
            agents (list): Liste aller Agenten.
            houses (list): Liste aller Häuser.

        Returns:
            Agent: Getöteter Agent oder None.
        """
        self.choose_target(agents, houses)

        if self.target:
            self.move_towards(self.target.x, self.target.y)

        # Angriff auf Agenten
        if self.target and hasattr(self.target, "x") and hasattr(self.target, "y"):
            for agent in agents:
                if self.distance(agent.x, agent.y) < 6 and not agent.in_house:
                    return agent
        return None

    def draw(self, surface):
        """Zeichnet den Enemy auf dem Surface."""
        pygame.draw.rect(surface, (200,0,0), (int(self.x), int(self.y), 6,6))
