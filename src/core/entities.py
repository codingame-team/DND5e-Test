"""
Enhanced game entities with equipment, inventory, and spells support
Extends dnd-5e-core entities with game-specific functionality
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from dnd_5e_core import Character, Monster
from dnd_5e_core.equipment import Weapon as DndWeapon, Armor as DndArmor


class Item:
    """Base class for all items"""
    def __init__(self, name: str, description: str, value: int, weight: float = 0.0):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.name} ({self.value} po)"


class Weapon(Item):
    """Weapon with combat stats"""
    def __init__(self, name: str, description: str, value: int, damage_dice: str,
                 damage_type: str, weight: float = 0.0, attack_bonus: int = 0,
                 properties: Optional[List[str]] = None):
        super().__init__(name, description, value, weight)
        self.damage_dice = damage_dice
        self.damage_type = damage_type
        self.attack_bonus = attack_bonus
        self.properties = properties or []

    @classmethod
    def from_dnd_weapon(cls, weapon: DndWeapon, value: int = 10) -> 'Weapon':
        """Create Weapon from dnd-5e-core Weapon"""
        return cls(
            name=weapon.name,
            description=weapon.desc or "",
            value=value,
            weight=weapon.weight if hasattr(weapon, 'weight') else 0.0,
            damage_dice=f"{weapon.damage.damage_dice}",
            damage_type=weapon.damage.damage_type.name if weapon.damage else "bludgeoning",
            attack_bonus=0,
            properties=[]
        )


class Armor(Item):
    """Armor with defense stats"""
    def __init__(self, name: str, description: str, value: int, armor_class: int,
                 armor_type: str, weight: float = 0.0, stealth_disadvantage: bool = False):
        super().__init__(name, description, value, weight)
        self.armor_class = armor_class
        self.armor_type = armor_type
        self.stealth_disadvantage = stealth_disadvantage

    @classmethod
    def from_dnd_armor(cls, armor: DndArmor, value: int = 10) -> 'Armor':
        """Create Armor from dnd-5e-core Armor"""
        return cls(
            name=armor.name,
            description=armor.desc or "",
            value=value,
            weight=armor.weight if hasattr(armor, 'weight') else 0.0,
            armor_class=armor.armor_class.base,
            armor_type=armor.armor_category,
            stealth_disadvantage=armor.stealth_disadvantage
        )


class Potion(Item):
    """Consumable potion"""
    def __init__(self, name: str, description: str, value: int, effect_type: str, effect_value: str,
                 weight: float = 0.0):
        super().__init__(name, description, value, weight)
        self.effect_type = effect_type
        self.effect_value = effect_value

    def use(self) -> int:
        """Use the potion and return effect value"""
        import random
        if '+' in self.effect_value:
            dice, bonus = self.effect_value.split('+')
            num, sides = map(int, dice.split('d'))
            return sum(random.randint(1, int(sides)) for _ in range(int(num))) + int(bonus)
        elif 'd' in self.effect_value:
            num, sides = map(int, self.effect_value.split('d'))
            return sum(random.randint(1, int(sides)) for _ in range(int(num)))
        else:
            return int(self.effect_value)


class GameCharacter(Character):
    """
    Enhanced Character with equipment, inventory, and spell management
    Extends dnd-5e-core Character
    """

    def __init__(self, *args, **kwargs):
        # Extract custom fields before passing to parent
        self.equipped_weapon: Optional[Weapon] = kwargs.pop('equipped_weapon', None)
        self.equipped_armor: Optional[Armor] = kwargs.pop('equipped_armor', None)
        self.inventory_items: List[Item] = kwargs.pop('inventory_items', [])
        self.spell_slots_current: Dict[int, int] = kwargs.pop('spell_slots_current', {})
        self.prepared_spells: List[str] = kwargs.pop('prepared_spells', [])

        super().__init__(*args, **kwargs)

        # Initialize spell slots if caster
        if self.class_type.can_cast and not self.spell_slots_current:
            self.spell_slots_current = self._init_spell_slots()

    def _init_spell_slots(self) -> Dict[int, int]:
        """Initialize spell slots based on class and level"""
        # Simplified: level 3 casters get 4/2 slots for level 1/2
        if self.level >= 3:
            return {1: 4, 2: 2}
        elif self.level >= 2:
            return {1: 3}
        else:
            return {1: 2}

    def equip_weapon(self, weapon: Weapon):
        """Equip a weapon"""
        if self.equipped_weapon:
            self.inventory_items.append(self.equipped_weapon)
        self.equipped_weapon = weapon
        if weapon in self.inventory_items:
            self.inventory_items.remove(weapon)

    def equip_armor(self, armor: Armor):
        """Equip armor"""
        if self.equipped_armor:
            self.inventory_items.append(self.equipped_armor)
        self.equipped_armor = armor
        if armor in self.inventory_items:
            self.inventory_items.remove(armor)
        # Update AC
        self.armor_class = armor.armor_class

    def add_item(self, item: Item):
        """Add item to inventory"""
        self.inventory_items.append(item)

    def remove_item(self, item: Item) -> bool:
        """Remove item from inventory"""
        if item in self.inventory_items:
            self.inventory_items.remove(item)
            return True
        return False

    def use_potion(self, potion: Potion) -> int:
        """Use a potion from inventory"""
        if potion in self.inventory_items:
            effect = potion.use()
            self.remove_item(potion)

            # Apply effect
            if potion.effect_type == "healing":
                old_hp = self.hit_points
                self.hit_points = min(self.hit_points + effect, self.max_hit_points)
                return self.hit_points - old_hp

            return effect
        return 0

    def can_cast_spell(self, spell_level: int) -> bool:
        """Check if character has spell slot available"""
        return self.spell_slots_current.get(spell_level, 0) > 0

    def cast_spell(self, spell_level: int) -> bool:
        """Use a spell slot"""
        if self.can_cast_spell(spell_level):
            self.spell_slots_current[spell_level] -= 1
            return True
        return False

    def rest_long(self):
        """Long rest - restore HP and spell slots"""
        self.hit_points = self.max_hit_points
        self.spell_slots_current = self._init_spell_slots()

    def rest_short(self):
        """Short rest - restore some HP"""
        # Restore 1 hit die worth of HP
        import random
        heal = random.randint(1, self.class_type.hit_die) + self.abilities.con // 2 - 5
        self.hit_points = min(self.hit_points + max(1, heal), self.max_hit_points)

    def get_attack_bonus(self) -> int:
        """Calculate attack bonus including weapon"""
        base_bonus = self.abilities.str // 2 - 5  # Simplified modifier
        weapon_bonus = self.equipped_weapon.attack_bonus if self.equipped_weapon else 0
        return base_bonus + weapon_bonus + self.level // 2  # Proficiency

    def get_damage_dice(self) -> str:
        """Get damage dice from equipped weapon or unarmed"""
        if self.equipped_weapon:
            return self.equipped_weapon.damage_dice
        return "1+0"  # Unarmed strike

    def __str__(self) -> str:
        parts = [f"{self.name} ({self.class_type.name} {self.level})"]
        parts.append(f"HP: {self.hit_points}/{self.max_hit_points}")
        parts.append(f"CA: {self.armor_class}")

        if self.equipped_weapon:
            parts.append(f"Arme: {self.equipped_weapon.name}")
        if self.equipped_armor:
            parts.append(f"Armure: {self.equipped_armor.name}")

        if self.class_type.can_cast:
            slots_str = ", ".join(f"N{lvl}:{count}" for lvl, count in sorted(self.spell_slots_current.items()))
            parts.append(f"Sorts: {slots_str}")

        return " | ".join(parts)


class GameMonster(Monster):
    """
    Enhanced Monster with loot drops
    Extends dnd-5e-core Monster
    """

    def __init__(self, *args, **kwargs):
        self.loot_table: List[Item] = kwargs.pop('loot_table', [])
        super().__init__(*args, **kwargs)

    def get_loot(self) -> List[Item]:
        """Get loot drops when defeated"""
        import random
        # 50% chance to drop each item
        return [item for item in self.loot_table if random.random() > 0.5]

