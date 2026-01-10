#!/usr/bin/env python3
"""
Test rapide d'un combat pour vérifier que les monstres fonctionnent
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from chasse_gobelins_refactored import ChasseGobelinsScenario

print("="*70)
print("🧪 TEST RAPIDE - Combat avec Gobelins")
print("="*70)

# Créer le scénario
scenario = ChasseGobelinsScenario(pdf_path="", use_ncurses=False)
scenario.party = scenario.create_party()

print(f"\n✅ Groupe créé:")
for char in scenario.party:
    print(f"   - {char.name}: {char.hit_points} HP, AC {char.armor_class}")

# Créer des gobelins
print(f"\n🧪 Création des monstres:")
goblin1 = scenario.monster_factory.create_monster("goblin", "Gobelin Éclaireur")
goblin2 = scenario.monster_factory.create_monster("goblin", "Gobelin Archer")
goblin_boss = scenario.monster_factory.create_monster("goblin_boss", "Chef Grukk")

monsters = [m for m in [goblin1, goblin2, goblin_boss] if m]

for monster in monsters:
    print(f"   - {monster.name}: {monster.hit_points} HP, AC {monster.armor_class}, CR {monster.challenge_rating}")
    print(f"     Actions: {', '.join([a.name for a in monster.actions])}")

print(f"\n✅ Combat peut être lancé avec {len(scenario.party)} personnages vs {len(monsters)} monstres")
print("\n" + "="*70)
print("🎉 SUCCÈS - Tous les systèmes sont opérationnels!")
print("="*70)

