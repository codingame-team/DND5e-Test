"""
Tales from the Yawning Portal - Scénario D&D 5e
Aventure classique dans la taverne légendaire
"""

from typing import List
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_system import (
    NarrativeScene, ChoiceScene, CombatScene, RestScene
)
from dnd_5e_core.combat import Action, ActionType, Damage
from dnd_5e_core.mechanics import DamageDice
from dnd_5e_core.equipment import DamageType
from dnd_5e_core import Monster, Abilities


class YawningPortalScenario(BaseScenario):
    """
    The Sunless Citadel - Premier donjon de Tales from the Yawning Portal
    """

    def get_scenario_name(self) -> str:
        return "Tales from the Yawning Portal - The Sunless Citadel"

    def create_party(self) -> List[Character]:
        """Créer un groupe d'aventuriers pour la citadelle"""
        party = [
            self.create_basic_fighter("Tordek", level=1),
            self.create_basic_cleric("Jozan", level=1),
        ]

        # Ajouter un roublard (simplifié comme fighter avec DEX)
        from dnd_5e_core import Abilities
        from dnd_5e_core.races import Race
        from dnd_5e_core.classes import ClassType
        from dnd_5e_core.abilities import AbilityType
        from src.core.adapters import CharacterExtensions

        race = Race(
            index='halfling', name='Halfling', speed=25, ability_bonuses={},
            alignment='Any', age='Adult', size='Small', size_description='3 ft',
            starting_proficiencies=[], starting_proficiency_options=[],
            languages=[], language_desc='Common, Halfling', traits=[], subraces=[]
        )

        rogue_class = ClassType(
            index='rogue', name='Rogue', hit_die=8, proficiency_choices=[],
            proficiencies=[], saving_throws=[AbilityType.DEX, AbilityType.INT],
            starting_equipment=[], starting_equipment_options=[], class_levels=[],
            multi_classing=[], subclasses=[], spellcasting_level=0,
            spellcasting_ability=None, can_cast=False, spell_slots={},
            spells_known=[], cantrips_known=[]
        )

        rogue = Character(
            name="Lidda", race=race, subrace=None, ethnic='Lightfoot', gender='Female',
            height='3ft', weight='40 lbs', age=25,
            class_type=rogue_class, proficiencies=[],
            abilities=Abilities(str=10, dex=17, con=12, int=14, wis=13, cha=12),
            ability_modifiers=Abilities(str=10, dex=17, con=12, int=14, wis=13, cha=12),
            hit_points=9, max_hit_points=9,
            speed=25, haste_timer=0.0, hasted=False,
            xp=0, level=1,
            inventory=[], gold=75, sc=None, conditions=[]
        )

        CharacterExtensions.add_inventory_management(rogue)
        party.append(rogue)

        return party

    def build_custom_scenes(self):
        """Construire les scènes de The Sunless Citadel"""

        # INTRO
        intro_text = """Vous vous tenez devant l'entrée de la Citadelle Sans Soleil, 
une forteresse engloutie qui a sombré dans la terre il y a des siècles.

Les villageois d'Oakhurst parlent d'aventuriers disparus, de gobelins malveillants,
et d'un arbre maudit qui produit des fruits magiques...

L'air est froid et humide. L'entrée béante semble vous appeler."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🏰 LA CITADELLE SANS SOLEIL",
            text=intro_text,
            next_scene_id="entrance"
        ))

        # ENTRANCE - Choix d'approche
        self.scene_manager.add_scene(ChoiceScene(
            scene_id="entrance",
            title="🚪 ENTRÉE DE LA CITADELLE",
            description="Comment voulez-vous entrer?",
            choices=[
                {
                    'text': "Descendre prudemment par l'ancien escalier",
                    'next_scene': "main_hall",
                    'effects': {}
                },
                {
                    'text': "Chercher une entrée alternative",
                    'next_scene': "side_entrance",
                    'effects': {'exploration': 1}
                },
                {
                    'text': "Se reposer avant d'entrer",
                    'next_scene': "rest_entrance"
                }
            ]
        ))

        # REST AT ENTRANCE
        self.scene_manager.add_scene(RestScene(
            scene_id="rest_entrance",
            title="💤 CAMPEMENT À L'ENTRÉE",
            rest_type="short",
            next_scene_id="entrance"
        ))

        # SIDE ENTRANCE
        side_text = """Vous contournez les ruines et découvrez une fissure dans la pierre.
        
