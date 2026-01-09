"""
Inventory management system
"""

from typing import List, Optional, Dict, Type
from .entities import Item, Weapon, Armor, Potion


class Inventory:
    """Manages character inventory with weight and capacity"""

    def __init__(self, max_weight: float = 150.0, max_gold: int = 9999):
        self.items: List[Item] = []
        self.gold: int = 0
        self.max_weight = max_weight
        self.max_gold = max_gold

    def add_item(self, item: Item) -> bool:
        """Add item if weight allows"""
        if self.current_weight() + item.weight <= self.max_weight:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item: Item) -> bool:
        """Remove item from inventory"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def add_gold(self, amount: int) -> bool:
        """Add gold if capacity allows"""
        if self.gold + amount <= self.max_gold:
            self.gold += amount
            return True
        return False

    def remove_gold(self, amount: int) -> bool:
        """Remove gold if available"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def current_weight(self) -> float:
        """Calculate total weight"""
        return sum(item.weight for item in self.items)

    def get_items_by_type(self, item_type: Type) -> List[Item]:
        """Get all items of a specific type"""
        return [item for item in self.items if isinstance(item, item_type)]

    def get_weapons(self) -> List[Weapon]:
        """Get all weapons"""
        return self.get_items_by_type(Weapon)

    def get_armors(self) -> List[Armor]:
        """Get all armors"""
        return self.get_items_by_type(Armor)

    def get_potions(self) -> List[Potion]:
        """Get all potions"""
        return self.get_items_by_type(Potion)

    def find_item(self, name: str) -> Optional[Item]:
        """Find item by name"""
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

    def __str__(self) -> str:
        lines = [f"💰 Or: {self.gold} po"]
        lines.append(f"⚖️ Poids: {self.current_weight():.1f}/{self.max_weight} lbs")

        if self.items:
            lines.append("\n📦 Objets:")
            for item in self.items:
                lines.append(f"  - {item}")
        else:
            lines.append("\n📦 Inventaire vide")

        return "\n".join(lines)

