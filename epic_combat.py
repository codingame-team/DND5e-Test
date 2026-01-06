"""
Combat difficile avec un groupe de 6 aventuriers vs une horde de monstres
Utilise le système de Challenge Rating pour créer un combat "HARD" ou "DEADLY"
"""
from dnd_5e_core import Monster, Character, Abilities
from dnd_5e_core.combat import CombatSystem, Action, ActionType, Damage
from dnd_5e_core.mechanics import DamageDice, calculate_encounter_difficulty, get_appropriate_cr_range
from dnd_5e_core.equipment import DamageType
from dnd_5e_core.races import Race
from dnd_5e_core.classes import ClassType
from dnd_5e_core.abilities import AbilityType


def create_damage_type(index: str, name: str) -> DamageType:
    """Créer un type de dégâts"""
    return DamageType(index=index, name=name, desc=f"{name} damage")


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


def create_monster(name: str, cr: float, hp: int, ac: int, str_val: int,
                   attack_name: str, attack_bonus: int, damage_dice: str,
                   damage_type: DamageType) -> Monster:
    """Créer un monstre"""
    abilities = Abilities(str=str_val, dex=12, con=14, int=7, wis=10, cha=8)

    action = Action(
        name=attack_name,
        desc=f"Melee Weapon Attack: +{attack_bonus} to hit, reach 5 ft.",
        type=ActionType.MELEE,
        attack_bonus=attack_bonus,
        damages=[Damage(type=damage_type, dd=DamageDice(damage_dice))],
        normal_range=5
    )

    return Monster(
        index=name.lower().replace(" ", "-"),
        name=name,
        abilities=abilities,
        proficiencies=[],
        armor_class=ac,
        hit_points=hp,
        hit_dice=f"{hp//6}d8+{hp//6}",
        xp=int(cr * 200),
        speed=30,
        challenge_rating=cr,
        actions=[action]
    )


# Types de dégâts
slashing = create_damage_type("slashing", "Slashing")
piercing = create_damage_type("piercing", "Piercing")
bludgeoning = create_damage_type("bludgeoning", "Bludgeoning")

# =============================================================================
# CRÉATION DU GROUPE (même groupe que party_combat.py)
# =============================================================================

party = [
    Character("Thorgrim", create_basic_race("Dwarf"), None, "Mountain Dwarf", "Male", "4'5\"", "180 lbs", 45,
              create_basic_class("Fighter", 10), [], Abilities(16, 14, 15, 10, 12, 8),
              Abilities(16, 14, 15, 10, 12, 8), 38, 38, 25, 0.0, False, 2700, 4, [], 150, None, []),

    Character("Ser Aldric", create_basic_race("Human"), None, "Human", "Male", "6'0\"", "200 lbs", 28,
              create_basic_class("Paladin", 10), [], Abilities(15, 10, 14, 10, 12, 15),
              Abilities(15, 10, 14, 10, 12, 15), 28, 28, 30, 0.0, False, 900, 3, [], 120, None, []),

    Character("Grok", create_basic_race("Half-Orc"), None, "Half-Orc", "Male", "6'4\"", "240 lbs", 22,
              create_basic_class("Barbarian", 12), [], Abilities(18, 14, 16, 8, 10, 10),
              Abilities(18, 14, 16, 8, 10, 10), 55, 55, 40, 0.0, False, 6500, 5, [], 100, None, []),

    Character("Lyra", create_basic_race("Elf"), None, "Wood Elf", "Female", "5'7\"", "130 lbs", 110,
              create_basic_class("Ranger", 10), [], Abilities(12, 17, 13, 12, 15, 10),
              Abilities(12, 17, 13, 12, 15, 10), 25, 25, 35, 0.0, False, 900, 3, [], 110, None, []),

    Character("Elara", create_basic_race("High Elf"), None, "High Elf", "Female", "5'5\"", "110 lbs", 150,
              create_basic_class("Wizard", 6, True), [], Abilities(8, 14, 12, 17, 13, 10),
              Abilities(8, 14, 12, 17, 13, 10), 22, 22, 30, 0.0, False, 2700, 4, [], 200, None, []),

    Character("Frère Marcus", create_basic_race("Human"), None, "Human", "Male", "5'10\"", "170 lbs", 35,
              create_basic_class("Cleric", 8, True), [], Abilities(13, 10, 14, 12, 16, 14),
              Abilities(13, 10, 14, 12, 16, 14), 24, 24, 30, 0.0, False, 900, 3, [], 130, None, []),
]

alive_chars = party.copy()
party_levels = [char.level for char in party]

# =============================================================================
# CRÉATION D'UNE HORDE DE MONSTRES POUR UN COMBAT DIFFICILE
# =============================================================================

