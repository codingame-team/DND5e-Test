#!/usr/bin/env python3
"""
Test rapide du système de monstres
"""
from src.scenarios.base_scenario import BaseScenario
from dnd_5e_core import Character


class TestScenario(BaseScenario):
    def get_scenario_name(self) -> str:
        return "Test Monsters"

    def create_party(self):
        return []

    def build_custom_scenes(self):
        pass


# Test
scenario = TestScenario("", False)
print("\n🧪 Test de chargement des monstres:\n")

# Test monstres locaux
for monster_id in ['goblin', 'goblin_boss', 'snake_guardian', 'snake_king']:
    monster = scenario.monster_factory.create_monster(monster_id)
    if monster:
        print(f"✅ {monster_id}: {monster.name} (AC {monster.armor_class}, HP {monster.hit_points}, CR {monster.challenge_rating})")
    else:
        print(f"❌ {monster_id}: Non trouvé")

print("\n🧪 Test de chargement des potions:\n")
try:
    weapons, armors, equipments, potions = scenario._load_equipment()
    print(f"✅ Potions: {len(potions)} chargées")
    for potion in potions:
        print(f"   - {potion.name} ({potion.rarity.name})")
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

