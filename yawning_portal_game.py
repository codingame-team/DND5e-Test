"""
Tales from the Yawning Portal - Scénario D&D 5e
Aventure classique dans la taverne légendaire
Version utilisant fichiers JSON
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class YawningPortalScenario(BaseScenario):
    """
    The Sunless Citadel - Premier donjon de Tales from the Yawning Portal
    Utilise le fichier JSON data/scenes/sunless_citadel.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "Tales from the Yawning Portal - The Sunless Citadel"

    def create_party(self) -> List[Character]:
        """Créer un groupe d'aventuriers pour la citadelle"""
        party = [
            self.create_basic_fighter("Tordek", level=1),
            self.create_basic_cleric("Jozan", level=1),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        # Charger le scénario depuis JSON
        json_path = Path("data/scenes/sunless_citadel.json")

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
        intro_text = """Vous vous tenez devant l'entrée de la Citadelle Sans Soleil, 
une forteresse engloutie qui a sombré dans la terre il y a des siècles.

Les villageois d'Oakhurst parlent d'aventuriers disparus, de gobelins malveillants,
et d'un arbre maudit qui produit des fruits magiques...

L'air est froid et humide. L'entrée béante semble vous appeler."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🏰 LA CITADELLE SANS SOLEIL",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario The Sunless Citadel"""
    import argparse

    parser = argparse.ArgumentParser(description="Tales from the Yawning Portal - The Sunless Citadel")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = YawningPortalScenario(
        pdf_path="scenarios/Tales from the Yawning Portal.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

