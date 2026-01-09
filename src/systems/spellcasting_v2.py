"""
Spellcasting System utilisant dnd_5e_core.spells
Évite la redondance avec le package dnd-5e-core
"""

from typing import Dict, Optional, List
from dnd_5e_core.spells import Spell
from dnd_5e_core import Character
from dnd_5e_core.data import load_spell
import random


class SpellcastingManager:
    """
    Gestionnaire de sorts utilisant directement dnd_5e_core
    """

    # Cache des sorts chargés
    _spell_cache: Dict[str, Spell] = {}

    @classmethod
    def get_spell(cls, spell_name: str) -> Optional[Spell]:
        """
        Obtenir un sort depuis dnd-5e-core API
        Utilise un cache pour éviter requêtes répétées
        """
        if spell_name in cls._spell_cache:
            return cls._spell_cache[spell_name]

        try:
            spell = load_spell(spell_name)
            if spell:
                cls._spell_cache[spell_name] = spell
            return spell
        except Exception as e:
            print(f"Erreur chargement sort {spell_name}: {e}")
            return None

    @classmethod
    def get_cleric_spells(cls, level: int = 3) -> List[Spell]:
        """Obtenir sorts typiques d'un Clerc niveau 3"""
        spell_names = [
            "sacred-flame",      # Cantrip
            "cure-wounds",       # Niveau 1
            "guiding-bolt",      # Niveau 1
            "spiritual-weapon"   # Niveau 2
        ]

        spells = []
        for name in spell_names:
            spell = cls.get_spell(name)
            if spell:
                spells.append(spell)

        return spells

    @classmethod
    def get_wizard_spells(cls, level: int = 3) -> List[Spell]:
        """Obtenir sorts typiques d'un Magicien niveau 3"""
        spell_names = [
            "fire-bolt",         # Cantrip
            "magic-missile",     # Niveau 1
            "shield",            # Niveau 1
            "scorching-ray"      # Niveau 2
        ]

        spells = []
        for name in spell_names:
            spell = cls.get_spell(name)
            if spell:
                spells.append(spell)

        return spells

    @staticmethod
    def can_cast(character: Character, spell: Spell) -> bool:
        """Vérifier si personnage peut lancer le sort"""
        from src.core.adapters import CharacterExtensions

        # Cantrips toujours disponibles
        if spell.level == 0:
            return character.class_type.can_cast

        # Vérifier emplacements
        return CharacterExtensions.can_cast_spell(character, spell.level)

    @staticmethod
    def cast_healing_spell(character: Character, spell: Spell, target: Character) -> Optional[int]:
        """
        Lancer sort de soin
        Retourne montant de soin ou None si échec
        """
        from src.core.adapters import CharacterExtensions

        if not SpellcastingManager.can_cast(character, spell):
            return None

        # Utiliser emplacement
        if spell.level > 0:
            CharacterExtensions.cast_spell(character, spell.level)

        # Calculer soin (simplifié)
        if hasattr(spell, 'heal_at_slot_level'):
            # Utiliser données spell si disponibles
            heal_dice = spell.heal_at_slot_level.get(str(spell.level), "1d8")
        else:
            # Fallback simplifié
            heal_dice = "1d8+3" if spell.level == 1 else "2d8+3"

        healing = SpellcastingManager._roll_dice(heal_dice)

        # Appliquer
        old_hp = target.hit_points
        target.hit_points = min(target.hit_points + healing, target.max_hit_points)
        actual_healing = target.hit_points - old_hp

        return actual_healing

    @staticmethod
    def cast_damage_spell(character: Character, spell: Spell, target) -> Optional[Dict]:
        """
        Lancer sort de dégâts
        Retourne dict avec résultats ou None si échec
        """
        from src.core.adapters import CharacterExtensions

        if not SpellcastingManager.can_cast(character, spell):
            return None

        # Utiliser emplacement
        if spell.level > 0:
            CharacterExtensions.cast_spell(character, spell.level)

        result = {
            'hit': False,
            'damage': 0,
            'save_success': False
        }

        # Calculer dégâts selon niveau du sort
        if hasattr(spell, 'damage'):
            # Utiliser données du sort
            damage_dice = spell.damage.damage_at_slot_level.get(str(spell.level), "1d10")
        else:
            # Fallback
            damage_dice = f"{spell.level}d6" if spell.level > 0 else "1d10"

        # Vérifier save ou attaque
        if hasattr(spell, 'dc'):
            # Sort avec jet de sauvegarde
            save_roll = random.randint(1, 20)
            save_modifier = getattr(target.abilities, spell.dc.dc_type.name.lower(), 10) // 2 - 5
            save_total = save_roll + save_modifier

            result['save_success'] = save_total >= spell.dc.dc_value
            damage = SpellcastingManager._roll_dice(damage_dice)

            if result['save_success']:
                damage = damage // 2  # Demi-dégâts si save

            result['hit'] = damage > 0
            result['damage'] = damage
        else:
            # Sort d'attaque
            attack_roll = random.randint(1, 20)
            spell_attack_bonus = (character.abilities.int // 2 - 5) + (character.level // 2)

            if attack_roll + spell_attack_bonus >= target.armor_class:
                result['hit'] = True
                result['damage'] = SpellcastingManager._roll_dice(damage_dice)

        # Appliquer dégâts
        if result['hit']:
            target.hit_points -= result['damage']

        return result

    @staticmethod
    def _roll_dice(dice_str: str) -> int:
        """Parser et lancer dés (ex: '2d8+3')"""
        total = 0

        if '+' in dice_str:
            dice_part, bonus = dice_str.split('+')
            total += int(bonus)
        elif '-' in dice_str:
            dice_part, penalty = dice_str.split('-')
            total -= int(penalty)
        else:
            dice_part = dice_str

        if 'd' in dice_part:
            num, sides = map(int, dice_part.split('d'))
            total += sum(random.randint(1, sides) for _ in range(num))
        else:
            total += int(dice_part)

        return max(0, total)

    @staticmethod
    def format_spell_slots(character: Character) -> str:
        """Formater emplacements de sorts pour affichage"""
        from src.core.adapters import CharacterExtensions

        if not character.class_type.can_cast:
            return "Pas de sorts"

        if not hasattr(character, 'spell_slots_current'):
            character.spell_slots_current = CharacterExtensions.init_spell_slots(character)

        max_slots = CharacterExtensions.init_spell_slots(character)
        slots = []

        for level in sorted(character.spell_slots_current.keys()):
            current = character.spell_slots_current[level]
            maximum = max_slots[level]
            slots.append(f"Niv{level}:{current}/{maximum}")

        return " | ".join(slots)


# Alias pour compatibilité
SpellcastingSystem = SpellcastingManager

