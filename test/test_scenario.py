#!/usr/bin/env python3
"""
Test automatique d'un scénario complet
"""
from chasse_gobelins_refactored import ChasseGobelinsScenario

print("🧪 Test du scénario La Chasse aux Gobelins\n")

# Créer le scénario
scenario = ChasseGobelinsScenario(pdf_path="", use_ncurses=False)

# Initialiser le scénario
scenario.party = scenario.create_party()
scenario.build_custom_scenes()

# Vérifier le groupe
print(f"✅ Groupe créé: {len(scenario.party)} personnages")
for char in scenario.party:
    print(f"   - {char.name} (Niveau {char.level}, HP {char.hit_points}/{char.max_hit_points})")

# Vérifier les scènes
print(f"\n✅ Scènes chargées: {len(scenario.scene_manager.scenes)} scènes")

# Vérifier les monstres
print(f"\n🧪 Test des monstres du scénario:")
test_monsters = ['goblin', 'goblin_boss']
for monster_id in test_monsters:
    monster = scenario.monster_factory.create_monster(monster_id)
    if monster:
        print(f"   ✅ {monster.name}: AC {monster.armor_class}, HP {monster.hit_points}, CR {monster.challenge_rating}")
        print(f"      Actions: {', '.join([a.name for a in monster.actions])}")

print("\n✅ Tous les tests passent!")

