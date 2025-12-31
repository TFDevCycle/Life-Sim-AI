import pygame
import random
import math
import time

class Agent:
    """
    Repräsentiert einen Agenten in der Simulation.

    Attributes:
        x (float): X-Position des Agenten.
        y (float): Y-Position des Agenten.
        hunger (float): Hungerlevel (0-100).
        age (float): Alter des Agenten in Jahren.
        wood (int): Gesammelte Holzmenge.
        stone (int): Gesammelte Steinmenge.
        has_pickaxe (bool): Ob der Agent eine Spitzhacke besitzt.
        in_house (bool): Ob der Agent aktuell in einem Haus ist.
        current_house (House): Referenz auf das Haus, in dem der Agent ist.
        memory (dict): Lernwerte für verschiedene Aktionen.
        vision_radius (float): Wahrnehmungsradius für Ressourcen und Gegner.
        reproduction_cooldown (int): Zeit bis zur nächsten Fortpflanzung.
        reproduction_timer (int): Zähler für Fortpflanzung.
        total_reward (float): Durchschnittlicher Reward der letzten Aktionen.
        reward_buffer (list): Zwischenspeicher für Reward-Glättung.
        reward_tick (float): Zeitstempel des letzten Reward-Updates.
        reward_interval (float): Intervall für Reward-Glättung.
        tribe (Tribe): Zugehöriger Stamm.
        generation (int): Generation des Agenten innerhalb des Stammes.
    """

    def __init__(self, x, y, memory=None, tribe=None, generation=0):
        """
        Initialisiert einen Agenten mit Position, optionalem Memory, Tribe und Generation.

        Args:
            x (float): Start-X-Position.
            y (float): Start-Y-Position.
            memory (dict, optional): Initiales Lern-Memory.
            tribe (Tribe, optional): Zugehöriger Stamm.
            generation (int, optional): Generation innerhalb des Stammes.
        """
        self.x = x
        self.y = y
        self.hunger = 100
        self.age = 0.0
        self.wood = 0
        self.stone = 0
        self.has_pickaxe = False
        self.in_house = False
        self.current_house = None

        self.tribe = None  # Zugehörigkeit zu Tribe
        self.generation = generation

        self.total_reward = 0
        self.reward_buffer = []
        self.reward_tick = time.time()
        self.reward_interval = 0.5

        self.memory = memory if memory else {
            "wander": 1.0,
            "chop_tree": 0.0,
            "eat_bush": 0.0,
            "craft_pickaxe": 0.0,
            "mine_stone": 0.0
        }

        self.vision_radius = 100
        self.reproduction_cooldown = 600
        self.reproduction_timer = random.randint(0, 300)

    # ----------------------------

    def add_reward(self, r):
        """
        Fügt einen Reward hinzu und glättet über den Puffer.

        Args:
            r (float): Reward-Wert.
        """
        self.reward_buffer.append(r)
        if len(self.reward_buffer) > 10:
            self.reward_buffer.pop(0)
        self.total_reward = sum(self.reward_buffer) / len(self.reward_buffer)

    def distance(self, obj):
        """
        Berechnet die euklidische Distanz zu einem Objekt.

        Args:
            obj: Objekt mit x- und y-Attributen.

        Returns:
            float: Distanz zum Objekt.
        """
        return math.hypot(self.x - obj.x, self.y - obj.y)

    # ----------------------------

    def choose_action(self):
        """
        Wählt zufällig eine Aktion basierend auf Memory-Werten.
        Höher bewertete Aktionen werden häufiger gewählt.

        Returns:
            str: Name der gewählten Aktion.
        """
        pool = []
        for action, value in self.memory.items():
            pool.extend([action] * max(1, int(value + 1)))
        return random.choice(pool)

    def learn(self, action, reward):
        """
        Aktualisiert das Memory basierend auf Aktion und Reward.

        Args:
            action (str): Name der Aktion.
            reward (float): Reward für diese Aktion.
        """
        self.memory[action] += reward
        self.memory[action] = max(-5, min(10, self.memory[action]))

        current_time = time.time()
        if current_time - self.reward_tick >= self.reward_interval:
            self.reward_tick = current_time
            self.add_reward(reward)

    # ----------------------------

    def move_random(self):
        """Bewegt den Agenten zufällig innerhalb erlaubter Grenzen."""
        self.x += random.randint(-2, 2)
        self.y += random.randint(-2, 2)
        self.x = max(0, min(self.x, 880))
        self.y = max(0, min(self.y, 720))

    def move_towards(self, target):
        """
        Bewegt den Agenten auf ein Ziel zu.

        Args:
            target: Objekt mit x- und y-Attributen.
        """
        dx, dy = target.x - self.x, target.y - self.y
        dist = max(1, math.hypot(dx, dy))
        self.x += int(2 * dx / dist)
        self.y += int(2 * dy / dist)

    def find_nearest(self, objects):
        """
        Findet das nächste sichtbare Objekt aus einer Liste.

        Args:
            objects (list): Liste von Objekten mit x- und y-Attributen.

        Returns:
            Objekt oder None: Nächstes sichtbares Objekt.
        """
        visible = [o for o in objects if self.distance(o) < self.vision_radius]
        return min(visible, key=lambda o: self.distance(o)) if visible else None

    # ----------------------------

    def update(self, trees, stones, bushes, agents, houses, is_day, enemies):
        """
        Hauptlogik pro Tick für den Agenten.

        Args:
            trees, stones, bushes (list): Ressourcenlisten.
            agents (list): Alle Agenten.
            houses (list): Alle Häuser.
            is_day (bool): Tag/Nacht-Status.
            enemies (list): Liste von Gegnern.

        Returns:
            tuple: (status, data)
                status (str): "alive", "dead" oder "build_house".
                data: Zusatzinformationen, z.B. Hausmaterial und Position.
        """
        self.age += 0.01
        self.hunger -= 0.01

        if self.hunger <= 0 or self.age >= 100:
            return "dead", None

        # Nacht: im Haus bleiben
        if not is_day and self.in_house and self.current_house:
            self.x = max(self.current_house.x,
                         min(self.x, self.current_house.x + self.current_house.width - 6))
            self.y = max(self.current_house.y,
                         min(self.y, self.current_house.y + self.current_house.height - 6))
            return "alive", None

        # Tag: Haus verlassen
        if is_day and self.in_house:
            self.current_house.leave(self)

        # Gegnererkennung
        threat = any(self.distance(e) < 80 for e in enemies)
        if threat:
            safe_houses = [h for h in houses if h.has_space() and h.tribe == self.tribe]
            if safe_houses:
                nearest = min(safe_houses, key=lambda h: self.distance(h))
                nearest.enter(self)
                return "alive", None

        # Aktion ausführen
        action = self.choose_action()
        print(f"{self.age:.2f}y chooses {action} with wood={self.wood} stone={self.stone}")

        if action == "wander":
            self.move_random()
            self.learn(action, -0.01)
        elif action == "eat_bush":
            bush = self.find_nearest(bushes)
            if bush:
                if self.distance(bush) < 8:
                    bushes.remove(bush)
                    self.hunger = min(100, self.hunger + 40)
                    self.learn(action, 4)
                else:
                    self.move_towards(bush)
        elif action == "chop_tree":
            tree = self.find_nearest(trees)
            if tree:
                if self.distance(tree) < 8:
                    trees.remove(tree)
                    self.wood += 1
                    self.learn(action, 3)
                else:
                    self.move_towards(tree)
        elif action == "craft_pickaxe":
            if self.wood >= 5 and not self.has_pickaxe:
                self.wood -= 5
                self.has_pickaxe = True
                self.learn(action, 8)
            else:
                self.learn(action, -0.2)
        elif action == "mine_stone":
            if self.has_pickaxe:
                stone = self.find_nearest(stones)
                if stone:
                    if self.distance(stone) < 8:
                        stones.remove(stone)
                        self.stone += 1
                        self.learn(action, 5)
                    else:
                        self.move_towards(stone)
            else:
                self.learn(action, -1)

        # Haus bauen
        if self.wood >= 10:
            self.wood -= 10
            return "build_house", ("wood", self.x, self.y)
        if self.wood >= 5 and self.stone >= 5:
            self.wood -= 5
            self.stone -= 5
            return "build_house", ("stone", self.x, self.y)

        return "alive", None

    # ----------------------------

    def make_child(self, other):
        """
        Erzeugt ein Kind-Agenten.

        Args:
            other (Agent): Partner-Agent.

        Returns:
            Agent: Kind-Agent mit vererbtem Memory, Tribe und Generation.
        """
        new_memory = {}
        for key in self.memory:
            avg = (self.memory[key] + other.memory[key]) / 2
            new_memory[key] = avg + random.uniform(-0.2, 0.2)

        child = Agent(
            self.x,
            self.y,
            memory=new_memory,
            tribe=self.tribe,
            generation=max(self.generation, other.generation) + 1
        )
        return child

    # ----------------------------

    def draw(self, surface):
        """
        Zeichnet den Agenten auf dem Surface.

        Args:
            surface: Pygame Surface.
        """
        color = self.tribe.color if self.tribe else (255, 255, 255)
        pygame.draw.rect(surface, color, (self.x, self.y, 6, 6))
