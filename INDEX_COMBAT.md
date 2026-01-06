# 🎲 D&D 5e - Scripts de Combat avec Personnages Aléatoires

## 📌 Vue d'Ensemble

Ce projet contient plusieurs scripts de combat pour D&D 5e, dont **4 nouvelles versions** qui utilisent la fonction `generate_random_character()` pour créer des personnages aléatoires et les faire combattre contre des monstres sélectionnés automatiquement selon le **Challenge Rating**.

---

## 🆕 Nouveaux Scripts (Personnages Aléatoires)

### 1. 🎬 `demo_quick_combat.py` - DÉMO RAPIDE
**Pour:** Première découverte, démonstration rapide  
**Caractéristiques:**
- ✅ Chargement silencieux et rapide
- ✅ Affichage condensé
- ✅ État tous les 3 rounds (pas à chaque round)
- ✅ Parfait pour présenter le concept

**Lancer:**
```bash
python demo_quick_combat.py
```

---

### 2. 🔄 `auto_random_combat.py` - COMBAT AUTOMATIQUE
**Pour:** Tests automatisés, benchmarks  
**Caractéristiques:**
- ✅ Lance automatiquement sans attendre
- ✅ Affichage amélioré avec émojis
- ✅ Indicateurs de santé colorés (🟢🟡🔴)
- ✅ Statistiques finales détaillées

**Lancer:**
```bash
python auto_random_combat.py
```

---

### 3. ⚔️ `random_party_combat.py` - COMBAT ALÉATOIRE
**Pour:** Combats variés avec analyse préalable  
**Caractéristiques:**
- ⏸️ Pause avant le combat (Entrée pour lancer)
- ✅ 6 personnages aléatoires (niveaux 1-5)
- ✅ Monstres sélectionnés par CR
- ✅ Affichage standard round par round

**Lancer:**
```bash
python random_party_combat.py
```

---

### 4. 🏆 `advanced_random_combat.py` - VERSION AVANCÉE ⭐ RECOMMANDÉ
**Pour:** Simulations réalistes, analyse tactique complète  
**Caractéristiques:**
- ⏸️ Pause avant combat pour examiner les forces
- ✅ Interface enrichie professionnelle
- ✅ Affichage détaillé des stats de chaque personnage
- ✅ Analyse tactique de la rencontre (HP totaux, multiplicateurs, etc.)
- ✅ Rapport final complet (taux de survie, répartition XP)
- ✅ Statistiques de sorts, capacités, équipement
- ✅ Formatage avancé avec tableaux

**Lancer:**
```bash
python advanced_random_combat.py
```

**Exemple d'affichage:**
```
🛡️  LIGNE DE FRONT (3 combattants au corps-à-corps):
   1. Badger               Gnome        Warlock    Niv.2
      💚 HP:  16/ 16 | ⚔️ FOR:11 DEX:10 CON:10 | 🔮 3 sorts

📊  ANALYSE DE LA RENCONTRE
   Niveau moyen du groupe: 3.2
   HP total groupe: 212 | HP total monstres: 146
   Difficulté: MEDIUM (890 XP ajustés)
```

---

## 📜 Scripts Existants

### `combat.py` - Combat Simple
- 1 personnage (wizard) vs 1 monstre (orc)
- Personnages créés manuellement
- Bon pour apprendre les bases

### `party_combat.py` - Combat de Groupe
- 6 personnages vs monstres
- Personnages créés manuellement
- Utilise le Challenge Rating

---

## 🎯 Fonctionnalités Principales

### ✨ Génération Aléatoire
- **Races:** Elf, Dwarf, Human, Gnome, Dragonborn, Half-Elf, Halfling, Tiefling, Half-Orc
- **Classes:** Fighter, Wizard, Paladin, Rogue, Bard, Warlock, Ranger, Cleric, Druid, Sorcerer, Barbarian, Monk
- **Noms:** Générés aléatoirement selon la race
- **Niveaux:** Variables (1-5 ou 2-5 selon le script)
- **Sorts:** Assignés automatiquement aux lanceurs

### 🎖️ Système Tactique
- **3 en ligne de FRONT:** Attaques de mêlée, protègent l'arrière
- **3 en ligne ARRIÈRE:** Attaques à distance/sorts, protégés des attaques de mêlée

### 📊 Challenge Rating (CR)
- Calcul automatique du niveau moyen du groupe
- Sélection de monstres appropriés (CR min-max)
- Ajustement de la difficulté: `easy`, `medium`, `hard`, `deadly`
- Multiplicateurs selon le nombre de monstres
- Calcul des XP ajustés

---

## 🚀 Démarrage Rapide

### Installation
```bash
cd /Users/display/PycharmProjects/DnD5e-Test
# Les dépendances sont déjà installées
```

### Première Utilisation
```bash
# Démo rapide (5 minutes)
python demo_quick_combat.py

# Combat automatique complet (10-15 minutes)
python auto_random_combat.py

# Simulation avancée avec analyse (15-20 minutes)
python advanced_random_combat.py
```

