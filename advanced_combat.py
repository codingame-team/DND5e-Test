"""
Combat Avancé D&D 5e
====================
Script complet avec :
- Chargement des données depuis JSON (monstres, armes, armures, potions)
- Attaques spéciales et sorts des monstres
- Système de combat avec CombatSystem
- Gains XP et trésors après victoire
- Gestion automatique du level up
- Persistance du groupe sur disque (sauvegarde/chargement)
"""
import os
import sys
import pickle
from pathlib import Path
from typing import List, Optional
from random import choice, randint

# Add dnd-5e-core to path
_parent_dir = Path(__file__).parent.parent
_dnd_5e_core_path = _parent_dir / 'dnd-5e-core'
if _dnd_5e_core_path.exists() and str(_dnd_5e_core_path) not in sys.path:
    sys.path.insert(0, str(_dnd_5e_core_path))

# Add DnD-5th-Edition-API to path for populate_functions
_api_path = _parent_dir / 'DnD-5th-Edition-API'
if _api_path.exists() and str(_api_path) not in sys.path:
    sys.path.insert(0, str(_api_path))

from dnd_5e_core import Monster, Character, Abilities
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.mechanics import (
    calculate_encounter_difficulty,
    get_appropriate_cr_range,
    get_level_from_xp,
    perform_level_up
)
from dnd_5e_core.races import Race
from dnd_5e_core.classes import ClassType
from dnd_5e_core.abilities import AbilityType
from dnd_5e_core.equipment import HealingPotion, PotionRarity

# Import data loading functions
try:
    from populate_functions import (
        populate,
        request_monster,
        request_weapon,
        request_armor,
        request_equipment
    )
    from populate_rpg_functions import load_potions_collections
    DATA_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: populate_functions not available")
    DATA_AVAILABLE = False


# =============================================================================
# CONFIGURATION
# =============================================================================

SAVE_DIR = Path(__file__).parent / "savegames"
PARTY_FILE = SAVE_DIR / "party.pkl"
ROSTER_DIR = SAVE_DIR / "roster"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_basic_race(name: str, speed: int = 30) -> Race:
    """Créer une race simplifiée"""
    return Race(
        index=name.lower(),
        name=name,
        speed=speed,
        ability_bonuses={},
        alignment="Any",
        age="Varies",
        size="Medium",
        size_description="Medium size",
        starting_proficiencies=[],
        starting_proficiency_options=[],
        languages=[],
        language_desc="Common",
        traits=[],
        subraces=[]
    )


def create_basic_class(name: str, hit_die: int, can_cast: bool = False) -> ClassType:
    """Créer une classe simplifiée"""
    return ClassType(
        index=name.lower(),
        name=name,
        hit_die=hit_die,
        proficiency_choices=[],
        proficiencies=[],
        saving_throws=[AbilityType.STR, AbilityType.CON],
        starting_equipment=[],
        starting_equipment_options=[],
        class_levels=[],
        multi_classing=[],
        subclasses=[],
        spellcasting_level=1 if can_cast else 0,
        spellcasting_ability="int" if can_cast else None,
        can_cast=can_cast,
        spell_slots={},
        spells_known=[],
        cantrips_known=[]
    )


