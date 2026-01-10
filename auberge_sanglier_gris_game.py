#!/usr/bin/env python3
"""
L'Auberge du Sanglier Gris - Scénario D&D 5e
Une nuit mouvementée dans une auberge sur la route du Nord
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class AubergeSanglierGrisScenario(BaseScenario):
    """
    L'Auberge du Sanglier Gris - Intrigue et action dans une auberge
    Utilise le fichier JSON data/scenes/auberge_sanglier_gris.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "L'Auberge du Sanglier Gris"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Bran", level=1),
            self.create_basic_cleric("Lyssa", level=1),
            self.create_basic_fighter("Torgrim", level=1),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        json_path = Path("data/scenes/auberge_sanglier_gris.json")

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

        print(f"✅ Scénario chargé depuis JSON: {len(self.scene_manager.scenes)} scènes")

    def _build_default_scenes(self):
        """Scènes par défaut si le JSON n'est pas trouvé"""
        from src.scenes.scene_system import NarrativeScene

        intro_text = """Une nuit d'orage, vous trouvez refuge dans l'Auberge du Sanglier Gris, 
sur la route du Nord.

L'aubergiste vous accueille chaleureusement. Mais cette nuit sera plus mouvementée 
que prévu..."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🍺 L'AUBERGE DU SANGLIER GRIS",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario L'Auberge du Sanglier Gris"""
    import argparse

    parser = argparse.ArgumentParser(description="L'Auberge du Sanglier Gris")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = AubergeSanglierGrisScenario(
        pdf_path="scenarios/Auberge-du-sanglier-gris.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

