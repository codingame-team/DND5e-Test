# DnD5e-Scenarios

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![dnd-5e-core](https://img.shields.io/badge/dnd--5e--core-0.1.8-success.svg)](https://pypi.org/project/dnd-5e-core/)

**Créez et jouez des aventures D&D 5e en utilisant le système de scénarios JSON !**

Système complet de création de scénarios basés sur JSON utilisant le package [dnd-5e-core](https://pypi.org/project/dnd-5e-core/). Créez des aventures narratives interactives avec combats, choix, marchands et plus encore.

---

## 🎯 Qu'est-ce que DnD5e-Scenarios ?

DnD5e-Scenarios est un **moteur de scénarios JSON** pour D&D 5e qui vous permet de :

✅ **Créer des aventures** en écrivant du JSON (pas de code Python requis)  
✅ **Jouer 3 scénarios complets** prêts à l'emploi  
✅ **Utiliser les règles officielles D&D 5e** via le package `dnd-5e-core`  
✅ **Personnaliser facilement** les scènes, combats, NPCs et récompenses  

---

## 🚀 Démarrage Rapide

### Installation

```bash
# 1. Installer le package dnd-5e-core
pip install dnd-5e-core

# 2. Cloner ce dépôt
git clone https://github.com/codingame-team/DnD5e-Scenarios.git
cd DnD5e-Scenarios

# 3. Jouer un scénario !
python chasse_gobelins_refactored.py
```

### Lancer un scénario

```bash
# La Chasse aux Gobelins (niveau 3)
python chasse_gobelins_refactored.py

# La Tombe des Rois Serpents (niveau 2)
python tombe_rois_serpents_game.py

# Tales from the Yawning Portal - Sunless Citadel (niveau 1)
python yawning_portal_game.py
```

---

## 📖 5 Scénarios Prêts à Jouer

### 🏰 La Chasse aux Gobelins
- **Niveau** : 3
- **Durée** : 1-2 heures
- **Difficulté** : Facile
- **Synopsis** : Sauvez le Village de Brume terrorisé par des gobelins !

```bash
python chasse_gobelins_refactored.py
```

### 🏛️ The Sunless Citadel
- **Niveau** : 1
- **Durée** : 2-3 heures  
- **Difficulté** : Moyenne
- **Synopsis** : Explorez une citadelle engloutie et détruisez l'arbre maudit !

```bash
python yawning_portal_game.py
```

### 🔺 La Tombe des Rois Serpents
- **Niveau** : 2
- **Durée** : 2 heures
- **Difficulté** : Moyenne
- **Synopsis** : Pillez une pyramide ancienne et affrontez le Roi Serpent momifié !

```bash
python tombe_rois_serpents_game.py
```

### 👁️ L'Oeil de Gruumsh
- **Niveau** : 3
- **Durée** : 2-3 heures
- **Difficulté** : Moyenne
- **Synopsis** : Affrontez une tribu d'orques menée par un redoutable Oeil de Gruumsh dans les Montagnes de Fer !

```bash
python oeil_gruumsh_game.py
```

### 💀 La Secte du Crâne
- **Niveau** : 4
- **Durée** : 2-3 heures
- **Difficulté** : Difficile
- **Synopsis** : Infiltrez les catacombes de Ravencrest et arrêtez un culte nécromantique avant qu'il ne soit trop tard !

```bash
python secte_du_crane_game.py
```

---

## 🎨 Système de Scénarios JSON

### Créez vos propres aventures !

Le système supporte **5 types de scènes** :

| Type | Description | Exemple |
|------|-------------|---------|
| 🎭 **narrative** | Texte narratif immersif | Intro, descriptions de lieux |
| 🔀 **choice** | Choix multiples avec embranchements | Que faire ? Explorer / Se reposer |
| ⚔️ **combat** | Combat tactique avec monstres | Affrontement avec gobelins |
| 🛒 **merchant** | Marchand avec inventaire | Acheter potions et équipement |
| 💤 **rest** | Repos court ou long | Récupération HP et sorts |

### Exemple de scénario JSON

```json
{
  "scenario_id": "mon_aventure",
  "name": "Mon Aventure Épique",
  "level": 3,
  "difficulty": "medium",
  "scenes": [
    {
      "id": "intro",
      "type": "narrative",
      "title": "🏰 Le Début",
      "text": "Vous arrivez dans un village mystérieux...",
      "next_scene": "choix1"
    },
    {
      "id": "choix1",
      "type": "choice",
      "title": "Que faire ?",
      "description": "Le village est calme. Trop calme.",
      "choices": [
        {
          "text": "Explorer la taverne",
          "next_scene": "taverne",
          "effects": {"reputation": 1}
        },
        {
          "text": "Partir vers la forêt",
          "next_scene": "foret"
        }
      ]
    },
    {
      "id": "combat1",
      "type": "combat",
      "title": "⚔️ Embuscade !",
      "description": "Des bandits surgissent !",
      "monsters": ["bandit", "bandit", "bandit-captain"],
      "on_victory": "victoire",
      "on_defeat": "defaite"
    }
  ]
}
```

### Structure d'un scénario

```
data/scenes/mon_scenario.json
{
  "scenario_id": "identifiant_unique",
  "name": "Titre du Scénario",
  "level": 3,                    # Niveau recommandé
  "difficulty": "medium",        # easy, medium, hard
  "duration_hours": "2-3",
  "recommended_party_size": 4,
  "scenes": [
    // Liste des scènes...
  ]
}
```

📖 **Documentation complète** : [README_SCENARIOS_JSON.md](README_SCENARIOS_JSON.md)

---

## 🎮 Fonctionnalités

### Scènes Narratives
- ✅ Texte avec animation lettre par lettre
- ✅ Délai personnalisable
- ✅ Transitions fluides entre scènes

### Choix Interactifs
- ✅ Embranchements multiples
- ✅ Effets sur l'état du jeu (or, réputation, etc.)
- ✅ Navigation libre dans le scénario

### Système de Combat
- ✅ Règles D&D 5e officielles
- ✅ Jets d'attaque et de dégâts
- ✅ Actions spéciales des monstres
- ✅ Gestion de l'initiative

### Marchands
- ✅ Achat/vente d'équipement
- ✅ Armes, armures, potions
- ✅ Gestion automatique de l'inventaire

### Repos
- ✅ Repos court (récupération partielle)
- ✅ Repos long (récupération complète + sorts)
- ✅ Gestion automatique des HP et ressources

---

## 🏗️ Architecture du Projet

```
DnD5e-Scenarios/
├── README.md                          # Ce fichier
├── README_SCENARIOS_JSON.md           # Documentation détaillée du système
├── LICENSE                            # Licence MIT
│
├── 📁 data/                           # Données des scénarios
│   ├── scenes/                        # Scénarios JSON
│   │   ├── chasse_gobelins.json      # Scénario 1
│   │   ├── sunless_citadel.json      # Scénario 2
│   │   └── tombe_rois_serpents.json  # Scénario 3
│   └── parties/                       # Groupes pré-configurés
│       └── scenario_parties.json
│
├── 📁 src/                            # Code source
│   ├── core/                          # Extensions du package
│   ├── rendering/                     # Système de rendu
│   ├── scenarios/                     # Classe de base
│   ├── scenes/                        # Système de scènes
│   │   ├── scene_system.py           # Classes de scènes
│   │   └── scene_factory.py          # Loader JSON → Scènes
│   ├── systems/                       # Systèmes de jeu
│   └── utils/                         # Utilitaires
│
├── 🎮 Scripts de lancement
│   ├── play_scenario_from_json.py    # Démo système JSON
│   ├── play_scenarios.py             # Lanceur interactif
│   ├── chasse_gobelins_refactored.py # Exemple code Python
│   ├── tombe_rois_serpents_game.py   # Exemple 2
│   └── yawning_portal_game.py        # Exemple 3
│
├── 📁 scenarios/                      # PDFs de scénarios (optionnel)
├── 📁 savegames/                      # Sauvegardes de parties
└── 📁 archive/                        # Documentation archivée
```

---

## 💡 Exemples d'Utilisation

### 1. Jouer avec le système JSON

```python
from src.scenes.scene_factory import SceneFactory
from dnd_5e_core.combat import CombatSystem

# Charger un scénario
scene_manager = SceneFactory.load_scenario_from_json_file(
    "data/scenes/chasse_gobelins.json",
    monster_factory=monster_factory
)

# Préparer le contexte
game_context = {
    'party': party,
    'game_state': game_state,
    'renderer': renderer,
    'combat_system': CombatSystem(verbose=True),
    'monster_factory': monster_factory
}

# Lancer l'aventure
scene_manager.run(game_context)
```

### 2. Créer un scénario personnalisé

Créez `data/scenes/ma_quete.json` :

```json
{
  "scenario_id": "ma_quete",
  "name": "La Quête du Dragon",
  "level": 5,
  "scenes": [
    {
      "id": "start",
      "type": "narrative",
      "title": "🐉 La Prophétie",
      "text": "Un dragon menace le royaume...",
      "next_scene": "village"
    }
  ]
}
```

Puis lancez-le :

```python
python play_scenario_from_json.py
# Modifiez le script pour pointer vers votre JSON
```

### 3. Intégrer dans votre code

```python
from src.scenarios.base_scenario import BaseScenario

class MonScenario(BaseScenario):
    def get_scenario_name(self):
        return "Mon Aventure"
    
    def create_party(self):
        return [
            self.create_basic_fighter("Guerrier", level=5),
            self.create_basic_cleric("Clerc", level=5)
        ]
    
    def build_custom_scenes(self):
        # Ajoutez vos scènes en Python
        pass
```

---

## 🎲 Système de Jeu

### Basé sur dnd-5e-core

Le package `dnd-5e-core` fournit :

- ✅ **332 monstres** avec stats officielles
- ✅ **319 sorts** D&D 5e
- ✅ **Système de combat** complet
- ✅ **Calcul de Challenge Rating** (CR)
- ✅ **Génération de personnages**
- ✅ **Règles D&D 5e** officielles

### Combats

- Initiative automatique
- Jets d'attaque avec bonus
- Calcul des dégâts (dés multiples)
- Actions spéciales des monstres
- Gestion HP et conditions

### Personnages

- Races et classes
- Capacités et modificateurs
- Équipement et inventaire
- Sorts et emplacements
- Progression XP

---

## 📚 Documentation

### Guides

- **[README_SCENARIOS_JSON.md](README_SCENARIOS_JSON.md)** - Documentation complète du système JSON
- **Exemples** - Consultez les fichiers dans `data/scenes/`

### Package dnd-5e-core

- **PyPI** : [pypi.org/project/dnd-5e-core](https://pypi.org/project/dnd-5e-core/)
- **GitHub** : [github.com/codingame-team/dnd-5e-core](https://github.com/codingame-team/dnd-5e-core)

---

## 🤝 Contribution

### Créer et partager des scénarios

1. Créez votre scénario JSON dans `data/scenes/`
2. Testez-le avec `play_scenario_from_json.py`
3. Partagez-le avec la communauté (Pull Request)

### Améliorer le système

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/amazing-feature`)
3. Commitez vos changements (`git commit -m 'Add amazing feature'`)
4. Pushez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

---

## 🎯 Feuille de Route

### Court terme
- [ ] Validation de schéma JSON
- [ ] Plus d'exemples de scénarios
- [ ] Tests unitaires

### Moyen terme
- [ ] Éditeur visuel de scénarios
- [ ] Générateur de scénarios aléatoires
- [ ] Support de conditions complexes
- [ ] Système de quêtes

### Long terme
- [ ] Interface graphique complète
- [ ] Mode multijoueur (DM + joueurs)
- [ ] Marketplace de scénarios
- [ ] Intégration Roll20/Foundry VTT

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **D&D 5e** - Wizards of the Coast
- **Package dnd-5e-core** - Règles D&D 5e en Python
- **5eTools** - Base de données de monstres

---

## 🎉 Commencez maintenant !

```bash
git clone https://github.com/codingame-team/DnD5e-Scenarios.git
cd DnD5e-Scenarios
pip install dnd-5e-core
python play_scenarios.py
```

**Que vos dés soient toujours critiques !** 🎲✨

---

**Projet** : DnD5e-Scenarios  
**Auteur** : CodingGame Team  
**Version** : 1.0  
**Date** : Janvier 2026

