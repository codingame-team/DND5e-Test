"""
Adapters pour dnd-5e-core - Éviter la redondance
Utilise directement les classes de dnd-5e-core avec extensions minimales
"""

from typing import List, Optional, Dict
from dnd_5e_core import Character, Monster
from dnd_5e_core.equipment import Weapon, Armor, Equipment
from dnd_5e_core.spells import Spell


class CharacterExtensions:
    """
    Extensions pour Character sans recréer la classe
    Utilise le pattern Mixin/Extension
    """

    @staticmethod
    def add_inventory_management(character: Character):
        """Ajouter gestion d'inventaire à un Character existant"""
        if not hasattr(character, 'inventory_items'):
            character.inventory_items = []
        if not hasattr(character, 'equipped_weapon'):
            character.equipped_weapon = None
        if not hasattr(character, 'equipped_armor'):
            character.equipped_armor = None
        if not hasattr(character, 'spell_slots_current'):
            character.spell_slots_current = {}
        return character

    @staticmethod
    def equip_weapon(character: Character, weapon: Weapon):
        """Équiper une arme"""
        if not hasattr(character, 'equipped_weapon'):
            CharacterExtensions.add_inventory_management(character)

        if character.equipped_weapon:
            character.inventory_items.append(character.equipped_weapon)
        character.equipped_weapon = weapon
        if weapon in character.inventory_items:
            character.inventory_items.remove(weapon)

    @staticmethod
    def equip_armor(character: Character, armor: Armor):
        """Équiper une armure"""
        if not hasattr(character, 'equipped_armor'):
            CharacterExtensions.add_inventory_management(character)

        if character.equipped_armor:
            character.inventory_items.append(character.equipped_armor)
        character.equipped_armor = armor
        if armor in character.inventory_items:
            character.inventory_items.remove(armor)

        # Stocker la CA de l'armure dans un attribut personnalisé
        # (armor_class est une propriété en lecture seule dans Character)
        if hasattr(armor.armor_class, 'base'):
            character._custom_armor_class = armor.armor_class.base
        else:
            character._custom_armor_class = armor.armor_class

    @staticmethod
    def get_armor_class(character: Character) -> int:
        """Obtenir la CA effective du personnage"""
        if hasattr(character, '_custom_armor_class'):
            return character._custom_armor_class
        return character.armor_class

    @staticmethod
    def add_item(character: Character, item):
        """Ajouter un item à l'inventaire"""
        if not hasattr(character, 'inventory_items'):
            CharacterExtensions.add_inventory_management(character)
        character.inventory_items.append(item)

    @staticmethod
    def remove_item(character: Character, item) -> bool:
        """Retirer un item de l'inventaire"""
        if not hasattr(character, 'inventory_items'):
            return False
        if item in character.inventory_items:
            character.inventory_items.remove(item)
            return True
        return False

    @staticmethod
    def init_spell_slots(character: Character) -> Dict[int, int]:
        """Initialiser emplacements de sorts selon niveau"""
        if not character.class_type.can_cast:
            return {}

        # Simplifié pour niveau 3
        if character.level >= 3:
            return {1: 4, 2: 2}
        elif character.level >= 2:
            return {1: 3}
        else:
            return {1: 2}

    @staticmethod
    def can_cast_spell(character: Character, spell_level: int) -> bool:
        """Vérifier si peut lancer sort"""
        if not hasattr(character, 'spell_slots_current'):
            character.spell_slots_current = CharacterExtensions.init_spell_slots(character)
        return character.spell_slots_current.get(spell_level, 0) > 0

    @staticmethod
    def cast_spell(character: Character, spell_level: int) -> bool:
        """Utiliser emplacement de sort"""
        if CharacterExtensions.can_cast_spell(character, spell_level):
            character.spell_slots_current[spell_level] -= 1
            return True
        return False

    @staticmethod
    def long_rest(character: Character):
        """Repos long - restaure HP et sorts"""
        character.hit_points = character.max_hit_points
        character.spell_slots_current = CharacterExtensions.init_spell_slots(character)


class Potion:
    """
    Potion - seule classe qui n'existe pas dans dnd-5e-core
    Pourrait être ajoutée à Equipment mais gardons-la simple
    """

    def __init__(self, name: str, description: str, value: int,
                 effect_type: str, effect_value: str, weight: float = 0.1):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight
        self.effect_type = effect_type  # healing, mana, buff, etc.
        self.effect_value = effect_value  # "2d4+2"

    def use(self) -> int:
        """Utiliser la potion et retourner valeur effet"""
        import random

        if '+' in self.effect_value:
            dice, bonus = self.effect_value.split('+')
            num, sides = map(int, dice.split('d'))
            return sum(random.randint(1, sides) for _ in range(num)) + int(bonus)
        elif 'd' in self.effect_value:
            num, sides = map(int, self.effect_value.split('d'))
            return sum(random.randint(1, sides) for _ in range(num))
        else:
            return int(self.effect_value)

    def __str__(self):
        return f"{self.name} ({self.value} po)"


# Exports pour compatibilité
__all__ = ['CharacterExtensions', 'Potion', 'Weapon', 'Armor', 'Spell', 'Character', 'Monster']