---

## ⚙️ Personnalisation

### Changer la Difficulté
Éditez le script et modifiez:
```python
difficulty = "hard"  # 'easy', 'medium', 'hard', 'deadly'
```

### Changer les Niveaux
```python
party = create_random_party(
    size=6,
    min_level=5,   # Modifier ici
    max_level=10,  # Et ici
    ...
)
```

### Changer le Nombre de Combattants
```python
party = create_random_party(
    size=4,  # Au lieu de 6
    ...
)
```

---

## 📚 Documentation

### Guides Complets
- **`README_COMBAT.md`** - Guide détaillé de tous les scripts, exemples, personnalisation
- **`SUMMARY_RANDOM_COMBAT.md`** - Résumé technique, concepts D&D, améliorations futures

### Utilitaires
- **`list_combat_scripts.py`** - Affiche la liste de tous les scripts disponibles

**Lancer:**
```bash
python list_combat_scripts.py
```

---

## 🎓 Concepts D&D 5e

- **Challenge Rating (CR):** Difficulté d'un monstre (0-30)
- **XP Thresholds:** Seuils d'XP par niveau pour easy/medium/hard/deadly
- **Encounter Multiplier:** x1.5 (2 monstres), x2 (3-6), x2.5 (7-10), etc.
- **Ability Scores:** STR, DEX, CON, INT, WIS, CHA (3-20)
- **Spell Slots:** Emplacements de sorts par niveau
- **Hit Dice:** d6 (Wizard), d8 (Rogue), d10 (Fighter), d12 (Barbarian)

---

## 🔧 Architecture Technique

### Dépendances
- `dnd-5e-core` (PyPI): Entités, combat system, mechanics
- `DnD-5th-Edition-API` (local): Collections de données, `generate_random_character()`

### Fichiers Principaux
```
DnD5e-Test/
├── demo_quick_combat.py          # Démo rapide
├── auto_random_combat.py         # Auto complet
├── random_party_combat.py        # Avec pause
├── advanced_random_combat.py     # Version avancée ⭐
├── combat.py                     # Simple (1v1)
├── party_combat.py               # Groupe manuel
├── README_COMBAT.md              # Guide complet
├── SUMMARY_RANDOM_COMBAT.md      # Résumé technique
├── INDEX_COMBAT.md               # Ce fichier
└── list_combat_scripts.py        # Utilitaire
```

---

## 📊 Tableau Comparatif

| Script | Personnages | Auto | Random | Affichage | Niveau |
|--------|-------------|------|--------|-----------|--------|
| `demo_quick_combat.py` | 6 | ❌ | ✅ | Condensé | ⭐ |
| `auto_random_combat.py` | 6 | ✅ | ✅ | Amélioré | ⭐⭐⭐ |
| `random_party_combat.py` | 6 | ❌ | ✅ | Standard | ⭐⭐⭐ |
| `advanced_random_combat.py` | 6 | ❌ | ✅ | Détaillé | ⭐⭐⭐⭐ |
| `party_combat.py` | 6 | ✅ | ❌ | Standard | ⭐⭐ |
| `combat.py` | 1 | ✅ | ❌ | Basique | ⭐ |

**Légende:**
- **Auto:** Lance automatiquement sans pause
- **Random:** Utilise `generate_random_character()`
- **Niveau:** Complexité/fonctionnalités

---

## 💡 Recommandations

| Situation | Script Recommandé |
|-----------|-------------------|
| 🎬 Découverte | `demo_quick_combat.py` |
| 🧪 Tests/Debug | `auto_random_combat.py` |
| 📊 Analyse tactique | `advanced_random_combat.py` |
| 🎮 Session de jeu | `random_party_combat.py` |
| 📚 Apprentissage | `combat.py` |

---

## ✅ Réalisation Complète

**Objectif initial:** Créer une version de combat utilisant `generate_random_character()`.

**Résultat:** 
- ✅ 4 scripts différents (du simple au très avancé)
- ✅ Personnages totalement aléatoires (races, classes, noms, niveaux)
- ✅ Système tactique front/arrière
- ✅ Challenge Rating automatique
- ✅ Documentation complète
- ✅ Personnalisation facile
- ✅ Tous testés et fonctionnels

---

## 🚀 Prochaines Étapes

Pour aller plus loin:
1. Tester chaque script pour découvrir leurs différences
2. Personnaliser les niveaux et difficultés
3. Analyser les stratégies de combat
4. Expérimenter avec différentes compositions de groupe

---

## 📞 Support

Pour plus d'informations, consultez:
- `README_COMBAT.md` - Guide utilisateur complet
- `SUMMARY_RANDOM_COMBAT.md` - Documentation technique
- `python list_combat_scripts.py` - Liste interactive

---

**Bon combat! ⚔️🎲**