def create_default_party() -> List[Character]:
    """Créer un groupe par défaut de 6 aventuriers"""
    party = [
        # Ligne de front
        Character("Thorgrim", create_basic_race("Dwarf"), None, "Mountain Dwarf", "Male",
                  "4'5\"", "180 lbs", 45, create_basic_class("Fighter", 10), [],
                  Abilities(16, 14, 15, 10, 12, 8), Abilities(16, 14, 15, 10, 12, 8),
                  38, 38, 25, 0.0, False, 2700, 4, [], 150, None, []),

        Character("Ser Aldric", create_basic_race("Human"), None, "Human", "Male",
                  "6'0\"", "200 lbs", 28, create_basic_class("Paladin", 10), [],
                  Abilities(15, 10, 14, 10, 12, 15), Abilities(15, 10, 14, 10, 12, 15),
                  28, 28, 30, 0.0, False, 900, 3, [], 120, None, []),

        Character("Grok", create_basic_race("Half-Orc"), None, "Half-Orc", "Male",
                  "6'4\"", "240 lbs", 22, create_basic_class("Barbarian", 12), [],
                  Abilities(18, 14, 16, 8, 10, 10), Abilities(18, 14, 16, 8, 10, 10),
                  55, 55, 40, 0.0, False, 6500, 5, [], 100, None, []),

        # Ligne arrière
        Character("Lyra", create_basic_race("Elf"), None, "Wood Elf", "Female",
                  "5'7\"", "130 lbs", 110, create_basic_class("Ranger", 10), [],
                  Abilities(12, 17, 13, 12, 15, 10), Abilities(12, 17, 13, 12, 15, 10),
                  25, 25, 35, 0.0, False, 900, 3, [], 110, None, []),

        Character("Elara", create_basic_race("High Elf"), None, "High Elf", "Female",
                  "5'5\"", "110 lbs", 150, create_basic_class("Wizard", 6, True), [],
                  Abilities(8, 14, 12, 17, 13, 10), Abilities(8, 14, 12, 17, 13, 10),
                  22, 22, 30, 0.0, False, 2700, 4, [], 200, None, []),

        Character("Frère Marcus", create_basic_race("Human"), None, "Human", "Male",
                  "5'10\"", "170 lbs", 35, create_basic_class("Cleric", 8, True), [],
                  Abilities(13, 10, 14, 12, 16, 14), Abilities(13, 10, 14, 12, 16, 14),
                  24, 24, 30, 0.0, False, 900, 3, [], 130, None, []),
    ]

    # Initialize tracking attributes
    for char in party:
        if not hasattr(char, 'kills'):
            char.kills = []
        if not hasattr(char, 'healing_potions'):
            char.healing_potions = []

    return party


# =============================================================================
# PERSISTENCE FUNCTIONS
# =============================================================================

def save_party(party: List[Character]):
    """Sauvegarder le groupe sur disque"""
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(PARTY_FILE, 'wb') as f:
        pickle.dump(party, f)
    print(f"✅ Groupe sauvegardé dans {PARTY_FILE}")


def load_party() -> Optional[List[Character]]:
    """Charger le groupe depuis le disque"""
    if PARTY_FILE.exists():
        with open(PARTY_FILE, 'rb') as f:
            party = pickle.load(f)
        print(f"✅ Groupe chargé depuis {PARTY_FILE}")
        return party
    return None


def save_character(char: Character):
    """Sauvegarder un personnage individuel"""
    ROSTER_DIR.mkdir(parents=True, exist_ok=True)
    char_file = ROSTER_DIR / f"{char.name}.pkl"
    with open(char_file, 'wb') as f:
        pickle.dump(char, f)


# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_monsters_from_json(count: int = 10, min_cr: float = 0.5, max_cr: float = 3) -> List[Monster]:
    """Charger des monstres depuis JSON"""
    if not DATA_AVAILABLE:
        print("⚠️  Using fallback monsters")
        return []

    try:
        monster_names = populate(collection_name="monsters", key_name="results")
        monsters = []

        for name in monster_names[:count * 3]:  # Load more to filter
            try:
                monster = request_monster(name)
                if monster and min_cr <= monster.challenge_rating <= max_cr:
                    monsters.append(monster)
                    if len(monsters) >= count:
                        break
            except Exception as e:
                continue

        return monsters
    except Exception as e:
        print(f"⚠️  Error loading monsters: {e}")
        return []


def load_equipment_from_json():
    """Charger armes, armures et potions depuis JSON"""
    weapons = []
    armors = []
    equipments = []
    potions = []

    if not DATA_AVAILABLE:
        return weapons, armors, equipments, potions

    try:
        # Load weapons
        weapon_names = populate(collection_name="weapons", key_name="equipment")
        weapons = [request_weapon(name) for name in weapon_names[:20]]
        weapons = [w for w in weapons if w is not None]

        # Load armors
        armor_names = populate(collection_name="armors", key_name="equipment")
        armors = [request_armor(name) for name in armor_names[:15]]
        armors = [a for a in armors if a is not None]

        # Load equipment
        equipment_names = populate(collection_name="equipment", key_name="results")
        equipments = [request_equipment(name) for name in equipment_names[:20]]
        equipments = [e for e in equipments if e is not None]

        # Load potions
        potions = load_potions_collections()

    except Exception as e:
        print(f"⚠️  Error loading equipment: {e}")

    return weapons, armors, equipments, potions


