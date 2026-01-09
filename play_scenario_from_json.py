#!/usr/bin/env python3
"""
Script de démonstration pour jouer un scénario depuis JSON
Exemple: La Chasse aux Gobelins
"""

from pathlib import Path
from dnd_5e_core import Character
from src.scenes.scene_factory import SceneFactory
from src.utils.monster_factory import MonsterFactory
from src.utils.save_manager import JSONLoader
from src.rendering.renderer import create_renderer
from dnd_5e_core.combat import CombatSystem


def create_demo_party():
    """Créer un groupe de personnages pour la démo"""
    from dnd_5e_core import Character, Abilities
    from dnd_5e_core.races import Race
    from dnd_5e_core.classes import ClassType
    from dnd_5e_core.abilities import AbilityType

    # Race humaine de base
    human = Race(
        index='human', name='Humain', speed=30, ability_bonuses={},
        alignment='Any', age='Adult', size='Medium', size_description='5-6 ft',
        starting_proficiencies=[], starting_proficiency_options=[],
        languages=[], language_desc='Common', traits=[], subraces=[]
    )

    # Classe Guerrier
    fighter = ClassType(
        index='fighter', name='Fighter', hit_die=10, proficiency_choices=[],
        proficiencies=[], saving_throws=[AbilityType.STR, AbilityType.CON],
        starting_equipment=[], starting_equipment_options=[], class_levels=[],
        multi_classing=[], subclasses=[], spellcasting_level=0,
        spellcasting_ability=None, can_cast=False, spell_slots={},
        spells_known=[], cantrips_known=[]
    )

    # Classe Clerc
    cleric = ClassType(
        index='cleric', name='Cleric', hit_die=8, proficiency_choices=[],
        proficiencies=[], saving_throws=[AbilityType.WIS, AbilityType.CHA],
        starting_equipment=[], starting_equipment_options=[], class_levels=[],
        multi_classing=[], subclasses=[], spellcasting_level=3,
        spellcasting_ability='wis', can_cast=True, spell_slots={},
        spells_known=[], cantrips_known=[]
    )

    # Guerrier
    grok = Character(
        name="Grok", race=human, subrace=None, ethnic='Human', gender='Male',
        height='6ft', weight='180 lbs', age=30,
        class_type=fighter, proficiencies=[],
        abilities=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=10),
        ability_modifiers=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=10),
        hit_points=28, max_hit_points=28,
        speed=30, haste_timer=0.0, hasted=False,
        xp=900, level=3, inventory=[], gold=50
    )

    # Clerc
    elara = Character(
        name="Sœur Elara", race=human, subrace=None, ethnic='Human', gender='Female',
        height='5ft6', weight='140 lbs', age=28,
        class_type=cleric, proficiencies=[],
        abilities=Abilities(str=12, dex=10, con=14, int=13, wis=16, cha=14),
        ability_modifiers=Abilities(str=12, dex=10, con=14, int=13, wis=16, cha=14),
        hit_points=24, max_hit_points=24,
        speed=30, haste_timer=0.0, hasted=False,
        xp=900, level=3, inventory=[], gold=30
    )

    return [grok, elara]


def main():
    print("=" * 70)
    print("  🎲 DÉMO: SCÉNARIO DEPUIS JSON")
    print("  La Chasse aux Gobelins")
    print("=" * 70)

    # Charger le scénario JSON
    json_path = Path("data/scenes/chasse_gobelins.json")

    if not json_path.exists():
        print(f"\n❌ Fichier de scénario non trouvé: {json_path}")
        print("Assurez-vous que les fichiers JSON sont dans data/scenes/")
        return

    # Créer les systèmes de jeu
    renderer = create_renderer(use_ncurses=False)
    combat_system = CombatSystem(verbose=True)

    # Charger les monstres
    json_loader = JSONLoader()
    monsters_data = json_loader.load_monsters()
    monster_factory = MonsterFactory(monsters_data)

    # Si pas de monstres dans data/, utiliser ceux du package dnd_5e_core
    if not monsters_data:
        print("⚠️ Utilisation des monstres du package dnd_5e_core")
        from dnd_5e_core.entities import FiveEToolsMonsterLoader
        loader = FiveEToolsMonsterLoader()

        # Créer une factory simple depuis le FiveEToolsMonsterLoader
        class SimpleMonsterFactory:
            def __init__(self, loader):
                self.loader = loader

            def create_monster(self, monster_name):
                # Normaliser le nom (ex: "goblin_boss" -> "goblin-boss")
                normalized_name = monster_name.replace('_', '-')
                monster = self.loader.load_monster(normalized_name)
                if not monster:
                    # Essayer sans normalisation
                    monster = self.loader.load_monster(monster_name)
                return monster

        monster_factory = SimpleMonsterFactory(loader)

    # Charger le scénario
    print("\n📖 Chargement du scénario...")
    scene_manager = SceneFactory.load_scenario_from_json_file(
        str(json_path),
        monster_factory=monster_factory
    )

    if not scene_manager:
        print("❌ Impossible de charger le scénario")
        return

    print(f"✅ Scénario chargé: {scene_manager.scenes.__len__()} scènes")

    # Créer le groupe
    print("\n👥 Création du groupe d'aventuriers...")
    party = create_demo_party()

    for char in party:
        print(f"  - {char.name} (niveau {char.level} {char.class_type.name})")

    # État du jeu
    game_state = {
        'combat_victories': 0,
        'total_xp': 0,
        'gold': 100,
        'gold_spent': 0,
        'locations_visited': 0,
        'npcs_met': 0,
        'quests_completed': 0,
        'deaths': 0,
        'reputation': 0
    }

    # Contexte de jeu
    game_context = {
        'party': party,
        'game_state': game_state,
        'renderer': renderer,
        'combat_system': combat_system,
        'monster_factory': monster_factory,
        'weapons': [],
        'armors': [],
        'equipments': [],
        'potions': []
    }

    # Lancer le scénario
    print("\n" + "=" * 70)
    print("  🎮 DÉBUT DE L'AVENTURE")
    print("=" * 70)
    input("\n[Appuyez sur ENTRÉE pour commencer]")

    try:
        scene_manager.run(game_context)

        # Afficher statistiques finales
        print("\n" + "=" * 70)
        print("  📊 STATISTIQUES FINALES")
        print("=" * 70)
        print(f"💰 Or: {game_state['gold']} pièces")
        print(f"⭐ XP total: {game_state['total_xp']}")
        print(f"⚔️  Combats gagnés: {game_state['combat_victories']}")
        print(f"🗺️  Lieux visités: {game_state['locations_visited']}")
        print(f"💀 Morts: {game_state['deaths']}")
        print("\n" + "=" * 70)
        print("  Merci d'avoir joué! 🎲")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n\n⚠️ Partie interrompue")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

