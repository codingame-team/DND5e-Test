"""
La Tombe des Rois Serpents - Scénario D&D 5e
Aventure dans une pyramide oubliée
Version utilisant fichiers JSON
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class TombeRoisSerpentsScenario(BaseScenario):
    """
    La Tombe des Rois Serpents - Aventure dans une pyramide ancienne
    Utilise le fichier JSON data/scenes/tombe_rois_serpents.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "La Tombe des Rois Serpents"

    def create_party(self) -> List[Character]:
        """Créer un groupe d'explorateurs"""
        party = [
            self.create_basic_fighter("Ankhar le Fort", level=2),
            self.create_basic_cleric("Neith la Sage", level=2),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        # Charger le scénario depuis JSON
        json_path = Path("data/scenes/tombe_rois_serpents.json")

        if not json_path.exists():
            print(f"⚠️  Fichier JSON non trouvé: {json_path}")
            print("Utilisation du scénario par défaut...")
            self._build_default_scenes()
            return

        # Charger les scènes depuis JSON avec SceneFactory
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            scenario_data = json.load(f)

        # Créer les scènes depuis le JSON
        for scene_data in scenario_data.get('scenes', []):
            scene = SceneFactory.create_scene_from_dict(scene_data, self.monster_factory)
            if scene:
                self.scene_manager.add_scene(scene)

        print(f"✅ Scénario chargé depuis JSON: {len(self.scene_manager.scenes)} scènes")

    def _build_default_scenes(self):
        """Scènes par défaut si le JSON n'est pas trouvé"""
        from src.scenes.scene_system import NarrativeScene

        # Scène d'intro minimale
        intro_text = """Le soleil brûlant du désert frappe impitoyablement alors que vous 
approchez de l'ancienne pyramide.

Des légendes parlent des Rois Serpents qui régnaient autrefois sur ces terres,
enterrés avec d'incroyables trésors... et de terribles malédictions.

L'entrée de la pyramide s'ouvre devant vous comme une gueule béante.
Des hiéroglyphes serpentins ornent les murs."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🏜️ LA PYRAMIDE MAUDITE",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario La Tombe des Rois Serpents"""
    import argparse

    parser = argparse.ArgumentParser(description="La Tombe des Rois Serpents")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = TombeRoisSerpentsScenario(
        pdf_path="scenarios/Tombe-des-rois-serpents.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()
