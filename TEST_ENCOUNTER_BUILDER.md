# Test du Système de Rencontre D&D 5e

## Description

Ce script (`test_encounter_builder.py`) démontre l'utilisation du système de génération de rencontres D&D 5e avec un groupe d'aventuriers de 4 à 6 personnages.

## Fonctionnalités

### 🎲 Génération de Groupe
- **Taille variable**: 4 à 6 personnages (aléatoire)
- **Classes diversifiées**: Fighter, Wizard, Cleric, Rogue, Ranger, Paladin
- **Niveaux variés**: Niveau moyen 5 avec variation ±1
- **Équipement complet**: Armes et armures appropriées à chaque classe

### ⚔️ Système de Rencontre
Utilise `encounter_builder.py` pour:
- **Tables officielles D&D 5e**: Basées sur le DMG (Dungeon Master's Guide)
- **Rencontres équilibrées**: Selon le niveau moyen du groupe
- **Deux types de rencontres**:
  - **Paires**: 2 monstres de CR différents
  - **Groupes**: Plusieurs monstres du même CR
- **Récompenses**: Or et XP selon le niveau de la rencontre

### 💥 Combat Complet
- **CombatSystem** automatique avec:
  - Spellcasting (sorts automatiques pour personnages et monstres)
  - Attaques d'armes équipées
  - Gestion des HP et conditions
  - Tours de combat détaillés
- **Formation tactique**: Front row (mêlée) et back row (sorts/distance)
- **Statistiques détaillées**: Survivants, HP restants, sorts utilisés

## Utilisation

```bash
python test_encounter_builder.py
```

## Exemple de Sortie

```
================================================================================
🎲 TEST DU SYSTÈME DE RENCONTRE D&D 5E
================================================================================

📋 ÉTAPE 1: Création du groupe d'aventuriers
--------------------------------------------------------------------------------
Taille du groupe: 6 aventuriers
  ✅ Conan: Niveau 6 Fighter - 41 HP
  ✅ Gandalf: Niveau 5 Fighter - 28 HP
  ✅ Friar: Niveau 6 Cleric - 42 HP
  ✅ Shadowblade: Niveau 4 Wizard - 26 HP
  ✅ Aragorn: Niveau 5 Ranger - 31 HP
  ✅ Lancelot: Niveau 4 Paladin - 12 HP

⚔️ ÉTAPE 2: Équipement du groupe
--------------------------------------------------------------------------------
  Conan: Longsword + Chain Mail (AC 16)
  Gandalf: Longsword + Chain Mail (AC 16)
  Friar: Mace + Chain Mail (AC 16)
  Shadowblade: Dagger (Pas d'armure)
  Aragorn: Longbow + Scale Mail (AC 14)
  Lancelot: Greatsword + Chain Mail (AC 16)

🎯 ÉTAPE 4: Génération de la rencontre
--------------------------------------------------------------------------------
Niveau moyen du groupe: 5

Options de rencontre pour niveau 5:
  - Paires possibles: CR 4 + CR 2
  - Groupes possibles:
    • 1 monstres de CR [4, 5, 6]
    • 2 monstres de CR [3]
    • 3 monstres de CR [2]
    • 4 monstres de CR [1, 2]
    • 5-6 monstres de CR [1]

✨ Rencontre générée: Type 'group'
   Nombre de monstres: 3
   Composition:
     • 3x Berserker (CR 2.0, 67 HP, AC 13)

💰 Récompense potentielle: 1600 pièces d'or

⚔️ ÉTAPE 5: COMBAT!
================================================================================

📊 Formation du groupe:
  [0] Conan (Fighter Niv.6): Front (Mêlée) - 41 HP
  [1] Gandalf (Fighter Niv.5): Front (Mêlée) - 28 HP
  [2] Friar (Cleric Niv.6): Front (Mêlée) - 42 HP
  [3] Lancelot (Paladin Niv.4): Back (Distance/Sorts) - 12 HP
  [4] Shadowblade (Wizard Niv.4): Back (Distance/Sorts) - 26 HP
  [5] Aragorn (Ranger Niv.5): Back (Distance/Sorts) - 31 HP

================================================================================
ROUND 1
================================================================================
Conan attacks Berserker!
Conan slashes Berserker for 4 hit points!
...
Shadowblade attacks Berserker!
Shadowblade CAST SPELL ** ACID ARROW ** on Berserker
Berserker is hit for 7 hit points!
...

================================================================================
📊 RÉSULTATS DU COMBAT
================================================================================

✅ VICTOIRE! Le groupe l'emporte!

   Survivants (6/6):
     ❤️ Conan: 41/41 HP (100%)
     ❤️ Gandalf: 20/28 HP (71%)
     ❤️ Friar: 42/42 HP (100%)
     ❤️ Lancelot: 12/12 HP (100%)
     ❤️ Shadowblade: 26/26 HP (100%)
     ❤️ Aragorn: 31/31 HP (100%)

   🔮 Shadowblade - Slots de sorts restants: [1, 3, 0, 0, 0]
   🔮 Lancelot - Slots de sorts restants: [0, 0, 0, 0, 0]

   💰 Le groupe obtient 1600 pièces d'or!

📈 Statistiques:
   - Nombre de rounds: 3
   - Type de rencontre: group
   - Niveau de rencontre: 5
   - Taille du groupe: 6 aventuriers
   - Nombre de monstres: 3
```

## Fonctionnalités Clés

### 📊 Encounter Builder

Le système utilise les **tables officielles D&D 5e** du DMG:

```python
from dnd_5e_core.mechanics.encounter_builder import (
    select_monsters_by_encounter_table,
    get_encounter_info
)

# Générer une rencontre équilibrée
monsters, encounter_type = select_monsters_by_encounter_table(
    encounter_level=5,
    available_monsters=all_monsters,
    allow_pairs=True
)
```

**Options de rencontre**:
- **1 monstre**: CR élevé (boss fight)
- **2-3 monstres**: CR moyen
- **4-6 monstres**: CR faible
- **7-12 monstres**: CR très faible
- **Paires**: 2 monstres de CR différents pour variété

### 🎯 Équilibrage Automatique

Le système ajuste automatiquement:
- **Nombre de monstres** selon le niveau du groupe
- **CR des monstres** pour un défi approprié
- **Récompenses en or** selon les tables DMG
- **Formation tactique** pour maximiser l'efficacité

### 🔮 Spellcasting Intelligent

Les lanceurs de sorts en position arrière (3+):
- **Lancent automatiquement** leurs meilleurs sorts
- **Gèrent leurs spell slots** intelligemment
- **Utilisent cantrips** quand plus de slots
- **Affichage des sorts utilisés** à la fin du combat

### ⚔️ Combat Réaliste

- **Armes équipées** utilisées correctement (slashes vs punches)
- **Armures** augmentent l'AC
- **Multi-attaques** pour certains monstres
- **Attaques spéciales** (breath weapon, etc.)
- **Gestion automatique** des tours de combat

## Étapes du Script

1. **Création du groupe** (4-6 personnages avec classes variées)
2. **Équipement** (armes et armures appropriées)
3. **Chargement des monstres** (332 monstres D&D 5e)
4. **Génération de rencontre** (via encounter_builder)
5. **Combat** (système automatique avec détails)
6. **Résultats** (statistiques complètes)

## Variables Ajustables

Dans le script, vous pouvez modifier:

```python
# Niveau du groupe
party_level = 5  # Changez pour d'autres niveaux (1-20)

# Taille du groupe (fixe au lieu d'aléatoire)
party_size = 6  # Au lieu de randint(4, 6)

# Classes spécifiques
char_class = "wizard"  # Forcer une classe

# Type de rencontre
allow_pairs=True  # False pour seulement des groupes
```

## Dépendances

- `dnd-5e-core` package
- `encounter_builder.py` (système de rencontre)
- `gold_rewards.py` (récompenses)
- `CombatSystem` (combat automatique)

## Résultats Possibles

- ✅ **Victoire**: Le groupe survit, gains d'or et XP
- ❌ **Défaite**: Les monstres gagnent
- 🤝 **Match nul**: Tous tombent (rare)

## Notes

- Les rencontres sont **aléatoires** à chaque exécution
- Le **niveau 5** est idéal pour des combats équilibrés
- Les **sorts sont automatiques** pour les classes appropriées
- La **formation du groupe** affecte la stratégie de combat

## Voir Aussi

- `test_spellcasting.py` - Test simple avec spellcasting
- `test.py` - Tests de combat de base
- `launcher.py` - Lanceur de scénarios
- `COMBAT_EXAMPLES.md` - Guide complet des combats

