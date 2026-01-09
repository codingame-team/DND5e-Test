"""
La Chasse aux Gobelins - Scénario D&D 5e Refactorisé
Version utilisant BaseScenario et fichiers JSON
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class ChasseGobelinsScenario(BaseScenario):
    """
    La Chasse aux Gobelins - Aventure dans le Village de Brume
    Utilise le fichier JSON data/scenes/chasse_gobelins.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "La Chasse aux Gobelins"

    def create_party(self) -> List[Character]:
        """Créer le groupe de héros du village"""
        party = [
            self.create_basic_fighter("Grok", level=3),
            self.create_basic_cleric("Sœur Elara", level=3),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        # Charger le scénario depuis JSON
        json_path = Path("data/scenes/chasse_gobelins.json")

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
        intro_text = """Le Village de Brume est en émoi. Des gobelins terrorisent 
la population, volant du bétail et effrayant les voyageurs.

Le maire vous a convoqués. "Nous avons besoin de héros! Les gobelins ont 
établi un camp dans la forêt sombre au nord. Débarrassez-nous d'eux, 
et vous serez grassement récompensés!"

Votre aventure commence..."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🏰 VILLAGE DE BRUME",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")



def main():
    """Lancer le scénario La Chasse aux Gobelins"""
    import argparse

    parser = argparse.ArgumentParser(description="La Chasse aux Gobelins")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = ChasseGobelinsScenario(
        pdf_path="scenarios/Chasse-aux-gobs.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