En vous faufilant à travers, vous évitez les pièges de l'entrée principale,
mais vous entendez des voix gutturales... des gobelins!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="side_entrance",
            title="🗿 ENTRÉE LATÉRALE",
            text=side_text,
            next_scene_id="goblin_guards"
        ))

        # MAIN HALL
        hall_text = """Le grand hall est en ruine. Des colonnes brisées jonchent le sol.
        
Sur les murs, d'anciennes fresques dépeignent une citadelle glorieuse,
maintenant tombée dans l'oubli.

Deux passages s'ouvrent devant vous: l'un vers l'ouest, l'autre vers l'est."""

        self.scene_manager.add_scene(ChoiceScene(
            scene_id="main_hall",
            title="🏛️ GRAND HALL",
            description=hall_text,
            choices=[
                {
                    'text': "Explorer le passage ouest (quartiers gobelins)",
                    'next_scene': "goblin_guards",
                    'effects': {'locations_visited': 1}
                },
                {
                    'text': "Explorer le passage est (jardins souterrains)",
                    'next_scene': "underground_gardens",
                    'effects': {'locations_visited': 1}
                },
                {
                    'text': "Examiner les fresques plus attentivement",
                    'next_scene': "fresco_discovery",
                    'effects': {}
                }
            ]
        ))

        # FRESCO DISCOVERY
        fresco_text = """En examinant les fresques, vous découvrez des indices sur l'histoire 
de la citadelle. Elle appartenait à un ordre de druides qui vénérait un arbre sacré.
        
Mais l'arbre fut corrompu par un mal ancien... le Gulthias Tree.
        
Cette information pourrait être cruciale."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="fresco_discovery",
            title="📜 DÉCOUVERTE HISTORIQUE",
            text=fresco_text,
            next_scene_id="main_hall"
        ))

        # GOBLIN GUARDS - Combat
        def create_goblins(ctx):
            goblins = []
            for i in range(3):
                goblin = self._create_goblin(f"Gobelin {i+1}")
                goblins.append(goblin)
            return goblins

        self.scene_manager.add_scene(CombatScene(
            scene_id="goblin_guards",
            title="⚔️ GARDES GOBELINS",
            description="Trois gobelins vous attaquent!",
            enemies_factory=create_goblins,
            on_victory_scene="goblin_lair",
            on_defeat_scene="game_over"
        ))

        # GOBLIN LAIR
        lair_text = """Vous pénétrez dans le repaire gobelin. Des paillasses sales,
des tonneaux de provisions volées, et... une cage!
        
À l'intérieur, un halfling prisonnier vous appelle faiblement.
"Aidez-moi... Je suis Erky Timbers, clerc d'Oakhurst... Ils m'ont capturé!"
        
Un gobelin chef plus imposant se tient près de la cage."""

        self.scene_manager.add_scene(ChoiceScene(
            scene_id="goblin_lair",
            title="🏚️ REPAIRE DES GOBELINS",
            description=lair_text,
            choices=[
                {
                    'text': "Attaquer le chef gobelin pour libérer le prisonnier",
                    'next_scene': "boss_goblin_chief",
                    'effects': {}
                },
                {
                    'text': "Négocier avec le chef gobelin",
                    'next_scene': "negotiate_goblins",
                    'effects': {}
                },
                {
                    'text': "Chercher une clé pour la cage",
                    'next_scene': "search_key",
                    'effects': {}
                }
            ]
        ))

        # BOSS FIGHT
        def create_goblin_chief(ctx):
            chief = self._create_goblin_chief()
            return [chief]

        self.scene_manager.add_scene(CombatScene(
            scene_id="boss_goblin_chief",
            title="👹 CHEF GOBELIN",
            description="Le chef gobelin hurle et charge!",
            enemies_factory=create_goblin_chief,
            on_victory_scene="rescue_erky",
            on_defeat_scene="game_over"
        ))

        # RESCUE
        rescue_text = """Vous libérez Erky Timbers de sa cage!
        
"Merci, aventuriers! J'ai été capturé il y a des semaines. Je peux vous soigner!"
        
