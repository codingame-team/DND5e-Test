"""
La Tombe des Rois Serpents - Scénario D&D 5e
Aventure dans une pyramide oubliée
"""

from typing import List, Dict
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_system import (
    NarrativeScene, ChoiceScene, CombatScene, RestScene
)
from src.utils.exploration_map import ExplorationMap


class TombeRoisSerpentsScenario(BaseScenario):
    """
    La Tombe des Rois Serpents - Aventure dans une pyramide ancienne
    """

    def __init__(self, pdf_path: str, use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)
        # 🆕 Initialiser la carte
        self.exploration_map = ExplorationMap("tombe_rois_serpents")

    def get_scenario_name(self) -> str:
        return "La Tombe des Rois Serpents"

    def create_party(self) -> List[Character]:
        """Créer un groupe d'explorateurs"""
        party = [
            self.create_basic_fighter("Ankhar le Fort", level=2),
            self.create_basic_cleric("Neith la Sage", level=2),
        ]

        # Ajouter un magicien
        from dnd_5e_core import Abilities
        from dnd_5e_core.races import Race
        from dnd_5e_core.classes import ClassType
        from dnd_5e_core.abilities import AbilityType
        from src.core.adapters import CharacterExtensions

        race = Race(
            index='elf', name='Elfe', speed=30, ability_bonuses={},
            alignment='Any', age='110', size='Medium', size_description='5-6 ft',
            starting_proficiencies=[], starting_proficiency_options=[],
            languages=[], language_desc='Common, Elvish', traits=[], subraces=[]
        )

        wizard_class = ClassType(
            index='wizard', name='Wizard', hit_die=6, proficiency_choices=[],
            proficiencies=[], saving_throws=[AbilityType.INT, AbilityType.WIS],
            starting_equipment=[], starting_equipment_options=[], class_levels=[],
            multi_classing=[], subclasses=[], spellcasting_level=2,
            spellcasting_ability='int', can_cast=True, spell_slots={},
            spells_known=[], cantrips_known=[]
        )

        wizard = Character(
            name="Zephyr l'Érudit", race=race, subrace=None, ethnic='High Elf', gender='Male',
            height='5ft10', weight='140 lbs', age=110,
            class_type=wizard_class, proficiencies=[],
            abilities=Abilities(str=8, dex=14, con=12, int=17, wis=13, cha=10),
            ability_modifiers=Abilities(str=8, dex=14, con=12, int=17, wis=13, cha=10),
            hit_points=11, max_hit_points=11,
            speed=30, haste_timer=0.0, hasted=False,
            xp=300, level=2,
            inventory=[], gold=40, sc=None, conditions=[]
        )

        CharacterExtensions.add_inventory_management(wizard)
        CharacterExtensions.init_spell_slots(wizard)
        party.append(wizard)

        return party

    def build_custom_scenes(self):
        """Construire les scènes de la Tombe des Rois Serpents"""

        # INTRO
        intro_text = """Le soleil brûlant du désert frappe impitoyablement alors que vous 
approchez de l'ancienne pyramide.

Des légendes parlent des Rois Serpents qui régnaient autrefois sur ces terres,
enterrés avec d'incroyables trésors... et de terribles malédictions.

L'entrée de la pyramide s'ouvre devant vous comme une gueule béante.
Des hiéroglyphes serpentins ornent les murs."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🔺 LA TOMBE DES ROIS SERPENTS",
            text=intro_text,
            next_scene_id="pyramid_entrance"
        ))

        # PYRAMID ENTRANCE
        entrance_text = """Vous vous tenez à l'entrée de la pyramide.
        
Des torches éternelles brûlent d'une flamme verdâtre, projetant des ombres dansantes.
L'air sent le renfermé et quelque chose de plus sinistre... du venin.

