"""
Exemple de création de personnage D&D 5e

Note: Ce script crée un personnage de manière simplifiée.
Les données complètes (races, classes, équipement) ne sont pas incluses dans le package PyPI
pour des raisons de taille. Vous pouvez :
1. Les télécharger depuis le dépôt GitHub
2. Les créer manuellement comme dans cet exemple
3. Utiliser l'API D&D 5e (https://www.dnd5eapi.co/)
"""

from dnd_5e_core.entities import Character
from dnd_5e_core.races import Race
from dnd_5e_core.classes import ClassType
from dnd_5e_core.abilities import Abilities

# Create abilities
abilities = Abilities(
    str=10,
    dex=14,
    con=12,
    int=16,
    wis=13,
    cha=8
)

# Créer une race (Elf) - Version simplifiée
# En production, vous chargeriez depuis JSON ou API
elf = Race(
    index="elf",
    name="Elf",
    speed=30,
    ability_bonuses={"dex": 2},  # Les elfes ont +2 en Dextérité
    alignment="Chaotic Good",
    age="Elves can live to be 750 years old",
    size="Medium",
    size_description="Elves range from under 5 to over 6 feet tall",
    starting_proficiencies=[],  # Perception skill (simplififié)
    starting_proficiency_options=[],
    languages=[],  # Common, Elvish (simplifié)
    language_desc="You can speak, read, and write Common and Elvish",
    traits=[],  # Darkvision, Fey Ancestry, Trance (simplifié)
    subraces=[]
)

# Créer une classe (Wizard) - Version simplifiée
wizard_class = ClassType(
    index="wizard",
    name="Wizard",
    hit_die=6,  # d6 hit die
    proficiency_choices=[],
    proficiencies=[],
    saving_throws=["int", "wis"],  # Wizards sont experts en INT et WIS saves
    starting_equipment=[],
    starting_equipment_options=[],
    class_levels=[],
    multi_classing=[],
    subclasses=[],
    spellcasting_level=1,  # Full caster (sorts au niveau 1)
    spellcasting_ability="int",  # Intelligence pour les sorts
    can_cast=True,
    spell_slots={},
    spells_known=[],
    cantrips_known=[]
)

# Create character
wizard = Character(
    name="Elyndor le Sage",
    race=elf,
    subrace=None,  # Pas de sous-race
    ethnic="High Elf",
    gender="Male",
    height="5'11\"",
    weight="150 lbs",
    age=120,
    class_type=wizard_class,
    proficiencies=[],  # Liste vide pour l'instant
    abilities=abilities,
    ability_modifiers=abilities,  # Les modificateurs sont calculés depuis les abilities
    hit_points=8,  # 6 (hit die) + 2 (CON modifier)
    max_hit_points=8,
    speed=30,  # Vitesse de l'elfe
    haste_timer=0.0,
    hasted=False,
    xp=0,  # Début de niveau 1
    level=1,
    inventory=[],  # Inventaire vide
    gold=100,
    sc=None,  # Pas de spellcaster pour l'instant (simplifié)
    conditions=[]  # Liste vide de conditions
)

# Afficher les informations du personnage
print("=" * 50)
print(f"  {wizard.name}")
print("=" * 50)
print(f"Race: {wizard.race.name}")
print(f"Class: {wizard.class_type.name} (Level {wizard.level})")
print(f"Hit Die: d{wizard.class_type.hit_die}")
print("-" * 50)
print(f"HP: {wizard.hit_points}/{wizard.max_hit_points}")
print(f"AC: {wizard.armor_class}")
print(f"Gold: {wizard.gold} gp")
print("-" * 50)
print("Ability Scores:")
print(f"  STR: {abilities.str} ({abilities.get_modifier('str'):+d})")
print(f"  DEX: {abilities.dex} ({abilities.get_modifier('dex'):+d})")
print(f"  CON: {abilities.con} ({abilities.get_modifier('con'):+d})")
print(f"  INT: {abilities.int} ({abilities.get_modifier('int'):+d})")
print(f"  WIS: {abilities.wis} ({abilities.get_modifier('wis'):+d})")
print(f"  CHA: {abilities.cha} ({abilities.get_modifier('cha'):+d})")
print("-" * 50)
print(f"Speed: {wizard.race.speed} ft")
print(f"Size: {wizard.race.size}")
print(f"Alignment: {wizard.race.alignment}")
print("=" * 50)

# Information supplémentaire
print("\nℹ️  Note:")
print("Pour accéder aux données complètes (équipement, sorts, etc.),")
print("vous pouvez télécharger les fichiers JSON depuis:")
print("https://github.com/codingame-team/dnd-5e-core/tree/main/data")