# =============================================================================
# LEVEL UP MANAGEMENT
# =============================================================================

def check_and_level_up(char: Character) -> bool:
    """Vérifier et appliquer le level up si nécessaire"""
    new_level = get_level_from_xp(char.xp)

    if new_level > char.level:
        old_level = char.level
        result = perform_level_up(char)

        if result:
            print(f"\n🎉 {char.name} passe au niveau {new_level}!")
            print(f"   HP: +{result.hp_gain} (Total: {char.hit_points}/{char.max_hit_points})")
            if result.ability_score_improvement:
                print(f"   ⭐ Amélioration de caractéristique disponible!")
            return True

    return False


# =============================================================================
# COMBAT FUNCTION
# =============================================================================

def run_combat(party: List[Character], monsters: List[Monster],
               weapons: List, armors: List, equipments: List, potions: List):
    """Exécuter un combat complet avec gains XP et trésors"""

    alive_chars = party.copy()
    alive_monsters = monsters.copy()

    # Calculate difficulty
    party_levels = [c.level for c in party]
    monster_crs = [m.challenge_rating for m in monsters]
    adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

    print("\n" + "=" * 70)
    print("  ⚔️  DÉBUT DU COMBAT!")
    print("=" * 70)
    print(f"Difficulté: {difficulty.upper()} (XP ajusté: {adjusted_xp})")
    print(f"Aventuriers: {len(party)} | Monstres: {len(monsters)}")
    print("-" * 70)

    # Combat system
    combat = CombatSystem(verbose=True)
    round_num = 1
    max_rounds = 50

    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'='*70}")
        print(f"  ROUND {round_num}")
        print(f"{'='*70}")
        print(f"Héros: {len(alive_chars)}/{len(party)} | Monstres: {len(alive_monsters)}/{len(monsters)}")
        print("-" * 70)

        # Character turns
        for char in alive_chars.copy():
            if not alive_monsters:
                break

            if char.hit_points <= 0:
                if char in alive_chars:
                    alive_chars.remove(char)
                continue

            char_index = party.index(char)
            in_melee = char_index < 3

            combat.character_turn(
                character=char,
                alive_chars=alive_chars,
                alive_monsters=alive_monsters,
                party=party,
                weapons=weapons,
                armors=armors,
                equipments=equipments,
                potions=potions
            )

        # Monster turns
        for monster in alive_monsters.copy():
            if not alive_chars:
                break

            if monster.hit_points <= 0:
                if monster in alive_monsters:
                    alive_monsters.remove(monster)
                continue

            # Limiter l'attaque à la ligne de front
            melee_chars = [c for c in alive_chars if party.index(c) < 3]
            ranged_chars = [c for c in alive_chars if party.index(c) >= 3]
            accessible_chars = melee_chars if melee_chars else ranged_chars

            combat.monster_turn(
                monster=monster,
                alive_monsters=alive_monsters,
                alive_chars=accessible_chars,
                party=party,
                round_num=round_num
            )

        round_num += 1

    # =============================================================================
    # POST-COMBAT: RÉSULTATS ET GAINS
    # =============================================================================

    print("\n" + "=" * 70)
    print("  FIN DU COMBAT!")
    print("=" * 70)

    if alive_chars:
        print(f"\n🎉 VICTOIRE!")

        # Show survivors
        print(f"\nSurvivants ({len(alive_chars)}/{len(party)}):")
        for char in alive_chars:
            hp_pct = (char.hit_points / char.max_hit_points) * 100
            status = "✓" if hp_pct > 50 else "⚠" if hp_pct > 25 else "!"
            print(f"  {status} {char.name} ({char.class_type.name} Lv{char.level}) - HP: {char.hit_points}/{char.max_hit_points} ({hp_pct:.0f}%)")

        # Show fallen
        if len(alive_chars) < len(party):
            print(f"\n💀 Héros tombés:")
            for char in party:
                if char not in alive_chars:
                    print(f"  ✝ {char.name} ({char.class_type.name} Lv{char.level})")

        # Calculate total gains
        total_xp = sum(m.xp for m in monsters if m not in alive_monsters)
        total_gold = 0

        print(f"\n💰 BUTIN:")
        print(f"  Monstres vaincus: {len(monsters) - len(alive_monsters)}/{len(monsters)}")
        print(f"  XP total: {total_xp}")

        # Distribute XP and check for level up
        leveled_up = []
        for char in alive_chars:
            old_level = char.level
            # XP is already gained in combat.character_turn via victory()
            if check_and_level_up(char):
                leveled_up.append((char, old_level, char.level))

        if leveled_up:
            print(f"\n⭐ LEVEL UP!")
            for char, old_lvl, new_lvl in leveled_up:
                print(f"  {char.name}: Niveau {old_lvl} → {new_lvl}")

        # Show total kills per character
        print(f"\n🗡️  TABLEAU DES KILLS:")
        for char in party:
            if hasattr(char, 'kills'):
                print(f"  {char.name}: {len(char.kills)} monstres tués")

    elif alive_monsters:
        print(f"\n💀 DÉFAITE TOTALE!")
        print(f"Monstres survivants: {len(alive_monsters)}/{len(monsters)}")
    else:
        print(f"\n⚔️  ÉGALITÉ!")

    print("=" * 70)


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    """Programme principal"""
    print("=" * 70)
    print("  D&D 5e - Combat Avancé")
    print("=" * 70)

    # Try to load existing party
    party = load_party()

    if party:
        print(f"\n✅ Groupe existant chargé ({len(party)} aventuriers)")
        for i, char in enumerate(party):
            position = "FRONT" if i < 3 else "ARRIÈRE"
            print(f"  [{position}] {char.name} - {char.class_type.name} Lv{char.level} (XP: {char.xp}, HP: {char.hit_points}/{char.max_hit_points})")
    else:
        print(f"\n✨ Création d'un nouveau groupe")
        party = create_default_party()
        for i, char in enumerate(party):
            position = "FRONT" if i < 3 else "ARRIÈRE"
            print(f"  [{position}] {char.name} - {char.class_type.name} Lv{char.level}")

    # Heal party to full
    for char in party:
        char.hit_points = char.max_hit_points

    # Load equipment
    print(f"\n📦 Chargement des équipements...")
    weapons, armors, equipments, potions = load_equipment_from_json()
    print(f"  Armes: {len(weapons)}, Armures: {len(armors)}, Équipement: {len(equipments)}, Potions: {len(potions)}")

    # Generate encounter
    avg_level = sum(c.level for c in party) // len(party)
    min_cr, max_cr = get_appropriate_cr_range(avg_level)

    print(f"\n🎲 Génération d'une rencontre...")
    print(f"  Niveau moyen du groupe: {avg_level}")
    print(f"  Range de CR: {min_cr} - {max_cr}")

    # Load monsters
    monsters = load_monsters_from_json(count=randint(4, 8), min_cr=min_cr, max_cr=max_cr)

    if not monsters:
        print("⚠️  Aucun monstre disponible, utilisation de monstres de secours")
        # Use fallback from epic_combat.py
        from epic_combat import create_monster, slashing, bludgeoning, piercing
        monsters = [
            create_monster("Orc", 0.5, 15, 13, 16, "Greataxe", 5, "1d12+3", slashing),
            create_monster("Goblin", 0.25, 7, 15, 8, "Scimitar", 4, "1d6+2", slashing),
            create_monster("Hobgoblin", 0.5, 11, 18, 13, "Longsword", 3, "1d8+1", slashing),
        ]

    print(f"\n👹 MONSTRES:")
    for monster in monsters:
        print(f"  - {monster.name} (CR {monster.challenge_rating}, HP: {monster.hit_points}, AC: {monster.armor_class})")

    # Run combat
    run_combat(party, monsters, weapons, armors, equipments, potions)

    # Save party
    print(f"\n💾 Sauvegarde du groupe...")
    save_party(party)

    # Save individual characters
    for char in party:
        save_character(char)

    print(f"\n✅ Terminé!")


if __name__ == "__main__":
    main()

