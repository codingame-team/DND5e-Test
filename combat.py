# combat.py
from dnd_5e_core import Monster, Abilities
from dnd_5e_core.combat import CombatSystem, Action, ActionType, Damage
from dnd_5e_core.mechanics import DamageDice
from dnd_5e_core.equipment import DamageType

from create_character import wizard

# Créer les capacités de l'Orc
orc_abilities = Abilities(
    str=16,
    dex=12,
    con=14,
    int=7,
    wis=11,
    cha=10
)

# Créer le type de dégâts (slashing)
slashing_damage = DamageType(
    index="slashing",
    name="Slashing",
    desc="Slashing damage from bladed weapons"
)

# Créer l'action Greataxe Attack
greataxe_attack = Action(
    name="Greataxe Attack",
    desc="Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 9 (1d12 + 3) slashing damage.",
    type=ActionType.MELEE,
    attack_bonus=5,
    damages=[Damage(type=slashing_damage, dd=DamageDice("1d12+3"))],
    normal_range=5
)

# Créer l'Orc
orc = Monster(
    index="orc",
    name="Orc",
    abilities=orc_abilities,
    proficiencies=[],
    armor_class=13,
    hit_points=30,
    hit_dice="3d8+6",
    xp=100,
    speed=30,
    challenge_rating=0.5,
    actions=[greataxe_attack]
)

# Initialize combat system
combat = CombatSystem(verbose=True)

# Lists pour gérer les combattants vivants
alive_chars = [wizard]
alive_monsters = [orc]
party = [wizard]

print("=" * 60)
print("  COMBAT: Elyndor le Sage vs Orc")
print("=" * 60)
print(f"{wizard.name} (HP: {wizard.hit_points}/{wizard.max_hit_points})")
print(f"vs {orc.name} (HP: {orc.hit_points}/{orc.max_hit_points}, CR: {orc.challenge_rating})")
print("=" * 60)
print()

round_num = 1

# Combat loop
while alive_chars and alive_monsters:
    print(f"\n--- Round {round_num} ---")

    # Character turn
    if alive_chars and alive_monsters:
        combat.character_turn(
            character=wizard,
            alive_chars=alive_chars,
            alive_monsters=alive_monsters,
            party=party
        )

    # Monster turn
    if alive_chars and alive_monsters:
        combat.monster_turn(
            monster=orc,
            alive_monsters=alive_monsters,
            alive_chars=alive_chars,
            party=party,
            round_num=round_num
        )

    round_num += 1

    # Safety: max 20 rounds
    if round_num > 20:
        print("\nCombat ended: too many rounds!")
        break

# Résultats
print("\n" + "=" * 60)
if alive_chars:
    print(f"  VICTORY! {wizard.name} wins!")
    print(f"  Final HP: {wizard.hit_points}/{wizard.max_hit_points}")
elif alive_monsters:
    print(f"  DEFEAT! {orc.name} wins!")
    print(f"  {wizard.name} was defeated...")
else:
    print("  DRAW!")
print("=" * 60)
