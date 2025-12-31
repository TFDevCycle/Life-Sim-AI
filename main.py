import pygame
import random
import time
import math
from agent import Agent
from Objects.tree import Tree
from Objects.stone import Stone
from Objects.bush import Bush
from Objects.house import House
from Objects.enemy import Enemy
from Objects.tribe import Tribe


SCREEN_W, SCREEN_H = 1920, 1080
WORLD_W = 1600
UI_X = 1550

DAY_TIME = 30
NIGHT_TIME = 20

class Game:
    """
    Hauptklasse für das Spiel / Simulation.

    Attributes:
        screen (pygame.Surface): Haupt-Screen der Simulation.
        clock (pygame.time.Clock): Pygame Clock für FPS.
        font (pygame.font.Font): Schriftart für UI.
        trees, stones, bushes (list): Listen der Ressourcenobjekte.
        agents (list): Liste aller Agenten in der Welt.
        houses (list): Liste aller Häuser.
        enemies (list): Liste aller Gegner.
        is_day (bool): Status Tag/Nacht.
        cycle_timer (float): Zeitstempel des letzten Tag/Nacht-Wechsels.
    """

    def __init__(self):
        """
        Initialisiert die Welt, spawnt Ressourcen, Agenten und Häuser
        und startet die Mainloop.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 16)

        # Ressourcen generieren
        self.trees = [Tree(random.randint(0, WORLD_W), random.randint(0, SCREEN_H)) for _ in range(160)]
        self.stones = [Stone(random.randint(0, WORLD_W), random.randint(0, SCREEN_H)) for _ in range(120)]
        self.bushes = [Bush(random.randint(0, WORLD_W), random.randint(0, SCREEN_H)) for _ in range(100)]

        # Agenten und Häuser
        self.agents = [Agent(400, 360), Agent(420, 360)]
        self.houses = [House(430, 350, "wood")]
        self.enemies = []
        self.tribes = []

        self.is_day = True
        self.cycle_timer = time.time()

        self.mainloop()

    def update_day_night(self):
        """
        Prüft den Tag/Nacht-Wechsel basierend auf Zeit.
        Spawnt Gegner bei Nacht und Ressourcen bei Tag.
        """
        elapsed = time.time() - self.cycle_timer

        if self.is_day and elapsed > DAY_TIME:
            self.is_day = False
            self.cycle_timer = time.time()
            self.spawn_enemies()  # Gegner erscheinen bei Nacht
        elif not self.is_day and elapsed > NIGHT_TIME:
            self.is_day = True
            self.cycle_timer = time.time()
            self.enemies.clear()  # Gegner verschwinden bei Tag
            self.respawn_resources()
            for house in self.houses:
                house.reset_occupants()  # Nacht-Status zurücksetzen

    def respawn_resources(self):
        """
        Setzt Ressourcen zurück und spawnt neue an zufälligen Positionen.
        """
        self.trees = [Tree(random.randint(0, WORLD_W), random.randint(0, SCREEN_H)) for _ in range(160)]
        self.stones = [Stone(random.randint(0, WORLD_W), random.randint(0, SCREEN_H)) for _ in range(120)]
        self.bushes = [Bush(random.randint(0, WORLD_W), random.randint(0, SCREEN_H)) for _ in range(100)]

    def spawn_enemies(self):
        """
        Spawnt Gegner zufällig in der Welt.
        """
        for _ in range(10):
            self.enemies.append(Enemy(random.randint(0, WORLD_W), random.randint(0, SCREEN_H)))

    def draw_ui(self):
        """
        Zeichnet die Informationsleiste rechts mit:
        - Bevölkerungsstatistiken
        - Überleben (Ø Alter, Hunger)
        - KI-Status (Reward, Top-Aktion)
        - Infrastruktur (Häuser, freie Plätze)
        - Stamm-Informationen (Anzahl Stämme, Mitglieder pro Stamm, Häuser pro Stamm)
        - Weltstatus (Tag/Nacht, Gegner, Ressourcen)
        """
        pygame.draw.rect(self.screen, (25, 25, 25), (UI_X, 0, 400, SCREEN_H))

        pop = len(self.agents)
        kids = sum(1 for a in self.agents if a.age < 18)
        adults = sum(1 for a in self.agents if 18 <= a.age < 80)
        hungry = sum(1 for a in self.agents if a.hunger < 30)
        avg_age = round(sum(a.age for a in self.agents) / max(1, pop), 1)
        avg_hunger = round(sum(a.hunger for a in self.agents) / max(1, pop), 1)
        avg_reward = round(sum(a.total_reward for a in self.agents) / max(1, pop), 2)

        # Häufigste Aktion
        action_counter = {}
        for a in self.agents:
            for k, v in a.memory.items():
                action_counter[k] = action_counter.get(k, 0) + v
        top_action = max(action_counter, key=action_counter.get) if action_counter else "-"

        # Häuser
        total_capacity = sum(h.capacity for h in self.houses)
        occupied = sum(len(h.occupants) for h in self.houses)
        free_places = total_capacity - occupied

        # Stämme zählen und Statistik erstellen
        tribes = {}
        for agent in self.agents:
            if hasattr(agent, "tribe") and agent.tribe:
                tribe_name = agent.tribe.name if hasattr(agent.tribe, "name") else str(id(agent.tribe))
                if tribe_name not in tribes:
                    tribes[tribe_name] = {"members": 0, "houses": 0}
                tribes[tribe_name]["members"] += 1

        for house in self.houses:
            if hasattr(house, "tribe") and house.tribe:
                tribe_name = house.tribe.name if hasattr(house.tribe, "name") else str(id(house.tribe))
                if tribe_name not in tribes:
                    tribes[tribe_name] = {"members": 0, "houses": 0}
                tribes[tribe_name]["houses"] += 1

        # Lines zusammenstellen
        lines = [
            "=== BEVÖLKERUNG ===",
            f"Gesamt: {pop}",
            f"Kinder: {kids}",
            f"Erwachsene: {adults}",
            f"Hungrig (<30): {hungry}",
            "",
            "=== ÜBERLEBEN ===",
            f"Ø Alter: {avg_age}",
            f"Ø Hunger: {avg_hunger}",
            "",
            "=== KI / LERNEN ===",
            f"Ø Reward: {avg_reward}",
            f"Top Aktion: {top_action}",
            "",
            "=== INFRASTRUKTUR ===",
            f"Häuser: {len(self.houses)}",
            f"Plätze frei: {free_places}",
            "",
            "=== STÄMME ===",
            f"Stämme: {len(self.tribes)}",
        ]

        for name, stats in tribes.items():
            lines.append(f"{name}: {stats['members']} Mitglieder, {stats['houses']} Häuser")

        lines += [
            "",
            "=== WELT ===",
            f"Phase: {'TAG' if self.is_day else 'NACHT'}",
            f"Gegner: {len(self.enemies)}",
            f"Bäume: {len(self.trees)}",
            f"Steine: {len(self.stones)}",
            f"Büsche: {len(self.bushes)}",
        ]

        # Text zeichnen
        y = 15
        for line in lines:
            color = (200, 200, 200)
            if "===" in line:
                color = (180, 220, 255)
            text = self.font.render(line, True, color)
            self.screen.blit(text, (UI_X + 15, y))
            y += 22


    def mainloop(self):
        """
        Haupt-Loop der Simulation:
        - Tag/Nacht wechseln
        - Agenten aktualisieren
        - Gegner aktualisieren
        - Hausbau & Fortpflanzung
        - Rendern der Welt und UI
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.update_day_night()

            # Fortpflanzung nachts
            if not self.is_day:
                for house in self.houses:
                    adults = [a for a in house.occupants if a.age >= 18]
                    if len(adults) >= 2 and not house.has_reproduced:
                        num_children = random.randint(1, 2)
                        for _ in range(num_children):
                            parents = random.sample(adults, 2)
                            child = parents[0].make_child(parents[1])
                            self.agents.append(child)
                            house.enter(child)
                        house.has_reproduced = True

            dead_agents = []

            for agent in self.agents:
                status, data = agent.update(
                    self.trees,
                    self.stones,
                    self.bushes,
                    self.agents,
                    self.houses,
                    self.is_day,
                    self.enemies
                )

                if status == "dead":
                    dead_agents.append(agent)

                if status == "build_house":
                    material, x, y = data
                    
                    # Nearby Tribe finden
                    nearby_tribes = [t for t in self.tribes if any(
                        math.hypot(h.x - x, h.y - y) < 200 for h in t.houses
                    )]

                    if nearby_tribes:
                        tribe = random.choice(nearby_tribes)
                        tribe.add_member(agent)  # Agent dem Tribe hinzufügen
                    else:
                        # Neuen Tribe erstellen, falls keiner in der Nähe
                        tribe = Tribe(agent, x, y)
                        self.tribes.append(tribe)
                    
                    agent.tribe = tribe
                    # Haus erzeugen und Tribe zuordnen
                    new_house = House(x, y, material, tribe=tribe)
                    self.houses.append(new_house)
                    tribe.houses.append(new_house)

            for enemy in self.enemies:
                killed = enemy.update(self.agents, self.houses)
                if killed and killed in self.agents:
                    self.agents.remove(killed)

            for d in dead_agents:
                if d in self.agents:
                    self.agents.remove(d)

            # Render
            bg = (0, 120, 0) if self.is_day else (10, 30, 60)
            self.screen.fill(bg)

            for obj in self.trees + self.stones + self.bushes + self.houses:
                obj.draw(self.screen)

            for agent in self.agents:
                # Tribe-Farbe, falls Agent einem Tribe angehört
                color = agent.tribe.color if hasattr(agent, "tribe") and agent.tribe else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (agent.x, agent.y, 6, 6))



            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Nacht-Overlay
            if not self.is_day:
                overlay = pygame.Surface((WORLD_W, SCREEN_H))
                overlay.set_alpha(100)
                overlay.fill((0, 0, 50))
                self.screen.blit(overlay, (0, 0))

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)

Game()
