# DnD5e-Test

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Scripts de démonstration et exemples d'utilisation du package [dnd-5e-core](https://github.com/codingame-team/dnd-5e-core)**

Ce dépôt contient des exemples pratiques et des scripts de démonstration montrant comment utiliser le package `dnd-5e-core` pour créer des systèmes de combat D&D 5e, générer des personnages aléatoires, et construire des rencontres équilibrées selon les règles officielles.

## ✨ Fonctionnalités

- 🎲 **Combat aléatoire** - 4 versions de scripts de combat avec personnages générés aléatoirement
- ⚔️ **Système de rencontres D&D 5e** - Génération de rencontres selon les tables officielles du DMG
- 👥 **Création de personnages** - Exemples de génération manuelle et aléatoire
- 👹 **Gestion de monstres** - Chargement et recherche dans la base de données de monstres
- 📊 **Challenge Rating** - Système de calcul de difficulté conforme aux règles D&D 5e

## 📚 Table des Matières

- [Scripts de Combat](#-scripts-de-combat)
- [Scripts de Création](#-scripts-de-création)
- [Installation](#-installation)
- [Démarrage Rapide](#-démarrage-rapide)

## ⚔️ Scripts de Combat

Ce projet contient plusieurs scripts de combat pour D&D 5e, dont **4 versions avec personnages aléatoires**.

### 🚀 Démarrage Rapide - Combat

```bash
# Démo rapide (première découverte)
python demo_quick_combat.py

# Combat automatique complet
python auto_random_combat.py

# Simulation complète avec statistiques détaillées ⭐
python advanced_random_combat.py
```

### 📋 Tous les Scripts de Combat

| Script                      | Description                         | Niveau |
|-----------------------------|-------------------------------------|--------|
| `demo_quick_combat.py`      | Démo rapide et condensée            | ⭐      |
| `auto_random_combat.py`     | Combat automatique complet          | ⭐⭐⭐    |
| `random_party_combat.py`    | Combat avec pause d'analyse         | ⭐⭐⭐    |
| `advanced_random_combat.py` | Version avancée avec stats          | ⭐⭐⭐⭐   |
| `party_combat.py`           | 6 personnages (manuels) vs monstres | ⭐⭐     |
| `combat.py`                 | Combat simple 1v1                   | ⭐      |

### 📖 Documentation Complète

- **[INDEX_COMBAT.md](INDEX_COMBAT.md)** - Vue d'ensemble et démarrage
- **[README_COMBAT.md](README_COMBAT.md)** - Guide détaillé
- **[SUMMARY_RANDOM_COMBAT.md](SUMMARY_RANDOM_COMBAT.md)** - Documentation technique
- **[MISSION_ACCOMPLIE.md](MISSION_ACCOMPLIE.md)** - Résumé du projet

### ✨ Fonctionnalités des Scripts Aléatoires

- ✅ 6 personnages générés aléatoirement avec `generate_random_character()`
- ✅ Niveaux variables (2-5)
- ✅ Système tactique: 3 en FRONT (mêlée) + 3 en ARRIÈRE (distance/sorts)
- ✅ Sélection automatique des monstres par Challenge Rating
- ✅ 4 niveaux de difficulté: easy, medium, hard, deadly
- ✅ Affichage progressif (basique → détaillé)

## 👤 Scripts de Création

### Personnages

- **`create_character.py`** - Exemple de création manuelle d'un personnage
- Montre comment créer un personnage avec race, classe, capacités

### Monstres

- **`create_monster.py`** - Exemple de chargement de monstres
- Utilise `ExtendedMonsterLoader` pour rechercher et filtrer

## 📦 Installation

### Prérequis

```bash
# Le package dnd-5e-core doit être installé
pip install dnd-5e-core

# OU en développement
cd /Users/display/PycharmProjects/dnd-5e-core
pip install -e .
```

### Dépendances

- `dnd-5e-core` (PyPI) - Package principal
- `DnD-5th-Edition-API` (local) - Pour `generate_random_character()`

## 🚀 Démarrage Rapide

### 1. Lister tous les scripts disponibles

```bash
python list_combat_scripts.py
```

### 2. Premier combat

```bash
# Le plus simple pour commencer
python demo_quick_combat.py
```

### 3. Créer un personnage

```bash
python create_character.py
```

### 4. Charger des monstres

```bash
python create_monster.py
```

## 🎯 Cas d'Usage

### Pour Apprendre

```bash
# Combat simple 1v1
python combat.py

# Création de personnage
python create_character.py
```

### Pour Tester

```bash
# Tests automatisés
python auto_random_combat.py
```

### Pour Simuler des Combats

```bash
# Simulation réaliste complète
python advanced_random_combat.py
```

## ⚙️ Personnalisation

### Modifier la Difficulté

Éditez le script et changez:
```python
difficulty = "hard"  # 'easy', 'medium', 'hard', 'deadly'
```

### Modifier les Niveaux

```python
min_level = 5
max_level = 10
```

### Modifier le Nombre de Personnages

```python
size = 4  # Au lieu de 6
```

## 📊 Structure du Projet

```
DnD5e-Test/
├── combat.py                      # Combat simple 1v1
├── party_combat.py                # Groupe de 6 (manuel)
├── demo_quick_combat.py           # Démo rapide ⭐
├── auto_random_combat.py          # Auto complet ⭐⭐⭐
├── random_party_combat.py         # Avec pause ⭐⭐⭐
├── advanced_random_combat.py      # Version avancée ⭐⭐⭐⭐
├── create_character.py            # Création personnage
├── create_monster.py              # Chargement monstres
├── list_combat_scripts.py         # Utilitaire
├── README.md                      # Ce fichier
├── INDEX_COMBAT.md                # Guide combat
├── README_COMBAT.md               # Doc détaillée
├── SUMMARY_RANDOM_COMBAT.md       # Doc technique
└── MISSION_ACCOMPLIE.md           # Résumé projet
```

## 🔧 Concepts D&D 5e

Les scripts utilisent les concepts officiels de D&D 5e:

- **Challenge Rating (CR)** - Difficulté des monstres
- **XP Thresholds** - Seuils d'XP par niveau
- **Encounter Multiplier** - Multiplicateur de rencontre
- **Ability Scores** - STR, DEX, CON, INT, WIS, CHA
- **Spell Slots** - Emplacements de sorts
- **Hit Dice** - Dés de vie par classe

## 📝 Notes

- Les personnages sans armes utilisent des attaques à mains nues (1-2 dégâts)
- Les lanceurs de sorts utilisent intelligemment leurs sorts
- Les combats sont limités à 30 rounds maximum
- HP calculés: `(hit_die + con_modifier) * level`

## 🎓 Apprendre D&D 5e

Ces scripts sont parfaits pour:

- ✅ Comprendre le système de combat D&D 5e
- ✅ Apprendre le Challenge Rating
- ✅ Tester différentes compositions de groupe
- ✅ Analyser les stratégies de combat
- ✅ Expérimenter avec les règles

## 🆘 Support

Pour plus d'informations:

1. Consultez la documentation: `README_COMBAT.md`
2. Lisez les guides: `INDEX_COMBAT.md`, `SUMMARY_RANDOM_COMBAT.md`
3. Lancez: `python list_combat_scripts.py`

## 📜 Licence

Voir le fichier LICENSE du projet parent.

## 🙏 Crédits

- Package `dnd-5e-core` - Système de combat et entités
- API D&D 5e - Données de référence
- Wizards of the Coast - D&D 5e SRD

---

**Bon jeu! ⚔️🎲**

