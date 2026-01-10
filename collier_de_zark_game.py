#!/usr/bin/env python3
"""
Le Collier de Zark - Scénario D&D 5e
Enquête et vol : retrouvez le précieux Collier d'Émeraude
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class CollierDeZarkScenario(BaseScenario):
    """
    Le Collier de Zark - Enquête sur un vol de bijou
    Utilise le fichier JSON data/scenes/collier_de_zark.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "Le Collier de Zark"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Rendal", level=2),
            self.create_basic_cleric("Mira", level=2),
            self.create_basic_fighter("Varick", level=2),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        json_path = Path("data/scenes/collier_de_zark.json")

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

        intro_text = """La prospère ville de Zark est en émoi. Le célèbre Collier d'Émeraude, 
trésor de la famille noble des Ashford, a été dérobé!

Lady Ashford vous a convoqués au manoir. Trouvez le voleur et récupérez le collier!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="💎 LA VILLE DE ZARK",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario Le Collier de Zark"""
    import argparse

    parser = argparse.ArgumentParser(description="Le Collier de Zark")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = CollierDeZarkScenario(
        pdf_path="scenarios/Collier-de-Zark.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

