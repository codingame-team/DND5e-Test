#!/usr/bin/env python3
"""
Launcher pour les scénarios D&D 5e
Permet de choisir et lancer n'importe quel scénario
"""

import sys


def main():
    print("=" * 70)
    print("  🎲 AVENTURES D&D 5e - SÉLECTION DE SCÉNARIO")
    print("=" * 70)

    print("\nScénarios disponibles:\n")
    print("  1. La Chasse aux Gobelins")
    print("     Niveau 3 | Durée: 1-2h | Difficulté: Facile")
    print("     Sauvez le Village de Brume des gobelins!")

    print("\n  2. Tales from the Yawning Portal - The Sunless Citadel")
    print("     Niveau 1 | Durée: 2-3h | Difficulté: Moyenne")
    print("     Explorez une citadelle engloutie et affrontez l'arbre maudit!")

    print("\n  3. La Tombe des Rois Serpents")
    print("     Niveau 2 | Durée: 2h | Difficulté: Moyenne")
    print("     Pillez une pyramide ancienne et affrontez le Roi Serpent momifié!")

    print("\n  4. L'Oeil de Gruumsh")
    print("     Niveau 3 | Durée: 2-3h | Difficulté: Moyenne")
    print("     Affrontez une tribu d'orques dans les Montagnes de Fer!")

    print("\n  5. La Secte du Crâne")
    print("     Niveau 4 | Durée: 2-3h | Difficulté: Difficile")
    print("     Infiltrez les catacombes et arrêtez un culte nécromantique!")

    print("\n  6. Le Collier de Zark")
    print("     Niveau 2 | Durée: 1-2h | Difficulté: Moyenne")
    print("     Enquête sur le vol d'un précieux collier d'émeraude!")

    print("\n  7. L'Auberge du Sanglier Gris")
    print("     Niveau 1 | Durée: 1-2h | Difficulté: Facile")
    print("     Une nuit mouvementée dans une auberge sur la route du Nord!")

    print("\n" + "=" * 70)

    while True:
        try:
            choice = input("\nChoisissez un scénario (1-7) ou 'q' pour quitter: ").strip()

            if choice.lower() == 'q':
                print("\nÀ bientôt, aventurier! 🎲")
                sys.exit(0)

            choice_num = int(choice)

            if choice_num == 1:
                print("\n🏰 Lancement de 'La Chasse aux Gobelins'...")
                from chasse_gobelins_refactored import ChasseGobelinsScenario
                scenario = ChasseGobelinsScenario(
                    pdf_path="scenarios/Chasse-aux-gobs.pdf",
                    use_ncurses=False
                )
                scenario.play()
                break

            elif choice_num == 2:
                print("\n🏰 Lancement de 'The Sunless Citadel'...")
                from yawning_portal_game import YawningPortalScenario
                scenario = YawningPortalScenario(
                    pdf_path="scenarios/Tales from the Yawning Portal.pdf",
                    use_ncurses=False
                )
                scenario.play()
                break

            elif choice_num == 3:
                print("\n🔺 Lancement de 'La Tombe des Rois Serpents'...")
                from tombe_rois_serpents_game import TombeRoisSerpentsScenario
                scenario = TombeRoisSerpentsScenario(
                    pdf_path="scenarios/Tombe-des-rois-serpents.pdf",
                    use_ncurses=False
                )
                scenario.play()
                break

            elif choice_num == 4:
                print("\n👁️ Lancement de 'L'Oeil de Gruumsh'...")
                from oeil_gruumsh_game import OeilDeGruumshScenario
                scenario = OeilDeGruumshScenario(
                    pdf_path="scenarios/Oeil-de-Gruumsh.pdf",
                    use_ncurses=False
                )
                scenario.play()
                break

            elif choice_num == 5:
                print("\n💀 Lancement de 'La Secte du Crâne'...")
                from secte_du_crane_game import SecteDuCraneScenario
                scenario = SecteDuCraneScenario(
                    pdf_path="scenarios/Secte-du-crane.pdf",
                    use_ncurses=False
                )
                scenario.play()
                break

            elif choice_num == 6:
                print("\n💎 Lancement de 'Le Collier de Zark'...")
                from collier_de_zark_game import CollierDeZarkScenario
                scenario = CollierDeZarkScenario(
                    pdf_path="scenarios/Collier-de-Zark.pdf",
                    use_ncurses=False
                )
                scenario.play()
                break

            elif choice_num == 7:
                print("\n🍺 Lancement de 'L'Auberge du Sanglier Gris'...")
                from auberge_sanglier_gris_game import AubergeSanglierGrisScenario
                scenario = AubergeSanglierGrisScenario(
                    pdf_path="scenarios/Auberge-du-sanglier-gris.pdf",
                    use_ncurses=False
                )
                scenario.play()
                break

            else:
                print("❌ Choix invalide. Veuillez entrer 1, 2, 3, 4, 5, 6, 7, ou 'q'")

        except ValueError:
            print("❌ Veuillez entrer un nombre valide")
        except KeyboardInterrupt:
            print("\n\nInterrompu par l'utilisateur. Au revoir! 👋")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()

