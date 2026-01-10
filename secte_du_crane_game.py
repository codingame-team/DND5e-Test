#!/usr/bin/env python3
"""
La Secte du Crâne - Scénario D&D 5e
Un groupe d'aventuriers doit infiltrer les catacombes et arrêter un culte nécromantique
"""

from src.populate_rpg_functions import populate_party
from src.play_scenario_from_json import JSONScenario


class SecteDuCraneScenario(JSONScenario):
    """Scénario: La Secte du Crâne"""

    def __init__(self):
        super().__init__(
            json_file="data/scenes/secte_du_crane.json",
            monsters_file="data/monsters/all_monsters.json"
        )

    def build_custom_party(self):
        """Crée le groupe d'aventuriers pour ce scénario"""
        print("\n" + "=" * 70)
        print("  💀 LA SECTE DU CRÂNE")
        print("=" * 70)
        print("\nCréation de votre groupe d'aventuriers...")
        print("Niveau recommandé: 4")
        print("Taille du groupe: 4 personnages")
        print()

        # Créer un groupe de 4 aventuriers de niveau 4
        party = populate_party(
            nb_characters=4,
            level=4,
            names=["Aldric", "Seraphine", "Gareth", "Elara"],
            classes=["paladin", "cleric", "rogue", "wizard"]
        )

        print("\n🗡️  Votre groupe:")
        for character in party:
            print(f"  - {character.name} ({character.char_class.capitalize()}) - Niveau {character.level}: {character.hit_points}/{character.hit_points} HP")

        return party


def main():
    """Point d'entrée principal"""
    scenario = SecteDuCraneScenario()
    party = scenario.build_custom_party()
    scenario.run(party)


if __name__ == "__main__":
    main()

