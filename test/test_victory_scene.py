#!/usr/bin/env python3
"""
Test de la scène de victoire - vérifie que le scénario se termine correctement
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from chasse_gobelins_refactored import ChasseGobelinsScenario

print("="*70)
print("🧪 TEST - Scène de Victoire")
print("="*70)

# Créer le scénario
scenario = ChasseGobelinsScenario(pdf_path="", use_ncurses=False)
scenario.party = scenario.create_party()
scenario.build_custom_scenes()

# Vérifier que la scène de victoire existe
victory_scene = scenario.scene_manager.scenes.get('victory')
if victory_scene:
    print(f"\n✅ Scène de victoire trouvée: {victory_scene.title}")
    print(f"   next_scene_id: {victory_scene.next_scene_id}")

    if victory_scene.next_scene_id is None:
        print("   ✅ La scène de victoire a next_scene_id = None (correct)")
    else:
        print(f"   ❌ ERREUR: next_scene_id = {victory_scene.next_scene_id} (devrait être None)")
else:
    print("❌ Scène de victoire non trouvée!")

print("\n" + "="*70)
print("Test terminé")
print("="*70)

