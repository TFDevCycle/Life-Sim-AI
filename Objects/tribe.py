import math
import random

class Tribe:
    """
    Repräsentiert einen Stamm (Tribe) innerhalb der Welt.

    Ein Tribe ist eine soziale Gruppierung von Agenten
    mit einem gemeinsamen Ursprung (erstes Haus).

    Verantwortlichkeiten:
    - Verwaltung der Mitglieder
    - Festlegen eines Stammeszentrums
    - Wachstum & Abspaltung (neue Tribes)
    - Organisation von Hausbau-Nähe
    """

    _id_counter = 0

    def __init__(self, founder_agent, center_x, center_y, color=None):
        """
        Erstellt einen neuen Tribe.

        Args:
            founder_agent (Agent): Erster Agent des Stammes
            center_x (float): X-Koordinate des Stammeszentrums
            center_y (float): Y-Koordinate des Stammeszentrums
            color (tuple, optional): RGB-Farbe des Tribes
        """
        Tribe._id_counter += 1
        self.id = Tribe._id_counter

        self.members = []
        self.center_x = float(center_x)
        self.center_y = float(center_y)

        self.color = color if color else (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255)
        )

        self.max_size = 15  # ab hier Abspaltung möglich
        self.houses = []  # <<< hier Houses-Liste hinzufügen
        self.add_member(founder_agent)

    # --------------------------------------------------

    def add_member(self, agent):
        """
        Fügt einen Agenten dem Tribe hinzu.

        Args:
            agent (Agent)
        """
        if agent not in self.members:
            self.members.append(agent)
            agent.tribe = self

    def remove_member(self, agent):
        """
        Entfernt einen Agenten aus dem Tribe.
        """
        if agent in self.members:
            self.members.remove(agent)
            agent.tribe = None

    # --------------------------------------------------

    def is_overcrowded(self):
        """
        Prüft, ob der Tribe zu groß geworden ist.

        Returns:
            bool
        """
        return len(self.members) >= self.max_size

    def split(self):
        """
        Spaltet einen neuen Tribe ab.

        Ablauf:
        - Hälfte der Mitglieder wird ausgewählt
        - Neuer Mittelpunkt wird zufällig leicht versetzt
        - Neuer Tribe entsteht

        Returns:
            Tribe: Neuer Tribe oder None
        """
        if len(self.members) < self.max_size:
            return None

        split_count = len(self.members) // 2
        new_members = random.sample(self.members, split_count)

        # Neuer Mittelpunkt leicht entfernt
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(120, 200)

        new_x = self.center_x + math.cos(angle) * distance
        new_y = self.center_y + math.sin(angle) * distance

        new_tribe = Tribe(new_members[0], new_x, new_y)

        for agent in new_members:
            self.remove_member(agent)
            new_tribe.add_member(agent)

        return new_tribe

    # --------------------------------------------------

    def get_house_build_position(self):
        """
        Gibt eine Position zurück, an der neue Häuser
        für diesen Tribe gebaut werden sollen.

        Häuser entstehen immer in Nähe des Stammeszentrums.

        Returns:
            (x, y)
        """
        offset_x = random.randint(-80, 80)
        offset_y = random.randint(-80, 80)

        return (
            int(self.center_x + offset_x),
            int(self.center_y + offset_y)
        )

    # --------------------------------------------------

    def average_age(self):
        """Durchschnittsalter des Tribes."""
        if not self.members:
            return 0
        return sum(a.age for a in self.members) / len(self.members)

    def population(self):
        """Aktuelle Bevölkerungszahl."""
        return len(self.members)