monsters = [
    # Groupe 1: Orcs (CR 0.5)
    create_monster("Orc Warrior 1", 0.5, 15, 13, 16, "Greataxe", 5, "1d12+3", slashing),
    create_monster("Orc Warrior 2", 0.5, 15, 13, 16, "Greataxe", 5, "1d12+3", slashing),
    create_monster("Orc Warrior 3", 0.5, 15, 13, 16, "Greataxe", 5, "1d12+3", slashing),

    # Groupe 2: Hobgoblins (CR 0.5)
    create_monster("Hobgoblin 1", 0.5, 11, 18, 13, "Longsword", 3, "1d8+1", slashing),
    create_monster("Hobgoblin 2", 0.5, 11, 18, 13, "Longsword", 3, "1d8+1", slashing),

    # Groupe 3: Bugbears (CR 1) - Plus forts
    create_monster("Bugbear 1", 1, 27, 16, 15, "Morningstar", 4, "2d8+2", bludgeoning),
    create_monster("Bugbear 2", 1, 27, 16, 15, "Morningstar", 4, "2d8+2", bludgeoning),

    # Chef: Orc Eye of Gruumsh (CR 2)
    create_monster("Orc Eye of Gruumsh", 2, 45, 16, 18, "Spear", 6, "1d6+4", piercing),
]

alive_monsters = monsters.copy()

# Calculer la difficulté
monster_crs = [m.challenge_rating for m in monsters]
adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

print("=" * 70)
print("  COMBAT ÉPIQUE: Horde de Monstres!")
print("=" * 70)
print(f"\nGroupe: 6 aventuriers (Niveau moyen: {sum(party_levels)//len(party_levels)})")
print(f"Monstres: {len(monsters)} créatures")
print(f"\nDifficulté: {difficulty.upper()}")
print(f"XP ajusté: {adjusted_xp}")
print("=" * 70)

print("\n--- AVENTURIERS ---")
for i, char in enumerate(party):
    position = "FRONT" if i < 3 else "ARRIÈRE"
    print(f"[{position}] {char.name} - {char.class_type.name} Lv{char.level} (HP: {char.hit_points})")

print("\n--- MONSTRES ---")
for monster in monsters:
    print(f"{monster.name} - CR {monster.challenge_rating} (HP: {monster.hit_points}, AC: {monster.armor_class})")

print("=" * 70)

# =============================================================================
# COMBAT
# =============================================================================

combat = CombatSystem(verbose=True)
round_num = 1
max_rounds = 50

while alive_chars and alive_monsters and round_num <= max_rounds:
    print(f"\n{'='*70}")
    print(f"  ROUND {round_num}")
    print(f"{'='*70}")
    print(f"Héros: {len(alive_chars)}/{len(party)} | Monstres: {len(alive_monsters)}/{len(monsters)}")
    print("-" * 70)

    # Tours des personnages
    for char in alive_chars.copy():
        if not alive_monsters:
            break

        if char.hit_points <= 0:
            if char in alive_chars:
                alive_chars.remove(char)
            continue

        char_index = party.index(char)
        in_melee = char_index < 3

        combat.character_turn(char, alive_chars, alive_monsters, party)

    # Tours des monstres
    for monster in alive_monsters.copy():
        if not alive_chars:
            break

        if monster.hit_points <= 0:
            if monster in alive_monsters:
                alive_monsters.remove(monster)
            continue

        # Les monstres attaquent prioritairement la ligne de front
        melee_chars = [c for c in alive_chars if party.index(c) < 3]
        ranged_chars = [c for c in alive_chars if party.index(c) >= 3]
        accessible_chars = melee_chars if melee_chars else ranged_chars

        combat.monster_turn(monster, alive_monsters, accessible_chars, party, round_num)

    round_num += 1

# =============================================================================
# RÉSULTATS
# =============================================================================

print("\n" + "=" * 70)
print("  FIN DU COMBAT!")
print("=" * 70)

if alive_chars:
    print(f"\n🎉 VICTOIRE HÉROÏQUE!")
    print(f"\nSurvivants ({len(alive_chars)}/{len(party)}):")
    for char in alive_chars:
        status = "✓" if char.hit_points > char.max_hit_points * 0.5 else "!"
        print(f"  {status} {char.name} ({char.class_type.name}) - HP: {char.hit_points}/{char.max_hit_points}")

    if len(alive_chars) < len(party):
        print(f"\n💀 Héros tombés:")
        for char in party:
            if char not in alive_chars:
                print(f"  ✝ {char.name} ({char.class_type.name})")

    kills_count = len(monsters) - len(alive_monsters)
    print(f"\nMonstres vaincus: {kills_count}/{len(monsters)}")

elif alive_monsters:
    print(f"\n💀 DÉFAITE TOTALE!")
    print(f"\nMonstres survivants: {len(alive_monsters)}/{len(monsters)}")
else:
    print("\n⚔️  ÉGALITÉ!")

print("=" * 70)

