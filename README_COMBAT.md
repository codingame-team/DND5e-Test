# Scripts de Combat D&D 5e

Ce dossier contient plusieurs scripts de combat utilisant le package `dnd-5e-core` et l'API D&D 5e.

## Tableau de Comparaison Rapide

| Script | Personnages | Génération | Auto | Affichage | Recommandé pour |
|--------|-------------|------------|------|-----------|-----------------|
| `combat.py` | 1 (manuel) | Manuel | ✅ | Basique | Apprentissage |
| `party_combat.py` | 6 (manuels) | Manuel | ✅ | Standard | Tests avec personnages fixes |
| `random_party_combat.py` | 6 (aléatoires) | **Aléatoire** | ❌ (pause) | Standard | Combats variés |
| `auto_random_combat.py` | 6 (aléatoires) | **Aléatoire** | ✅ | Amélioré | Tests automatisés |
| `advanced_random_combat.py` | 6 (aléatoires) | **Aléatoire** | ❌ (pause) | **Détaillé** | **Simulations réalistes** ⭐ |

**Légende:**
- ✅ Auto = Lance automatiquement
- ❌ Pause = Attend une entrée utilisateur avant de combattre
- **Aléatoire** = Utilise `generate_random_character()` de main.py

## Scripts Disponibles

### 1. `combat.py`
Combat simple: 1 personnage (wizard créé manuellement) vs 1 monstre (orc).
- Utilise `dnd_5e_core.combat.CombatSystem`
- Bon pour apprendre les bases du système de combat

### 2. `party_combat.py`
Combat avec un groupe de 6 aventuriers créés manuellement vs monstres.
- 3 personnages en ligne de front (mêlée)
- 3 personnages en ligne arrière (distance/sorts)
- Utilise le système de Challenge Rating pour équilibrer la rencontre
- Les personnages sont créés manuellement avec des classes et races spécifiques

### 3. `random_party_combat.py` ⭐ NOUVEAU
Combat avec un groupe de 6 aventuriers **ALÉATOIRES** vs monstres.
- Utilise `generate_random_character()` de `main.py` pour créer des personnages
- Les personnages ont des niveaux variables (1-5)
- Les monstres sont sélectionnés automatiquement selon le Challenge Rating
- 3 personnages en ligne de front (attaques de mêlée uniquement)
- 3 personnages en ligne arrière (attaques à distance et sorts)
- **Attend une entrée utilisateur** avant de commencer le combat

**Usage:**
```bash
cd /Users/display/PycharmProjects/DnD5e-Test
python random_party_combat.py
```

### 4. `auto_random_combat.py` ⭐ NOUVEAU - VERSION AUTO
Identique à `random_party_combat.py` mais **lance automatiquement** le combat sans attendre.
- Parfait pour les tests et démonstrations
- Affichage amélioré avec émojis et indicateurs de santé
- Statistiques détaillées en fin de combat

**Usage:**
```bash
cd /Users/display/PycharmProjects/DnD5e-Test
python auto_random_combat.py
```

### 6. `create_character.py`
Exemple de création d'un personnage unique.
- Montre comment créer manuellement un personnage
- Utile pour comprendre la structure des personnages

### 7. `create_monster.py`
Exemple de chargement de monstres depuis les données.
- Utilise `ExtendedMonsterLoader` pour charger des monstres
- Recherche et filtrage de monstres par nom et CR

## Caractéristiques des Combats Aléatoires

### Organisation du Groupe (6 personnages)

**Ligne de Front (indices 0-2):**
- Peuvent effectuer des **attaques de mêlée**
- Peuvent être atteints par les attaques de mêlée des monstres
- Classes typiques: Fighter, Paladin, Barbarian, Monk

**Ligne Arrière (indices 3-5):**
- Effectuent des **attaques à distance** ou lancent des **sorts**
- **Ne peuvent PAS** être atteints par les attaques de mêlée des monstres
- Peuvent être ciblés par des sorts et attaques spéciales
- Classes typiques: Wizard, Sorcerer, Ranger, Bard, Warlock

### Challenge Rating (CR)

Le système utilise `dnd_5e_core.mechanics.challenge_rating` pour:
- Calculer le niveau moyen du groupe
- Déterminer la plage de CR appropriée
- Sélectionner des monstres pour une difficulté équilibrée
- Calculer les XP ajustés et la difficulté finale

**Niveaux de difficulté:**
- `trivial`: Très facile
- `easy`: Facile
- `medium`: Moyen (par défaut)
- `hard`: Difficile
- `deadly`: Mortel

### Niveaux des Personnages

Par défaut:
- `random_party_combat.py`: niveaux 1-5
- `auto_random_combat.py`: niveaux 2-5 (pour plus d'action)

Vous pouvez modifier ces valeurs dans la fonction `create_random_party()`:
```python
party = create_random_party(
    size=6,
    min_level=1,  # Modifiez ici
    max_level=10,  # Et ici
    ...
)
```

### Modificer la Difficulté

Dans la fonction `select_monsters_for_encounter()`:
```python
monsters = select_monsters_for_encounter(
    party_levels=party_levels,
    monsters_db=monsters_db,
    difficulty="deadly"  # Changez 'medium' en 'easy', 'hard', ou 'deadly'
)
```

## Dépendances

- `dnd-5e-core`: Package principal avec les entités et le système de combat
- `DnD-5th-Edition-API`: Pour la fonction `generate_random_character()` et les collections de données

## Affichage du Combat

Le système affiche:
- 🗡️ Ligne de front
- 🏹 Ligne arrière
- 👹 Monstres avec leur CR
- 📊 Difficulté de la rencontre et XP ajustés
- ⚔️ Actions de combat round par round
- 🟢🟡🔴 Indicateurs de santé (>50%, 25-50%, <25%)
- 🎉 Résultat final avec survivants et pertes

## Exemples de Sortie

```
================================================================================
  ⚔️  DÉBUT DU COMBAT  ⚔️
================================================================================

🗡️  LIGNE DE FRONT (Attaques de mêlée):
  1. Badger (Gnome Warlock Niv.2)
     HP: 16/16 | STR: 11 DEX: 10 CON: 10

🏹  LIGNE ARRIÈRE (Attaques à distance et sorts):
  1. Pock (Gnome Bard Niv.3)
     HP: 21/21 | INT: 11 WIS: 14 CHA: 15
     Magie: 4 sorts connus

👹  MONSTRES:
  1. White Dragon Wyrmling - CR 2 | HP: 32/32 | CA: 16

📊  Difficulté: MEDIUM (450 XP ajusté)
```

## Notes Techniques

- Les personnages sans armes équipées utilisent des attaques à mains nues (1-2 dégâts)
- Les lanceurs de sorts utilisent leurs sorts de manière aléatoire
- Les monstres priorisent la ligne de front pour les attaques de mêlée
- Le combat s'arrête après 30 rounds pour éviter les boucles infinies
- Les HP sont ajustés selon le niveau: `(hit_die + con_modifier) * level`

## Améliorations Futures

- [ ] Permettre le choix interactif de la composition du groupe
- [ ] Ajouter des tactiques de combat plus avancées
- [ ] Implémenter le système de mort et d'inconscience (death saves)
- [ ] Ajouter des équipements aux personnages générés
- [ ] Gérer les zones de combat et la portée des attaques
- [ ] Interface graphique avec pygame