Deux passages s'ouvrent devant vous."""

        self.scene_manager.add_scene(ChoiceScene(
            scene_id="pyramid_entrance",
            title="🚪 ENTRÉE DE LA PYRAMIDE",
            description=entrance_text,
            choices=[
                {
                    'text': "Emprunter le passage de gauche (Chambre des Offrandes)",
                    'next_scene': "offering_chamber",
                    'effects': {'locations_visited': 1}
                },
                {
                    'text': "Emprunter le passage de droite (Salle des Gardiens)",
                    'next_scene': "guardian_hall",
                    'effects': {'locations_visited': 1}
                },
                {
                    'text': "Examiner les hiéroglyphes à l'entrée",
                    'next_scene': "hieroglyph_study",
                    'effects': {}
                }
            ]
        ))

        # HIEROGLYPH STUDY
        hieroglyph_text = """Vous étudiez attentivement les hiéroglyphes.
        
Ils racontent l'histoire du Roi Serpent Sesshathep, qui fut enterré vivant
avec ses serviteurs les plus fidèles... des hommes-serpents.

"Que celui qui entre respecte les offrandes, ou qu'il périsse par le venin."
        
Cette connaissance pourrait vous sauver la vie."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="hieroglyph_study",
            title="📜 ÉTUDE DES HIÉROGLYPHES",
            text=hieroglyph_text,
            next_scene_id="pyramid_entrance"
        ))

        # OFFERING CHAMBER
        offering_text = """La Chambre des Offrandes est remplie de vases, de statues,
et d'objets précieux.

Au centre, un autel avec une statue de serpent doré. Ses yeux sont des rubis.
        
Des squelettes d'aventuriers imprudents jonchent le sol."""

        self.scene_manager.add_scene(ChoiceScene(
            scene_id="offering_chamber",
            title="🏺 CHAMBRE DES OFFRANDES",
            description=offering_text,
            choices=[
                {
                    'text': "Faire une offrande à la statue (déposer de l'or)",
                    'next_scene': "make_offering",
                    'effects': {},
                    'condition': lambda ctx: ctx['party'][0].gold >= 10
                },
                {
                    'text': "Voler les rubis de la statue",
                    'next_scene': "steal_rubies",
                    'effects': {}
                },
                {
                    'text': "Quitter la chambre prudemment",
                    'next_scene': "guardian_hall",
                    'effects': {}
                }
            ]
        ))

        # MAKE OFFERING
        offering_made_text = """Vous déposez respectueusement 10 pièces d'or sur l'autel.
        
La statue de serpent s'illumine brièvement. Un passage secret s'ouvre dans le mur!
        
Vous avez gagné la faveur des Rois Serpents."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="make_offering",
            title="✨ OFFRANDE ACCEPTÉE",
            text=offering_made_text,
            next_scene_id="secret_passage"
        ))

        # STEAL RUBIES - Piège!
        def trigger_poison_trap(ctx):
            return self.monster_factory.create_monsters(["poison_snake"])

        self.scene_manager.add_scene(CombatScene(
            scene_id="steal_rubies",
            title="💀 PIÈGE MORTEL!",
            description="Du gaz toxique s'échappe! Des serpents venimeux attaquent!",
            enemies_factory=trigger_poison_trap,
            on_victory_scene="guardian_hall",
            on_defeat_scene="game_over"
        ))

        # GUARDIAN HALL
        hall_text = """Vous entrez dans la Salle des Gardiens.
        
D'immenses statues de guerriers serpents bordent les murs.
Leurs yeux semblent vous suivre...

