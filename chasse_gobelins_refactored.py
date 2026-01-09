"""
La Chasse aux Gobelins - Scénario D&D 5e Refactorisé
Version utilisant BaseScenario
"""

from typing import List
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_system import (
    NarrativeScene, ChoiceScene, CombatScene, RestScene, MerchantScene
)
from src.utils.exploration_map import ExplorationMap


class ChasseGobelinsScenario(BaseScenario):
    """
    La Chasse aux Gobelins - Aventure dans le Village de Brume
    """

    def __init__(self, pdf_path: str, use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)
        # 🆕 Initialiser la carte
        self.exploration_map = ExplorationMap("chasse_gobelins")

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
        """Construire les scènes de La Chasse aux Gobelins"""

        # INTRO
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
            next_scene_id="village_hub"
        ))

        # VILLAGE HUB - Scène intermédiaire pour update carte
        def village_hub_execute(ctx):
            # 🆕 Mettre à jour position sur carte
            self.update_map_location("village")

        # Wrapper class pour ajouter on_enter
        class VillageHubScene(NarrativeScene):
            def on_enter(scene_self, game_context: dict):
                super().on_enter(game_context)
                village_hub_execute(game_context)

        self.scene_manager.add_scene(VillageHubScene(
            scene_id="village_hub",
            title="🏘️ VILLAGE",
            text="Vous revenez au village.",
            next_scene_id="village_choice"
        ))

        self.scene_manager.add_scene(ChoiceScene(
            scene_id="village_choice",
            title="VILLAGE - PLACE CENTRALE",
            description="Vous êtes au village. Que faire?",
            choices=[
                {
                    'text': "Interroger les villageois",
                    'next_scene': "gather_info",
                    'effects': {'reputation': 1, 'npcs_met': 1}
                },
                {
                    'text': "Visiter le marchand",
                    'next_scene': "merchant_1"
                },
                {
                    'text': "Se reposer avant de partir",
                    'next_scene': "rest_1"
                },
                {
                    'text': "🗺️  Voir la carte",
                    'next_scene': "show_map_scene"
                },
                {
                    'text': "Partir vers la forêt",
                    'next_scene': "forest"
                }
            ]
        ))

        # GATHER INFO
        info_text = """Les villageois vous parlent des gobelins avec terreur.
        
"Ils viennent la nuit, emportent nos moutons!"
"J'ai vu leur chef - un gobelin énorme avec une grande hache!"
"Leur camp est dans la forêt, près de l'ancienne carrière."

Vous avez maintenant une meilleure idée de ce qui vous attend."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="gather_info",
            title="📝 ENQUÊTE",
            text=info_text,
            next_scene_id="village_choice"
        ))

        # MERCHANT
        self.scene_manager.add_scene(MerchantScene(
            scene_id="merchant_1",
            title="🛒 BOUTIQUE DU VILLAGE",
            merchant_id="village",
            next_scene_id="village_choice"
        ))

        # REST
        self.scene_manager.add_scene(RestScene(
            scene_id="rest_1",
            title="💤 REPOS",
            rest_type="short",
            next_scene_id="village_choice"
        ))

        # 🆕 CARTE
        class ShowMapScene(NarrativeScene):
            def on_enter(scene_self, game_context: dict):
                super().on_enter(game_context)
                self.show_map()
                game_context['renderer'].wait_for_input()

        self.scene_manager.add_scene(ShowMapScene(
            scene_id="show_map_scene",
            title="🗺️ CARTE",
            text="",
            next_scene_id="village_choice"
        ))

        # FOREST
        forest_text = """Vous entrez dans la forêt sombre.
        
Les arbres sont denses, la lumière peine à passer. Vous entendez 
des bruits suspects... des voix gutturales au loin.

Vous approchez du camp gobelin."""

        # Wrapper pour mettre à jour carte
        class ForestChoiceScene(ChoiceScene):
            def on_enter(scene_self, game_context: dict):
                super().on_enter(game_context)
                # 🆕 Mettre à jour carte
                self.update_map_location("forest_entrance")

        self.scene_manager.add_scene(ForestChoiceScene(
            scene_id="forest",
            title="🌲 FORÊT SOMBRE",
            description=forest_text,
            choices=[
                {
                    'text': "Avancer furtivement",
                    'next_scene': "goblin_camp",
                    'effects': {'locations_visited': 1}
                },
                {
                    'text': "Charger directement!",
                    'next_scene': "forest_ambush",
                    'effects': {}
                }
            ]
        ))

        # FOREST AMBUSH - 🆕 Utiliser MonsterFactory
        def create_ambush_goblins(ctx):
            return self.monster_factory.create_monsters([
                ("goblin", "Gobelin 1"),
                ("goblin", "Gobelin 2"),
                ("goblin", "Gobelin 3")
            ])

        self.scene_manager.add_scene(CombatScene(
            scene_id="forest_ambush",
            title="⚔️ EMBUSCADE!",
            description="Des gobelins surgissent!",
            enemies_factory=create_ambush_goblins,
            on_victory_scene="goblin_camp",
            on_defeat_scene="game_over"
        ))

        # GOBLIN CAMP
        camp_text = """Vous trouvez le camp des gobelins.
        
Des tentes sales, un feu de camp, et... des prisonniers!
Deux villageois sont attachés à un poteau.

Au fond du camp, vous voyez le chef gobelin - massif et menaçant."""

        class GoblinCampScene(NarrativeScene):
            def on_enter(scene_self, game_context: dict):
                super().on_enter(game_context)
                # 🆕 Mettre à jour carte
                self.update_map_location("goblin_camp")

        self.scene_manager.add_scene(GoblinCampScene(
            scene_id="goblin_camp",
            title="⛺ CAMP DES GOBELINS",
            text=camp_text,
            next_scene_id="boss_fight"
        ))

        # BOSS FIGHT - 🆕 Utiliser MonsterFactory
        def create_boss_encounter(ctx):
            return self.monster_factory.create_monsters(["goblin_boss"])

        self.scene_manager.add_scene(CombatScene(
            scene_id="boss_fight",
            title="👹 COMBAT FINAL - CHEF GOBELIN",
            description="Le chef gobelin rugit et charge!",
            enemies_factory=create_boss_encounter,
            on_victory_scene="victory",
            on_defeat_scene="game_over"
        ))

        # VICTORY
        victory_text = """Vous avez vaincu le chef gobelin!
        
Les autres gobelins fuient dans la forêt. Vous libérez les prisonniers,
qui vous remercient avec effusion.

De retour au village, les habitants vous acclament en héros!
Le maire vous remet une bourse remplie d'or.

Vous avez sauvé le Village de Brume!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="victory",
            title="🎉 VICTOIRE!",
            text=victory_text,
            next_scene_id=None
        ))



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

