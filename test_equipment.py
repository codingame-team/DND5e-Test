#!/usr/bin/env python3
"""
Script de validation des équipements pour tous les scénarios
Teste que les équipements se chargent correctement
"""

import sys
from pathlib import Path

# Scénarios à tester
SCENARIOS_TO_TEST = [
    ("masque_utruz_enrichi_game", "MasqueUtruzEnrichiScenario", "Le Masque Utruz (Enrichi)"),
    ("cryptes_de_kelemvor_manual_game", "CryptesDeKelemvorManualScenario", "Les Cryptes de Kelemvor (Manuel)"),
    ("chasse_gobelins_refactored", "ChasseGobelinsScenario", "La Chasse aux Gobelins"),
]


def test_equipment_loading(module_name, class_name, display_name):
    """Tester le chargement des équipements pour un scénario"""
    try:
        module = __import__(module_name)
        ScenarioClass = getattr(module, class_name)

        scenario = ScenarioClass()

        # Tester le chargement
        weapons, armors, equipments, potions = scenario._load_equipment()

        # Vérifier les résultats
        success = (
            len(weapons) == 20 and
            len(armors) == 15 and
            len(equipments) == 20 and
            len(potions) == 2
        )

        if success:
            print(f"✅ {display_name}")
            print(f"   Armes: {len(weapons)}, Armures: {len(armors)}, Équipements: {len(equipments)}, Potions: {len(potions)}")
            return True
        else:
            print(f"❌ {display_name}")
            print(f"   Attendu: 20 armes, 15 armures, 20 équipements, 2 potions")
            print(f"   Obtenu: {len(weapons)} armes, {len(armors)} armures, {len(equipments)} équipements, {len(potions)} potions")
            return False

    except Exception as e:
        print(f"❌ {display_name} - ERREUR: {e}")
        return False


def main():
    print("=" * 80)
    print("🧪 VALIDATION DU CHARGEMENT DES ÉQUIPEMENTS")
    print("=" * 80)
    print()

    results = []

    for module_name, class_name, display_name in SCENARIOS_TO_TEST:
        result = test_equipment_loading(module_name, class_name, display_name)
        results.append((display_name, result))
        print()

    # Résumé
    print("=" * 80)
    print("📊 RÉSUMÉ")
    print("=" * 80)

    success_count = sum(1 for _, result in results if result)
    total_count = len(results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print()
    print(f"Résultat: {success_count}/{total_count} scénarios validés")

    if success_count == total_count:
        print("\n🎉 TOUS LES SCÉNARIOS CHARGENT CORRECTEMENT LES ÉQUIPEMENTS!")
        return 0
    else:
        print("\n⚠️  Certains scénarios ont des problèmes de chargement")
        return 1


if __name__ == "__main__":
    sys.exit(main())