Au fond de la salle, une porte ornée de serpents entrelacés."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="guardian_hall",
            title="🗿 SALLE DES GARDIENS",
            text=hall_text,
            next_scene_id="guardian_fight"
        ))

        # GUARDIAN FIGHT
        def create_guardians(ctx):
            return self.monster_factory.create_monsters([
                ("snake_guardian", "Gardien 1"),
                ("snake_guardian", "Gardien 2")
            ])

        self.scene_manager.add_scene(CombatScene(
            scene_id="guardian_fight",
            title="⚔️ LES GARDIENS S'ÉVEILLENT!",
            description="Les statues s'animent! Des hommes-serpents squelettiques vous attaquent!",
            enemies_factory=create_guardians,
            on_victory_scene="throne_room_approach",
            on_defeat_scene="game_over"
        ))

        # SECRET PASSAGE (si offrande faite)
        secret_text = """Le passage secret vous mène directement à une antichambre
près de la Salle du Trône, évitant les gardiens!

Vous trouvez également un coffre contenant des potions et de l'équipement."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="secret_passage",
            title="🗝️ PASSAGE SECRET",
            text=secret_text,
            next_scene_id="rest_before_king"
        ))

        # REST BEFORE KING
        self.scene_manager.add_scene(RestScene(
            scene_id="rest_before_king",
            title="💤 REPOS AVANT LE ROI",
            rest_type="short",
            next_scene_id="throne_room_approach"
        ))

        # THRONE ROOM APPROACH
        approach_text = """Vous arrivez devant la porte de la Salle du Trône.
        
Des serpents vivants glissent sur le sol. L'air est épais et chargé de magie ancienne.
        
Derrière cette porte se trouve le Roi Serpent Sesshathep.
Êtes-vous prêts?"""

        self.scene_manager.add_scene(ChoiceScene(
            scene_id="throne_room_approach",
            title="👑 PORTE DE LA SALLE DU TRÔNE",
            description=approach_text,
            choices=[
                {
                    'text': "Ouvrir la porte et affronter le Roi Serpent",
                    'next_scene': "final_boss",
                    'effects': {}
                },
                {
                    'text': "Se préparer d'abord (repos court)",
                    'next_scene': "rest_final",
                    'effects': {}
                },
                {
                    'text': "Tenter de parlementer",
                    'next_scene': "parley_attempt",
                    'effects': {}
                }
            ]
        ))

        # REST FINAL
        self.scene_manager.add_scene(RestScene(
            scene_id="rest_final",
            title="💤 DERNIERS PRÉPARATIFS",
            rest_type="short",
            next_scene_id="final_boss"
        ))

        # PARLEY ATTEMPT
        parley_text = """Vous tentez de parlementer avec le Roi Serpent...
        
Mais il n'écoute pas! "Profanateurs! Vous paierez de votre vie!"
        
Le combat est inévitable!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="parley_attempt",
            title="🗣️ TENTATIVE DE PARLEY",
            text=parley_text,
            next_scene_id="final_boss"
        ))

        # FINAL BOSS
        def create_snake_king(ctx):
            return self.monster_factory.create_monsters(["snake_king"])

        self.scene_manager.add_scene(CombatScene(
            scene_id="final_boss",
            title="👑🐍 LE ROI SERPENT SESSHATHEP",
            description="Le Roi Serpent momifié se lève de son trône! Ses yeux brillent d'un feu vert!",
            enemies_factory=create_snake_king,
            on_victory_scene="victory",
            on_defeat_scene="game_over"
        ))

        # VICTORY
        victory_text = """Le Roi Serpent s'effondre dans un nuage de poussière millénaire!
        
La malédiction de la pyramide est brisée. Les trésors de la chambre funéraire
s'offrent à vous: or, gemmes, et artefacts anciens.

Mais plus important encore, vous avez mis fin au règne de terreur de Sesshathep.
Les villages du désert pourront enfin vivre en paix!

La pyramide commence à trembler. Il est temps de partir avant qu'elle ne s'effondre!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="victory",
            title="🏆 LA TOMBE EST CONQUISE!",
            text=victory_text,
            next_scene_id=None
        ))

    def _init_game_state(self) -> Dict:
        """État du jeu spécifique à ce scénario"""
        state = super()._init_game_state()
        state['offering_made'] = False
        state['secret_passage_found'] = False
        state['curse_active'] = True
        return state



def main():
    """Lancer le scénario Tombe des Rois Serpents"""
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