Erky utilise ses derniers sorts pour vous restaurer."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="rescue_erky",
            title="🆘 SAUVETAGE",
            text=rescue_text,
            next_scene_id="rest_lair"
        ))

        # REST IN LAIR
        self.scene_manager.add_scene(RestScene(
            scene_id="rest_lair",
            title="💤 REPOS DANS LE REPAIRE",
            rest_type="long",
            next_scene_id="underground_gardens"
        ))

        # UNDERGROUND GARDENS
        gardens_text = """Vous descendez vers les jardins souterrains.
        
Une lumière étrange émane d'une caverne massive. Des plantes phosphorescentes 
poussent partout, créant une atmosphère irréelle.
        
Au centre, vous voyez un arbre immense et tordu... le Gulthias Tree."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="underground_gardens",
            title="🌳 JARDINS SOUTERRAINS",
            text=gardens_text,
            next_scene_id="approach_tree"
        ))

        # APPROACH TREE
        self.scene_manager.add_scene(ChoiceScene(
            scene_id="approach_tree",
            title="🌿 L'ARBRE MAUDIT",
            description="L'arbre pulse d'une énergie maléfique. Que faites-vous?",
            choices=[
                {
                    'text': "Attaquer l'arbre pour le détruire",
                    'next_scene': "tree_awakens",
                    'effects': {}
                },
                {
                    'text': "Examiner l'arbre prudemment",
                    'next_scene': "examine_tree",
                    'effects': {}
                },
                {
                    'text': "Chercher le gardien de l'arbre",
                    'next_scene': "find_guardian",
                    'effects': {}
                }
            ]
        ))

        # TREE AWAKENS - Boss final
        def create_tree_awakened(ctx):
            return [self._create_tree_blight()]

        self.scene_manager.add_scene(CombatScene(
            scene_id="tree_awakens",
            title="🌳 L'ARBRE S'ÉVEILLE!",
            description="L'arbre s'anime, ses branches devenant des tentacules meurtriers!",
            enemies_factory=create_tree_awakened,
            on_victory_scene="victory",
            on_defeat_scene="game_over"
        ))

        # VICTORY
        victory_text = """L'arbre maudit s'effondre dans un hurlement végétal!
        
Ses racines se flétrissent, libérant la citadelle de son emprise.
        
Vous avez triomphé de la Citadelle Sans Soleil!
        
Erky vous remercie chaleureusement. Les villageois d'Oakhurst vous accueilleront 
en héros. Vous avez gagné leur gratitude éternelle!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="victory",
            title="🎉 VICTOIRE!",
            text=victory_text,
            next_scene_id=None
        ))

    def _create_goblin(self, name: str) -> Monster:
        """Créer un gobelin standard"""
        slashing = DamageType(index="slashing", name="Slashing", desc="Slashing damage")

        attack = Action(
            name="Cimeterre",
            desc="Attaque de mêlée",
            type=ActionType.MELEE,
            attack_bonus=4,
            damages=[Damage(type=slashing, dd=DamageDice("1d6+2"))],
            normal_range=5
        )

        return Monster(
            index="goblin", name=name,
            abilities=Abilities(str=8, dex=14, con=10, int=10, wis=8, cha=8),
            proficiencies=[], armor_class=15, hit_points=7, hit_dice="2d6",
            xp=50, speed=30, challenge_rating=0.25, actions=[attack]
        )

    def _create_goblin_chief(self) -> Monster:
        """Créer un chef gobelin"""
        slashing = DamageType(index="slashing", name="Slashing", desc="Slashing")

        attack = Action(
            name="Grande Hache",
            desc="Attaque puissante",
            type=ActionType.MELEE,
            attack_bonus=5,
            damages=[Damage(type=slashing, dd=DamageDice("1d12+3"))],
            normal_range=5
        )

        return Monster(
            index="goblin-boss", name="Chef Gobelin",
            abilities=Abilities(str=14, dex=12, con=12, int=10, wis=10, cha=12),
            proficiencies=[], armor_class=16, hit_points=21, hit_dice="4d8+4",
            xp=200, speed=30, challenge_rating=1, actions=[attack]
        )

    def _create_tree_blight(self) -> Monster:
        """Créer le boss final - Arbre corrompu"""
        bludgeoning = DamageType(index="bludgeoning", name="Bludgeoning", desc="Impact")

        branch_attack = Action(
            name="Branches Fouettantes",
            desc="Attaque multiple avec les branches",
            type=ActionType.MELEE,
            attack_bonus=6,
            damages=[Damage(type=bludgeoning, dd=DamageDice("2d8+3"))],
            normal_range=10
        )

        return Monster(
            index="tree-blight", name="Arbre Maudit - Gulthias",
            abilities=Abilities(str=18, dex=8, con=16, int=6, wis=10, cha=8),
            proficiencies=[], armor_class=14, hit_points=45, hit_dice="6d10+12",
            xp=700, speed=20, challenge_rating=2, actions=[branch_attack]
        )


def main():
    """Lancer le scénario Tales from the Yawning Portal"""
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

