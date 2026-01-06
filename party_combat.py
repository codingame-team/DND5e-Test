"""
Combat avec un groupe de 6 aventuriers vs monstres
Utilise le système de Challenge Rating pour équilibrer la rencontre
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


# =============================================================================
# CRÉATION DU GROUPE D'AVENTURIERS (6 personnages)
# =============================================================================

# Types de dégâts
slashing = create_damage_type("slashing", "Slashing")
piercing = create_damage_type("piercing", "Piercing")
bludgeoning = create_damage_type("bludgeoning", "Bludgeoning")
fire = create_damage_type("fire", "Fire")

# --- LIGNE DE FRONT (Mêlée) ---

# 1. GUERRIER (Fighter) - Niveau 4
fighter = Character(
    name="Thorgrim",
    race=create_basic_race("Dwarf"),
    subrace=None,
    ethnic="Mountain Dwarf",
    gender="Male",
    height="4'5\"",
    weight="180 lbs",
    age=45,
    class_type=create_basic_class("Fighter", 10),
    proficiencies=[],
    abilities=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=8),
    ability_modifiers=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=8),
    hit_points=38,  # 4d10 + CON bonus
    max_hit_points=38,
    speed=25,
    haste_timer=0.0,
    hasted=False,
    xp=2700,
    level=4,
    inventory=[],
    gold=150,
    sc=None,
    conditions=[]
)

# 2. PALADIN - Niveau 3
paladin = Character(
    name="Ser Aldric",
    race=create_basic_race("Human"),
    subrace=None,
    ethnic="Human",
    gender="Male",
    height="6'0\"",
    weight="200 lbs",
    age=28,
    class_type=create_basic_class("Paladin", 10),
    proficiencies=[],
    abilities=Abilities(str=15, dex=10, con=14, int=10, wis=12, cha=15),
    ability_modifiers=Abilities(str=15, dex=10, con=14, int=10, wis=12, cha=15),
    hit_points=28,
    max_hit_points=28,
    speed=30,
    haste_timer=0.0,
    hasted=False,
    xp=900,
    level=3,
    inventory=[],
    gold=120,
    sc=None,
    conditions=[]
)

# 3. BARBARE (Barbarian) - Niveau 5
barbarian = Character(
    name="Grok",
    race=create_basic_race("Half-Orc"),
    subrace=None,
    ethnic="Half-Orc",
    gender="Male",
    height="6'4\"",
    weight="240 lbs",
    age=22,
    class_type=create_basic_class("Barbarian", 12),
    proficiencies=[],
    abilities=Abilities(str=18, dex=14, con=16, int=8, wis=10, cha=10),
    ability_modifiers=Abilities(str=18, dex=14, con=16, int=8, wis=10, cha=10),
    hit_points=55,  # 5d12 + CON bonus
    max_hit_points=55,
    speed=40,
    haste_timer=0.0,
    hasted=False,
    xp=6500,
    level=5,
    inventory=[],
    gold=100,
    sc=None,
    conditions=[]
)

# --- LIGNE ARRIÈRE (Distance/Sorts) ---

# 4. RÔDEUR (Ranger) - Niveau 3
ranger = Character(
    name="Lyra",
    race=create_basic_race("Elf"),
    subrace=None,
    ethnic="Wood Elf",
    gender="Female",
    height="5'7\"",
    weight="130 lbs",
    age=110,
    class_type=create_basic_class("Ranger", 10),
    proficiencies=[],
    abilities=Abilities(str=12, dex=17, con=13, int=12, wis=15, cha=10),
    ability_modifiers=Abilities(str=12, dex=17, con=13, int=12, wis=15, cha=10),
    hit_points=25,
    max_hit_points=25,
    speed=35,
    haste_timer=0.0,
    hasted=False,
    xp=900,
    level=3,
    inventory=[],
    gold=110,
    sc=None,
    conditions=[]
)

# 5. MAGICIEN (Wizard) - Niveau 4
wizard = Character(
    name="Elara",
    race=create_basic_race("High Elf"),
    subrace=None,
    ethnic="High Elf",
    gender="Female",
    height="5'5\"",
    weight="110 lbs",
    age=150,
    class_type=create_basic_class("Wizard", 6, can_cast=True),
    proficiencies=[],
    abilities=Abilities(str=8, dex=14, con=12, int=17, wis=13, cha=10),
    ability_modifiers=Abilities(str=8, dex=14, con=12, int=17, wis=13, cha=10),
    hit_points=22,
    max_hit_points=22,
    speed=30,
    haste_timer=0.0,
    hasted=False,
    xp=2700,
    level=4,
    inventory=[],
    gold=200,
    sc=None,
    conditions=[]
)

# 6. CLERC (Cleric) - Niveau 3
cleric = Character(
    name="Frère Marcus",
    race=create_basic_race("Human"),
    subrace=None,
    ethnic="Human",
    gender="Male",
    height="5'10\"",
    weight="170 lbs",
    age=35,
    class_type=create_basic_class("Cleric", 8, can_cast=True),
    proficiencies=[],
    abilities=Abilities(str=13, dex=10, con=14, int=12, wis=16, cha=14),
    ability_modifiers=Abilities(str=13, dex=10, con=14, int=12, wis=16, cha=14),
    hit_points=24,
    max_hit_points=24,
    speed=30,
    haste_timer=0.0,
    hasted=False,
    xp=900,
    level=3,
    inventory=[],
    gold=130,
    sc=None,
    conditions=[]
)

# Groupe complet
party = [fighter, paladin, barbarian, ranger, wizard, cleric]
alive_chars = party.copy()

# =============================================================================
# CALCUL DES MONSTRES APPROPRIÉS AVEC CHALLENGE RATING
# =============================================================================

party_levels = [char.level for char in party]
avg_party_level = sum(party_levels) // len(party_levels)
min_cr, max_cr = get_appropriate_cr_range(avg_party_level)

print("=" * 70)
print("  GROUPE D'AVENTURIERS")
print("=" * 70)
print("\n--- LIGNE DE FRONT (Mêlée) ---")
for i, char in enumerate(party[:3]):
    print(f"{i+1}. {char.name} - {char.class_type.name} Niveau {char.level} (HP: {char.hit_points})")

print("\n--- LIGNE ARRIÈRE (Distance/Sorts) ---")
for i, char in enumerate(party[3:]):
    print(f"{i+4}. {char.name} - {char.class_type.name} Niveau {char.level} (HP: {char.hit_points})")

print(f"\nNiveau moyen du groupe: {avg_party_level}")
print(f"Range de CR approprié: {min_cr} - {max_cr}")
print("=" * 70)

# =============================================================================
# CRÉATION DES MONSTRES
# =============================================================================

def create_monster(name: str, cr: float, hp: int, ac: int, str_val: int,
                   attack_name: str, attack_bonus: int, damage_dice: str) -> Monster:
    """Créer un monstre simple"""
    abilities = Abilities(str=str_val, dex=12, con=14, int=7, wis=10, cha=8)

    action = Action(
        name=attack_name,
        desc=f"Melee Weapon Attack: +{attack_bonus} to hit, reach 5 ft.",
        type=ActionType.MELEE,
        attack_bonus=attack_bonus,
        damages=[Damage(type=slashing, dd=DamageDice(damage_dice))],
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

# Créer plusieurs monstres dans la plage de CR appropriée
monsters = [
    create_monster("Orc Warrior", 0.5, 15, 13, 16, "Greataxe", 5, "1d12+3"),
    create_monster("Goblin Boss", 1, 21, 17, 10, "Scimitar", 4, "1d6+2"),
    create_monster("Hobgoblin", 0.5, 11, 18, 13, "Longsword", 3, "1d8+1"),
    create_monster("Bugbear", 1, 27, 16, 15, "Morningstar", 4, "2d8+2"),
]

# Calculer la difficulté de la rencontre
monster_crs = [m.challenge_rating for m in monsters]
adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

print(f"\n--- MONSTRES RENCONTRÉS ---")
for i, monster in enumerate(monsters):
    print(f"{i+1}. {monster.name} - CR {monster.challenge_rating} (HP: {monster.hit_points}, AC: {monster.armor_class})")

print(f"\nDifficulté de la rencontre: {difficulty.upper()}")
print(f"XP ajusté: {adjusted_xp}")
print("=" * 70)

alive_monsters = monsters.copy()

# =============================================================================
# SYSTÈME DE COMBAT
# =============================================================================

combat = CombatSystem(verbose=True)

print("\n" + "=" * 70)
print("  DÉBUT DU COMBAT!")
print("=" * 70)

round_num = 1
max_rounds = 30

while alive_chars and alive_monsters and round_num <= max_rounds:
    print(f"\n{'='*70}")
    print(f"  ROUND {round_num}")
    print(f"{'='*70}")
    print(f"Aventuriers vivants: {len(alive_chars)}/{len(party)}")
    print(f"Monstres vivants: {len(alive_monsters)}/{len(monsters)}")
    print("-" * 70)

    # Tours des personnages
    for char in alive_chars.copy():
        if not alive_monsters:
            break

        # Vérifier si le personnage est encore vivant
        if char.hit_points <= 0:
            if char in alive_chars:
                alive_chars.remove(char)
            continue

        # Déterminer si le personnage est en mêlée ou à distance
        char_index = party.index(char)
        in_melee = char_index < 3  # Les 3 premiers sont en mêlée

        if in_melee:
            print(f"\n[MÊLÉE] ", end="")
        else:
            print(f"\n[DISTANCE] ", end="")

        combat.character_turn(
            character=char,
            alive_chars=alive_chars,
            alive_monsters=alive_monsters,
            party=party
        )

    # Tours des monstres
    for monster in alive_monsters.copy():
        if not alive_chars:
            break

        # Vérifier si le monstre est encore vivant
        if monster.hit_points <= 0:
            if monster in alive_monsters:
                alive_monsters.remove(monster)
            continue

        # Les monstres ne peuvent attaquer que la ligne de front en mêlée
        # S'il n'y a plus de personnages en mêlée, ils attaquent la ligne arrière
        melee_chars = [c for c in alive_chars if party.index(c) < 3]
        ranged_chars = [c for c in alive_chars if party.index(c) >= 3]

        # Modifier la liste des personnages accessibles pour ce monstre
        if melee_chars:
            # Il y a encore des personnages en mêlée, le monstre ne peut attaquer qu'eux
            accessible_chars = melee_chars
        else:
            # Plus de mêlée, les monstres peuvent atteindre l'arrière
            accessible_chars = ranged_chars

        combat.monster_turn(
            monster=monster,
            alive_monsters=alive_monsters,
            alive_chars=accessible_chars,  # Limiter les cibles accessibles
            party=party,
            round_num=round_num
        )

    round_num += 1

# =============================================================================
# RÉSULTATS
# =============================================================================

print("\n" + "=" * 70)
print("  FIN DU COMBAT!")
print("=" * 70)

if alive_chars:
    print(f"\n🎉 VICTOIRE! Le groupe a triomphé!")
    print(f"\nSurvivants ({len(alive_chars)}/{len(party)}):")
    for char in alive_chars:
        print(f"  - {char.name} ({char.class_type.name}) - HP: {char.hit_points}/{char.max_hit_points}")

    if len(alive_chars) < len(party):
        print(f"\n💀 Tombés au combat:")
        for char in party:
            if char not in alive_chars:
                print(f"  - {char.name} ({char.class_type.name})")
elif alive_monsters:
    print(f"\n💀 DÉFAITE! Le groupe a été vaincu...")
    print(f"\nMonstres survivants ({len(alive_monsters)}/{len(monsters)}):")
    for monster in alive_monsters:
        print(f"  - {monster.name} - HP: {monster.hit_points}/{monster.max_hit_points}")
else:
    print("\n⚔️  ÉGALITÉ! Tous les combattants sont tombés!")

print("=" * 70)

