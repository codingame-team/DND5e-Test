# 🎲 Nouveaux Scénarios Ajoutés

## Date: 11 Janvier 2026

Deux nouveaux scénarios ont été ajoutés au projet DnD5e-Scenarios, basés sur les aventures disponibles sur https://www.aidedd.org/adj/scenarios/

---

## 👁️ L'Oeil de Gruumsh

### Informations générales
- **Niveau recommandé**: 3
- **Durée**: 2-3 heures
- **Difficulté**: Moyenne
- **Taille du groupe**: 4 personnages
- **Fichier**: `oeil_gruumsh_game.py`
- **JSON**: `data/scenes/oeil_de_gruumsh.json`

### Synopsis
Les Montagnes de Fer sont en proie à une nouvelle menace. Une tribu d'orques, menée par un redoutable Oeil de Gruumsh (prêtre fanatique du dieu orque), a établi son campement dans les hauteurs et terrorise la vallée.

Les aventuriers doivent:
1. Enquêter au village de la vallée
2. Affronter les patrouilles orques dans la montagne
3. Infiltrer le campement ennemi
4. Vaincre l'Oeil de Gruumsh et ses guerriers d'élite

### Monstres inclus
- **Orc** (CR 0.5) - Guerriers féroces avec capacité Aggressive
- **Orc Eye of Gruumsh** (CR 2) - Prêtre-guerrier avec sorts et Gruumsh's Fury

### Particularités
- Choix tactiques: approche furtive vs frontale
- Possibilité de contourner certains combats
- Boss fight épique avec 3 ennemis
- 22 scènes différentes

### Lancer le scénario
```bash
python oeil_gruumsh_game.py
```

---

## 💀 La Secte du Crâne

### Informations générales
- **Niveau recommandé**: 4
- **Durée**: 2-3 heures
- **Difficulté**: Difficile
- **Taille du groupe**: 4 personnages
- **Fichier**: `secte_du_crane_game.py`
- **JSON**: `data/scenes/secte_du_crane.json`

### Synopsis
La ville de Ravencrest est troublée par d'étranges événements: disparitions mystérieuses, symboles sinistres, chuchotements nocturnes. Une secte du Crâne opère dans les ombres, cherchant l'immortalité par la nécromancie.

Les aventuriers doivent:
1. Enquêter en ville sur les disparitions
2. Explorer l'église abandonnée
3. S'infiltrer dans les catacombes
4. Libérer les prisonniers
5. Arrêter le rituel du Prêtre de la Mort

### Monstres inclus
- **Cultist** (CR 0.125) - Membres de base de la secte
- **Cult Fanatic** (CR 2) - Fanatiques avec sorts
- **Shadow** (CR 0.5) - Ombres vivantes invoquées
- **Death Priest** (CR 3) - Boss final avec puissants sorts de nécromancie

### Particularités
- Atmosphère d'horreur et mystère
- Exploration de catacombes
- Possibilité de sauver les prisonniers
- Combats contre créatures mort-vivantes
- Boss fight final très difficile (4 ennemis)
- 21 scènes différentes

### Lancer le scénario
```bash
python secte_du_crane_game.py
```

---

## 🎮 Intégration

Les deux scénarios sont maintenant intégrés dans:

1. **play_scenarios.py** - Launcher principal
   - Option 4: L'Oeil de Gruumsh
   - Option 5: La Secte du Crâne

2. **README.md** - Documentation mise à jour avec les 5 scénarios

3. **data/monsters/all_monsters.json** - 6 nouveaux monstres ajoutés

---

## 📊 Statistiques du projet

### Scénarios disponibles: 5
1. La Chasse aux Gobelins (Niveau 3, Facile)
2. The Sunless Citadel (Niveau 1, Moyenne)
3. La Tombe des Rois Serpents (Niveau 2, Moyenne)
4. **L'Oeil de Gruumsh** (Niveau 3, Moyenne) ✨ NOUVEAU
5. **La Secte du Crâne** (Niveau 4, Difficile) ✨ NOUVEAU

### Monstres disponibles: 12
- goblin, goblin_boss
- snake_guardian, snake_king
- giant_spider
- skeleton
- **orc, orc_eye_of_gruumsh** ✨ NOUVEAU
- **cultist, cult_fanatic** ✨ NOUVEAU
- **shadow, death_priest** ✨ NOUVEAU

---

## ✅ Tests effectués

- [x] Validation JSON des deux nouveaux scénarios
- [x] 22 scènes pour L'Oeil de Gruumsh
- [x] 21 scènes pour La Secte du Crâne
- [x] 6 nouveaux monstres avec stats complètes D&D 5e
- [x] Intégration dans play_scenarios.py
- [x] Mise à jour de la documentation

---

## 🎯 Prochaines étapes possibles

D'autres scénarios disponibles sur aidedd.org pourraient être ajoutés:
- Le Collier de Zark
- Le Masque Utruz
- L'Auberge du Sanglier Gris
- Les Cryptes de Kelemvor
- Et bien d'autres...

Le système de scénarios JSON rend l'ajout de nouveaux scénarios très simple!

