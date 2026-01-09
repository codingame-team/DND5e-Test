# Système de Scénarios JSON - DnD5e-Test

## Vue d'ensemble

Le projet DnD5e-Test inclut un système complet de scénarios basés sur JSON qui permet de créer et jouer des aventures D&D 5e sans écrire de code Python.

## 📁 Structure des fichiers

```
DnD5e-Test/
├── data/
│   ├── scenes/          # Fichiers JSON des scénarios
│   │   ├── chasse_gobelins.json
│   │   ├── sunless_citadel.json
│   │   └── tombe_rois_serpents.json
│   ├── parties/         # Configurations de groupes
│   │   └── scenario_parties.json
│   └── monsters/        # Données de monstres (optionnel)
├── src/
│   └── scenes/
│       ├── scene_system.py    # Classes de scènes
│       └── scene_factory.py   # Factory pour JSON → Scènes
└── play_scenario_from_json.py # Script de démonstration
```

## 🎮 Types de scènes disponibles

### 1. Narrative Scene (Texte narratif)
```json
{
  "id": "intro",
  "type": "narrative",
  "title": "🏰 VILLAGE DE BRUME",
  "text": "Le Village de Brume est en émoi...",
  "next_scene": "village_choice"
}
```

### 2. Choice Scene (Choix multiples)
```json
{
  "id": "village_choice",
  "type": "choice",
  "title": "VILLAGE - PLACE CENTRALE",
  "description": "Vous êtes au village. Que faire?",
  "choices": [
    {
      "text": "Interroger les villageois",
      "next_scene": "gather_info",
      "effects": {"reputation": 1, "npcs_met": 1}
    },
    {
      "text": "Partir vers la forêt",
      "next_scene": "forest"
    }
  ]
}
```

### 3. Combat Scene (Combat)
```json
{
  "id": "boss_fight",
  "type": "combat",
  "title": "👹 COMBAT FINAL",
  "description": "Le chef gobelin rugit et charge!",
  "monsters": ["goblin_boss"],
  "on_victory": "victory",
  "on_defeat": "game_over"
}
```

### 4. Merchant Scene (Marchand)
```json
{
  "id": "merchant_1",
  "type": "merchant",
  "title": "🛒 BOUTIQUE DU VILLAGE",
  "merchant_id": "village",
  "next_scene": "village_choice"
}
```

### 5. Rest Scene (Repos)
```json
{
  "id": "rest_1",
  "type": "rest",
  "title": "💤 REPOS",
  "rest_type": "long",  # ou "short"
  "next_scene": "village_choice"
}
```

## 📝 Structure d'un fichier de scénario

```json
{
  "scenario_id": "chasse_gobelins",
  "name": "La Chasse aux Gobelins",
  "level": 3,
  "difficulty": "easy",
  "duration_hours": "1-2",
  "recommended_party_size": 2,
  "scenes": [
    // ... liste des scènes
  ]
}
```

## 🚀 Utilisation

### 1. Lancer un scénario JSON

```bash
cd /Users/display/PycharmProjects/DnD5e-Test
python play_scenario_from_json.py
```

### 2. Créer votre propre scénario

1. Créez un fichier JSON dans `data/scenes/mon_scenario.json`
2. Définissez les métadonnées du scénario
3. Ajoutez vos scènes (voir exemples ci-dessus)
4. Lancez le scénario

### 3. Utiliser le SceneFactory dans votre code

```python
from src.scenes.scene_factory import SceneFactory

# Charger un scénario depuis JSON
scene_manager = SceneFactory.load_scenario_from_json_file(
    "data/scenes/chasse_gobelins.json",
    monster_factory=monster_factory
)

# Créer le contexte de jeu
game_context = {
    'party': party,
    'game_state': game_state,
    'renderer': renderer,
    'combat_system': combat_system,
    'monster_factory': monster_factory,
    # ...
}

# Lancer le scénario
scene_manager.run(game_context)
```

## 🎲 Scénarios disponibles

### La Chasse aux Gobelins
- **Niveau**: 3
- **Durée**: 1-2h
- **Difficulté**: Facile
- **Fichier**: `data/scenes/chasse_gobelins.json`

### The Sunless Citadel
- **Niveau**: 1
- **Durée**: 2-3h
- **Difficulté**: Moyenne
- **Fichier**: `data/scenes/sunless_citadel.json`

### La Tombe des Rois Serpents
- **Niveau**: 2
- **Durée**: 2h
- **Difficulté**: Moyenne
- **Fichier**: `data/scenes/tombe_rois_serpents.json`

## 🔧 Fonctionnalités avancées

### Effets des choix

Les choix peuvent avoir des effets sur l'état du jeu :

```json
{
  "text": "Interroger les villageois",
  "next_scene": "gather_info",
  "effects": {
    "reputation": 1,
    "npcs_met": 1,
    "gold": 10
  }
}
```

### Récompenses de fin

Les scènes narratives peuvent donner des récompenses :

```json
{
  "id": "victory",
  "type": "narrative",
  "title": "🎉 VICTOIRE!",
  "text": "Vous avez sauvé le village!",
  "rewards": {
    "gold": 100,
    "xp": 450,
    "reputation": 5
  }
}
```

### Monstres personnalisés

Référencez des monstres par leur nom (index) :
- Utilisez les monstres du package `dnd_5e_core`
- Ou définissez vos propres monstres dans `data/monsters/`

```json
{
  "monsters": ["goblin", "goblin", "goblin_boss"]
}
```

## 🏗️ Architecture

Le système utilise plusieurs patterns de conception :

1. **Factory Pattern**: `SceneFactory` crée des objets scène depuis JSON
2. **Composite Pattern**: `SceneManager` gère l'arbre de scènes
3. **Strategy Pattern**: Chaque type de scène a son propre comportement
4. **Template Method**: `BaseScene` définit le squelette d'exécution

## 📚 Dépendances

- `dnd_5e_core`: Package principal des règles D&D 5e
- Python 3.12+
- Aucune dépendance externe supplémentaire

## 🎯 Avantages du système JSON

✅ **Simplicité**: Créez des aventures sans code Python  
✅ **Réutilisabilité**: Partagez facilement des scénarios  
✅ **Modularité**: Combinez des scènes comme des LEGO  
✅ **Maintenabilité**: Sépare contenu et logique  
✅ **Extensibilité**: Ajoutez de nouveaux types de scènes facilement  

## 🔮 Évolutions futures

- [ ] Éditeur visuel de scénarios
- [ ] Validation de schéma JSON
- [ ] Import/export de scénarios
- [ ] Générateur de scénarios aléatoires
- [ ] Support de conditions complexes
- [ ] Système de quêtes avec suivi

## 📖 Exemples complets

Consultez les fichiers dans `data/scenes/` pour des exemples complets de scénarios.

## 🤝 Contribution

Pour ajouter un nouveau type de scène :

1. Ajoutez la classe dans `src/scenes/scene_system.py`
2. Ajoutez le support dans `SceneFactory.create_scene_from_dict()`
3. Documentez le format JSON
4. Ajoutez des exemples

---

**Auteur**: DnD5e-Test Project  
**License**: MIT  
**Package utilisé**: [dnd-5e-core](https://pypi.org/project/dnd-5e-core/)

