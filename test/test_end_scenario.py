#!/usr/bin/env python3
"""
Test simulé de fin de scénario
Simule l'arrivée à la scène de victoire et vérifie que le jeu se termine
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from chasse_gobelins_refactored import ChasseGobelinsScenario

print("="*70)
print("🧪 TEST - Simulation de Fin de Scénario")
print("="*70)

# Créer le scénario
scenario = ChasseGobelinsScenario(pdf_path="", use_ncurses=False)
scenario.party = scenario.create_party()
scenario.build_custom_scenes()

print("\n📍 État initial:")
print(f"   Scène courante: {scenario.scene_manager.current_scene_id}")
print(f"   Nombre de scènes: {len(scenario.scene_manager.scenes)}")

# Définir la scène de victoire comme scène courante
scenario.scene_manager.set_start_scene('victory')
print(f"\n📍 Scène de départ définie: {scenario.scene_manager.current_scene_id}")

# Créer le contexte du jeu
game_context = {
    'party': scenario.party,
    'game_state': scenario.game_state,
    'renderer': scenario.renderer,
    'scenario': scenario,
    'monster_factory': scenario.monster_factory
}

print("\n🎬 Simulation d'exécution de la scène de victoire...")
print("(Appuyez sur ENTER quand demandé, tapez 'n' pour ne pas sauvegarder)\n")

# Simuler l'exécution de la scène
result = scenario.scene_manager.execute_scene('victory', game_context)

print(f"\n📍 Après exécution de la scène de victoire:")
print(f"   Résultat: {result}")
print(f"   Scène courante: {scenario.scene_manager.current_scene_id}")

if scenario.scene_manager.current_scene_id is None:
    print("\n✅ SUCCESS - La scène courante est None, le scénario va se terminer correctement")
else:
    print(f"\n❌ ERREUR - La scène courante devrait être None, mais est: {scenario.scene_manager.current_scene_id}")

print("\n" + "="*70)
print("Test terminé")
print("="*70)

