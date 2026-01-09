"""
Spellcasting system for managing spells and spell slots
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import random


@dataclass
class Spell:
    """Represents a D&D spell"""
    name: str
    level: int
    school: str  # evocation, necromancy, etc.
    casting_time: str
    range: str
    components: List[str]
    duration: str
    description: str
    damage_dice: Optional[str] = None  # e.g., "3d8"
    healing_dice: Optional[str] = None  # e.g., "1d8+3"
    save_type: Optional[str] = None  # DEX, CON, etc.
    save_dc: int = 13  # Default DC

    def roll_damage(self) -> int:
        """Roll spell damage"""
        if not self.damage_dice:
            return 0
        return self._roll_dice(self.damage_dice)

    def roll_healing(self) -> int:
        """Roll spell healing"""
        if not self.healing_dice:
            return 0
        return self._roll_dice(self.healing_dice)

    @staticmethod
    def _roll_dice(dice_str: str) -> int:
        """Parse and roll dice (e.g., '3d8+5')"""
        total = 0

        # Handle bonus
        if '+' in dice_str:
            dice_part, bonus = dice_str.split('+')
            total += int(bonus)
        elif '-' in dice_str:
            dice_part, penalty = dice_str.split('-')
            total -= int(penalty)
        else:
            dice_part = dice_str

        # Roll dice
        if 'd' in dice_part:
            num, sides = map(int, dice_part.split('d'))
            total += sum(random.randint(1, sides) for _ in range(num))
        else:
            total += int(dice_part)

        return max(0, total)


class SpellcastingSystem:
    """Manages spell casting for characters"""

    # Predefined spells library
    SPELL_LIBRARY: Dict[str, Spell] = {
        # Cantrips (level 0)
        "sacred_flame": Spell(
            name="Flamme Sacrée",
            level=0,
            school="evocation",
            casting_time="1 action",
            range="60 ft",
            components=["V", "S"],
            duration="Instantané",
            description="Lance une flamme sacrée. La cible doit réussir un JdS DEX ou subir des dégâts radiants.",
            damage_dice="1d8",
            save_type="DEX"
        ),
        "fire_bolt": Spell(
            name="Trait de Feu",
            level=0,
            school="evocation",
            casting_time="1 action",
            range="120 ft",
            components=["V", "S"],
            duration="Instantané",
            description="Lance un projectile de feu.",
            damage_dice="1d10"
        ),

        # Level 1 spells
        "cure_wounds": Spell(
            name="Soin des Blessures",
            level=1,
            school="evocation",
            casting_time="1 action",
            range="Touch",
            components=["V", "S"],
            duration="Instantané",
            description="Soigne une créature que vous touchez.",
            healing_dice="1d8+3"
        ),
        "guiding_bolt": Spell(
            name="Éclair Traceur",
            level=1,
            school="evocation",
            casting_time="1 action",
            range="120 ft",
            components=["V", "S"],
            duration="1 round",
            description="Lance un éclair de lumière radieuse.",
            damage_dice="4d6"
        ),
        "magic_missile": Spell(
            name="Projectile Magique",
            level=1,
            school="evocation",
            casting_time="1 action",
            range="120 ft",
            components=["V", "S"],
            duration="Instantané",
            description="3 projectiles magiques qui touchent automatiquement.",
            damage_dice="1d4+1"  # x3 missiles
        ),
        "shield": Spell(
            name="Bouclier",
            level=1,
            school="abjuration",
            casting_time="1 réaction",
            range="Self",
            components=["V", "S"],
            duration="1 round",
            description="+5 CA jusqu'au début de votre prochain tour."
        ),

        # Level 2 spells
        "spiritual_weapon": Spell(
            name="Arme Spirituelle",
            level=2,
            school="evocation",
            casting_time="1 action bonus",
            range="60 ft",
            components=["V", "S"],
            duration="1 minute",
            description="Crée une arme spectrale qui attaque.",
            damage_dice="1d8+3"
        ),
        "scorching_ray": Spell(
            name="Rayon Ardent",
            level=2,
            school="evocation",
            casting_time="1 action",
            range="120 ft",
            components=["V", "S"],
            duration="Instantané",
            description="3 rayons de feu. Jet d'attaque pour chacun.",
            damage_dice="2d6"  # x3 rays
        )
    }

    def __init__(self):
        self.active_effects: Dict[str, List] = {}  # character_name: [effects]

    def get_spell(self, spell_id: str) -> Optional[Spell]:
        """Get spell from library"""
        return self.SPELL_LIBRARY.get(spell_id)

    def can_cast(self, character, spell: Spell) -> bool:
        """Check if character can cast spell"""
        # Cantrips don't require slots
        if spell.level == 0:
            return character.class_type.can_cast

        # Check spell slots
        return character.can_cast_spell(spell.level)

    def cast_healing_spell(self, character, spell: Spell, target) -> Optional[int]:
        """Cast a healing spell"""
        if not self.can_cast(character, spell):
            return None

        # Use spell slot
        if spell.level > 0:
            character.cast_spell(spell.level)

        # Roll healing
        healing = spell.roll_healing()

        # Apply healing
        old_hp = target.hit_points
        target.hit_points = min(target.hit_points + healing, target.max_hit_points)
        actual_healing = target.hit_points - old_hp

        return actual_healing

    def cast_damage_spell(self, character, spell: Spell, target) -> Optional[Dict]:
        """Cast a damage spell"""
        if not self.can_cast(character, spell):
            return None

        # Use spell slot
        if spell.level > 0:
            character.cast_spell(spell.level)

        result = {
            'hit': False,
            'damage': 0,
            'save_success': False
        }

        # Check if spell requires save
        if spell.save_type:
            # Target makes saving throw
            save_roll = random.randint(1, 20)
            save_modifier = getattr(target.abilities, spell.save_type.lower(), 10) // 2 - 5
            save_total = save_roll + save_modifier

            result['save_success'] = save_total >= spell.save_dc

            # Half damage on successful save for some spells
            damage = spell.roll_damage()
            if result['save_success']:
                damage = damage // 2

            result['hit'] = damage > 0
            result['damage'] = damage
        else:
            # Spell attack roll
            attack_roll = random.randint(1, 20)
            spell_attack_bonus = character.get_attack_bonus()  # Intelligence modifier + proficiency

            if attack_roll + spell_attack_bonus >= target.armor_class:
                result['hit'] = True
                result['damage'] = spell.roll_damage()

        # Apply damage
        if result['hit']:
            target.hit_points -= result['damage']

        return result

    def cast_buff_spell(self, character, spell: Spell, target) -> bool:
        """Cast a buff spell"""
        if not self.can_cast(character, spell):
            return False

        # Use spell slot
        if spell.level > 0:
            character.cast_spell(spell.level)

        # Apply effect (simplified)
        if spell.name == "Bouclier":
            target.armor_class += 5
            # TODO: Add effect tracking with duration

        return True

    def get_prepared_spells(self, character) -> List[Spell]:
        """Get all prepared spells for character"""
        spells = []

        # Based on class
        if character.class_type.name == "Cleric":
            spells = [
                self.get_spell("sacred_flame"),
                self.get_spell("cure_wounds"),
                self.get_spell("guiding_bolt"),
                self.get_spell("spiritual_weapon")
            ]
        elif character.class_type.name == "Wizard":
            spells = [
                self.get_spell("fire_bolt"),
                self.get_spell("magic_missile"),
                self.get_spell("shield"),
                self.get_spell("scorching_ray")
            ]

        return [s for s in spells if s is not None]

    def format_spell_slots(self, character) -> str:
        """Format spell slots for display"""
        if not character.class_type.can_cast:
            return "Pas de sorts"

        slots = []
        for level in sorted(character.spell_slots_current.keys()):
            current = character.spell_slots_current[level]
            max_slots = character._init_spell_slots()[level]
            slots.append(f"Niv{level}: {current}/{max_slots}")

        return " | ".join(slots)

