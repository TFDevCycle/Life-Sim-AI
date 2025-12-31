# Life Sim AI

Eine intelligente, autonome Lebenssimulation, in der Agenten lernen, überleben, Ressourcen sammeln, Häuser bauen, sich fortpflanzen und sich gegen Gegner verteidigen – gesteuert durch KI.

---

## Inhalt

- [Überblick](#überblick)
- [Features](#features)
- [Simulation](#simulation)
- [Tribes / Stammeslogik](#tribes--stammeslogik)
- [Bekannte Einschränkungen](#bekannte-einschränkungen)
- [Installation](#installation)
- [Nutzung](#nutzung)
- [Screenshots](#screenshots)
- [Zukünftige Verbesserungen](#zukünftige-verbesserungen)
- [Lizenz](#lizenz)

---

## Überblick

Life Sim AI simuliert eine kleine Welt, in der autonome Agenten interagieren, lernen und überleben müssen.  

Die Welt verfügt über:  

- einen Tag-/Nacht-Zyklus  
- Ressourcen (Bäume, Steine, Büsche)  
- Gegner, die Agenten bedrohen  
- Häuser, in denen Agenten Schutz suchen und sich fortpflanzen können  
- Tribes, soziale Gruppierungen von Agenten mit eigenen Häusern und Farben  

Die KI-Agenten treffen Entscheidungen basierend auf einem Belohnungssystem (Reward-System) und lernen aus ihren Erfahrungen.

---

## Features

- **Autonome Agenten** mit Hunger, Alter und Memory-System  
- **Belohnungssystem (Reward-System)** für Entscheidungen  
- **Tag-/Nacht-Zyklus**:
  - Tag: Ressourcen sammeln, Häuser bauen, erkunden
  - Nacht: Schutz in Häusern, Fortpflanzung, Verteidigung  
- **Fortpflanzung** nur innerhalb von Häusern nachts  
- **Dynamisches Ressourcenmanagement** (Bäume, Steine, Büsche) mit respawn  
- **Gegner (Enemy)** mit Sichtfeld und Jagdverhalten  
- **Tribes / Stammeslogik**:
  - Agenten können neue Tribes gründen oder bestehenden Tribes beitreten
  - Tribes haben Häuser, Mitglieder, eigene Farbe  
- **UI / Informationsleiste** zeigt:
  - Bevölkerungsstatistiken (Gesamt, Kinder, Erwachsene, Hungrig)
  - Überleben (Ø Alter, Ø Hunger)
  - KI-Lernen (Ø Reward, Top Aktion)
  - Infrastruktur (Häuser, freie Plätze)
  - Tribe-Informationen (Anzahl Stämme, Mitglieder pro Stamm, Häuser pro Stamm)
  - Weltstatus (Phase, Gegner, Ressourcen)
- **Grafische Darstellung** mit Pygame

---

## Simulation

- Weltgröße: 1600 × 1080 Pixel  
- UI rechts: 400px Informationsleiste  
- Ressourcen, Häuser und Agenten werden visuell dargestellt  
- Agenten werden farblich nach Tribe markiert  
- Nacht-Overlay dunkelblau für Tag-/Nacht-Zyklus

---

## Tribes / Stammeslogik

- Ein Tribe wird erzeugt, wenn ein Agent ein Haus baut und keiner in Reichweite ist  
- Agenten können einem Tribe beitreten, wenn sie in der Nähe eines Tribe-Hauses bauen  
- Jeder Tribe hat:
  - Mitgliederliste
  - Liste der Häuser
  - Zentrumskoordinaten (erste Hausposition)
  - Farbe für Visualisierung  
- Fortpflanzung erhöht Mitglieder eines Tribe, aber nur innerhalb von Häusern  

---

## Bekannte Einschränkungen

- **Tribes**:
  - Anfangs haben neue Tribes nur einen Agenten, daher kann Fortpflanzung erst später stattfinden  
  - Die automatische Zuordnung von Agenten zu Tribes bei Hausbau funktioniert noch nicht vollständig stabil  
- **KI-Agenten**:
  - Lernen ist rudimentär und kann noch nicht langfristig komplexe Strategien entwickeln  
- **UI / Performance**:
  - Bei vielen Agenten und Ressourcen kann die FPS fallen  
- **Gegner-KI**:
  - Noch keine komplexen Taktiken, agiert eher zufällig oder patrouillierend  

---

## Installation

1. Repository klonen:

```bash
git clone https://github.com/tfdevcycle/life-sim-ai.git
cd life-sim-ai
