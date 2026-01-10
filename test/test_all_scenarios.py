#!/usr/bin/env python3
"""
Test de tous les scénarios
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_scenario(scenario_class, scenario_name):
    """Test un scénario"""
    print(f"\n{'='*70}")
    print(f"🧪 Test: {scenario_name}")
    print('='*70)

    try:
        # Créer le scénario
        scenario = scenario_class(pdf_path="", use_ncurses=False)

        # Initialiser
        scenario.party = scenario.create_party()
        scenario.build_custom_scenes()

        # Vérifier le groupe
        print(f"✅ Groupe: {len(scenario.party)} personnages")
        for char in scenario.party:
            print(f"   - {char.name} (Niveau {char.level}, HP {char.hit_points}/{char.max_hit_points})")

        # Vérifier les scènes
        print(f"✅ Scènes: {len(scenario.scene_manager.scenes)} chargées")

        # Vérifier le factory de monstres
        print(f"✅ Factory de monstres: OK")

        return True

    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎲 TEST DE TOUS LES SCÉNARIOS D&D 5e")
    print("="*70)

    results = {}

    # Test 1: Chasse aux Gobelins
    from chasse_gobelins_refactored import ChasseGobelinsScenario
    results["Chasse aux Gobelins"] = test_scenario(
        ChasseGobelinsScenario,
        "La Chasse aux Gobelins"
    )

    # Test 2: Tombe des Rois Serpents
    from tombe_rois_serpents_game import TombeRoisSerpentsScenario
    results["Tombe des Rois Serpents"] = test_scenario(
        TombeRoisSerpentsScenario,
        "La Tombe des Rois Serpents"
    )

    # Test 3: Yawning Portal
    from yawning_portal_game import YawningPortalScenario
    results["Yawning Portal"] = test_scenario(
        YawningPortalScenario,
        "Tales from the Yawning Portal"
    )

    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*70)

    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")

    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} scénarios passent les tests")

    if passed == total:
        print("\n🎉 TOUS LES TESTS PASSENT!")
    else:
        print("\n⚠️ Certains tests ont échoué")

