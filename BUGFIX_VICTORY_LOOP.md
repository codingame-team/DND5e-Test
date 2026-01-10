# Fix: Boucle Infinie sur Scène de Victoire

## 🐛 Problème Identifié

**Symptôme:** La scène de victoire se répète en boucle infinie, le joueur ne peut pas terminer le scénario.

```
======================================================================
  🎉 VICTOIRE!
======================================================================

Vous avez vaincu le chef gobelin!
...

💾 Sauvegarder la partie? (o/n): o
✅ Partie sauvegardée: autosave
✅ Partie sauvegardée: autosave    <- Se répète!

[Appuyez sur ENTRÉE pour continuer]

======================================================================
  🎉 VICTOIRE!                       <- Boucle infinie!
======================================================================
```

---

## 🔍 Cause du Problème

### Code Défectueux

Dans `/src/scenes/scene_system.py`, la méthode `SceneManager.execute_scene()` :

```python
def execute_scene(self, scene_id: str, game_context: Dict) -> SceneResult:
    scene = self.scenes[scene_id]
    result = scene.execute(game_context)
    
    # ❌ PROBLÈME ICI
    if scene.next_scene_id:
        self.current_scene_id = scene.next_scene_id
    
    return result
```

**Problème:** Quand `scene.next_scene_id` est `None` (scène finale), `current_scene_id` n'est jamais mis à jour et reste sur la scène actuelle.

### Boucle While

Dans `SceneManager.run()` :

```python
while self.current_scene_id:  # Continue tant que current_scene_id n'est pas None
    result = self.execute_scene(self.current_scene_id, game_context)
    # ...
```

**Résultat:** Comme `current_scene_id` n'est jamais mis à `None`, la boucle s'exécute indéfiniment sur la même scène de victoire.

---

## ✅ Solution Implémentée

### 1. Correction de `execute_scene()`

**Avant:**
```python
# Mettre à jour scène courante
if scene.next_scene_id:
    self.current_scene_id = scene.next_scene_id
```

**Après:**
```python
# Mettre à jour scène courante
# Si next_scene_id est None, on termine le scénario
self.current_scene_id = scene.next_scene_id
```

**Effet:** Maintenant, si `next_scene_id` est `None`, `current_scene_id` devient aussi `None`, ce qui termine la boucle.

### 2. Amélioration de `run()` avec Messages

**Ajout:**
```python
# Si pas de prochaine scène, fin du scénario
if not self.current_scene_id:
    print("\n" + "="*70)
    print("🏁 Fin du scénario - Merci d'avoir joué!")
    print("="*70)
    break
```

---

## 🧪 Tests Ajoutés

### 1. `test/test_victory_scene.py`
Vérifie que la scène de victoire a bien `next_scene_id = None`.

```python
victory_scene = scenario.scene_manager.scenes.get('victory')
assert victory_scene.next_scene_id is None  # ✅
```

### 2. `test/test_end_scenario.py`
Simule l'exécution de la scène de victoire et vérifie que `current_scene_id` devient `None`.

```python
scenario.scene_manager.execute_scene('victory', game_context)
assert scenario.scene_manager.current_scene_id is None  # ✅
```

---

## 📊 Résultat Attendu

### Avant (Boucle Infinie)
```
🎉 VICTOIRE!
💾 Sauvegarder...
[ENTER]
🎉 VICTOIRE!      <- Répète
💾 Sauvegarder...
[ENTER]
🎉 VICTOIRE!      <- Répète encore
...
```

### Après (Termine Correctement)
```
🎉 VICTOIRE!
💾 Sauvegarder la partie? (o/n): o
✅ Partie sauvegardée: autosave
[Appuyez sur ENTRÉE pour continuer]

======================================================================
🏁 Fin du scénario - Merci d'avoir joué!
======================================================================
```

---

## 📝 Fichiers Modifiés

- ✅ `/src/scenes/scene_system.py` - Correction de `execute_scene()` et `run()`
- ✅ `/test/test_victory_scene.py` - Test de la scène de victoire
- ✅ `/test/test_end_scenario.py` - Test de fin de scénario

---

## 🎯 Impact

Cette correction s'applique à **tous les scénarios** utilisant le système de scènes JSON :
- ✅ La Chasse aux Gobelins
- ✅ La Tombe des Rois Serpents
- ✅ Tales from the Yawning Portal

Toute scène avec `"next_scene": null` terminera maintenant correctement le scénario.

---

## 🚀 Vérification

Pour vérifier la correction :
```bash
# Jouer jusqu'à la fin
python chasse_gobelins_refactored.py

# Ou tester directement
python test/test_victory_scene.py
python test/test_end_scenario.py
```

---

**Date:** 10 janvier 2026  
**Statut:** ✅ CORRIGÉ  
**Commit:** `8280d99`  
**Gravité:** Haute (bloquait la fin du jeu)

