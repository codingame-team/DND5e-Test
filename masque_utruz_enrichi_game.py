#!/usr/bin/env python3
"""
Le Masque Utruz - VERSION ENRICHIE - Scénario D&D 5e
Basé sur le contenu réel du PDF du scénario officiel
Enquête urbaine, usurier, halfelin prisonnier, et le mystérieux trésor des Utruz
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class MasqueUtruzEnrichiScenario(BaseScenario):
    """
    Le Masque Utruz - Version Enrichie
    Utilise le fichier JSON data/scenes/masque_utruz_enrichi.json
    Basé sur l'extraction du PDF officiel
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "Le Masque Utruz (Version Enrichie)"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Kael", level=3),
            self.create_basic_cleric("Seren", level=3),
            self.create_basic_fighter("Dorn", level=3),
            self.create_basic_cleric("Mira", level=3),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON enrichi"""
        json_path = Path("data/scenes/masque_utruz_enrichi.json")

        if not json_path.exists():
            print(f"⚠️  Fichier JSON non trouvé: {json_path}")
            print("Utilisation du scénario par défaut...")
            self._build_default_scenes()
            return

        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            scenario_data = json.load(f)

        for scene_data in scenario_data.get('scenes', []):
            scene = SceneFactory.create_scene_from_dict(scene_data, self.monster_factory)
            if scene:
                self.scene_manager.add_scene(scene)

        print(f"✅ Scénario enrichi chargé depuis JSON: {len(self.scene_manager.scenes)} scènes")
        print(f"📖 Basé sur l'extraction du PDF officiel")

    def _build_default_scenes(self):
        """Scènes par défaut si le JSON n'est pas trouvé"""
        from src.scenes.scene_system import NarrativeScene

        intro_text = """Vous êtes des aventuriers dans l'immense cité grouillante de mercenaires.

Après bien des recherches, vous entrez au service d'un usurier: Maître Grassepath, 
propriétaire du Boulier Bleu - une maison au bord de la faille.

Votre mission: retrouver un halfelin rouquin emprisonné..."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🏙️ LA CITÉ SUR LA FAILLE",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario Le Masque Utruz (Version Enrichie)"""
    import argparse

    parser = argparse.ArgumentParser(description="Le Masque Utruz - Version Enrichie")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    print("=" * 70)
    print("🎭 LE MASQUE UTRUZ - VERSION ENRICHIE")
    print("=" * 70)
    print("📖 Basé sur le contenu du PDF officiel")
    print("📝 39 scènes enrichies avec détails du scénario original")
    print("🏙️ Cité sur la faille, usurier, Utruz, et Dieu-Poisson")
    print("=" * 70)
    print()

    scenario = MasqueUtruzEnrichiScenario(
        pdf_path="scenarios/Masque-utruz.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

