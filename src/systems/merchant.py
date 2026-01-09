"""
Merchant system for buying and selling items
"""

from typing import Dict, List, Optional, Tuple
from ..core.adapters import CharacterExtensions


class Item:
    """Base item class"""
    def __init__(self, name: str, description: str, value: int, weight: float = 0.0):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight

    def __str__(self):
        return f"{self.name} ({self.value} po)"


class Weapon(Item):
    """Weapon item"""
    def __init__(self, name: str, description: str, value: int, damage_dice: str,
                 damage_type: str, weight: float = 0.0, attack_bonus: int = 0):
        super().__init__(name, description, value, weight)
        self.damage_dice = damage_dice
        self.damage_type = damage_type
        self.attack_bonus = attack_bonus


class Armor(Item):
    """Armor item"""
    def __init__(self, name: str, description: str, value: int, armor_class: int,
                 armor_type: str, weight: float = 0.0, stealth_disadvantage: bool = False):
        super().__init__(name, description, value, weight)
        self.armor_class = armor_class
        self.armor_type = armor_type
        self.stealth_disadvantage = stealth_disadvantage


class Potion(Item):
    """Potion item"""
    def __init__(self, name: str, description: str, value: int, effect_type: str,
                 effect_value: str, weight: float = 0.1):
        super().__init__(name, description, value, weight)
        self.effect_type = effect_type
        self.effect_value = effect_value


class MerchantStock:
    """Represents merchant's inventory"""

    def __init__(self, name: str):
        self.name = name
        self.items: Dict[str, tuple[Item, int, int]] = {}  # item_id: (item, quantity, price)

    def add_item(self, item_id: str, item: Item, quantity: int, price: Optional[int] = None):
        """Add item to stock"""
        if price is None:
            price = item.value
        self.items[item_id] = (item, quantity, price)

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if item is in stock"""
        if item_id in self.items:
            _, stock_qty, _ = self.items[item_id]
            return stock_qty >= quantity
        return False

    def get_item(self, item_id: str) -> Optional[tuple[Item, int, int]]:
        """Get item info"""
        return self.items.get(item_id)

    def remove_quantity(self, item_id: str, quantity: int = 1) -> bool:
        """Remove quantity from stock"""
        if self.has_item(item_id, quantity):
            item, stock_qty, price = self.items[item_id]
            new_qty = stock_qty - quantity
            if new_qty <= 0:
                del self.items[item_id]
            else:
                self.items[item_id] = (item, new_qty, price)
            return True
        return False

    def add_quantity(self, item_id: str, quantity: int = 1):
        """Add quantity to stock"""
        if item_id in self.items:
            item, stock_qty, price = self.items[item_id]
            self.items[item_id] = (item, stock_qty + quantity, price)


class MerchantSystem:
    """Manages trading between characters and merchants"""

    # Predefined merchant stocks
    MERCHANTS: Dict[str, MerchantStock] = {}

    @classmethod
    def create_village_merchant(cls, weapons=None, armors=None) -> MerchantStock:
        """Create default village merchant with weapons and armors from game"""
        merchant = MerchantStock("Boutique du Village")

        # Potions
        merchant.add_item("potion_healing",
            Potion(name="Potion de Soin", description="Restaure 2d4+2 HP", value=50,
                   effect_type="healing", effect_value="2d4+2"),
            quantity=5, price=50)

        merchant.add_item("potion_greater_healing",
            Potion(name="Potion de Soin Supérieure", description="Restaure 4d4+4 HP", value=100,
                   effect_type="healing", effect_value="4d4+4"),
            quantity=2, price=100)

        merchant.add_item("potion_mana",
            Potion(name="Potion de Mana", description="Restaure 1 emplacement de sort niveau 1", value=60,
                   effect_type="mana", effect_value="1"),
            quantity=3, price=60)

        # 🔧 CORRECTION: Toujours utiliser le fallback pour avoir des armes/armures fonctionnelles
        # Les objets WeaponData/ArmorData de populate_functions ne sont pas compatibles
        # avec le système de marchand, donc on utilise des armes/armures créées manuellement

        weapons_added = 0
        armors_added = 0

        # Essayer d'utiliser les armes chargées (si compatibles)
        if weapons and len(weapons) > 0:
            for i, weapon in enumerate(weapons[:10]):
                try:
                    # Vérifier si c'est un objet WeaponData ou Weapon compatible
                    if hasattr(weapon, 'name') and hasattr(weapon, 'damage'):
                        # Extraire les infos de manière sûre
                        name = weapon.name
                        damage_dice = '1d6'  # Par défaut
                        damage_type = 'slashing'  # Par défaut
                        cost = 10  # Par défaut

                        # Essayer d'extraire les vraies valeurs
                        if hasattr(weapon, 'damage') and isinstance(weapon.damage, dict):
                            damage_dice = weapon.damage.get('damage_dice', '1d6')
                            if 'damage_type' in weapon.damage and isinstance(weapon.damage['damage_type'], dict):
                                damage_type = weapon.damage['damage_type'].get('name', 'slashing')

                        if hasattr(weapon, 'cost') and isinstance(weapon.cost, dict):
                            cost = weapon.cost.get('quantity', 10)

                        merchant.add_item(f"weapon_{i}",
                            Weapon(name=name, description=f"Arme: {damage_dice} {damage_type}",
                                   value=cost, damage_dice=damage_dice, damage_type=damage_type),
                            quantity=2, price=cost)
                        weapons_added += 1
                except Exception as e:
                    pass  # Skip weapons with issues

        # Si aucune arme n'a été ajoutée, utiliser le fallback
        if weapons_added == 0:
            # Fallback: armes basiques
            merchant.add_item("dagger",
                Weapon(name="Dague", description="Arme légère de mêlée", value=2,
                       damage_dice="1d4", damage_type="piercing"),
                quantity=10, price=2)

            merchant.add_item("shortsword",
                Weapon(name="Épée Courte", description="Arme de mêlée polyvalente", value=10,
                       damage_dice="1d6", damage_type="piercing"),
                quantity=3, price=10)

            merchant.add_item("longsword",
                Weapon(name="Épée Longue", description="Arme de mêlée versatile", value=15,
                       damage_dice="1d8", damage_type="slashing"),
                quantity=2, price=15)

            merchant.add_item("greatsword",
                Weapon(name="Grande Épée", description="Arme à deux mains puissante", value=50,
                       damage_dice="2d6", damage_type="slashing"),
                quantity=1, price=50)

            merchant.add_item("longbow",
                Weapon(name="Arc Long", description="Arme à distance", value=50,
                       damage_dice="1d8", damage_type="piercing"),
                quantity=2, price=50)

        # Essayer d'utiliser les armures chargées (si compatibles)
        if armors and len(armors) > 0:
            for i, armor in enumerate(armors[:8]):
                try:
                    if hasattr(armor, 'name') and hasattr(armor, 'armor_class'):
                        name = armor.name
                        ac_base = 11  # Par défaut
                        armor_type = 'light'  # Par défaut
                        cost = 10  # Par défaut

                        # Extraire AC
                        if isinstance(armor.armor_class, dict):
                            ac_base = armor.armor_class.get('base', 11)
                        elif isinstance(armor.armor_class, int):
                            ac_base = armor.armor_class

                        # Extraire type
                        if hasattr(armor, 'armor_category'):
                            armor_type = armor.armor_category

                        # Extraire coût
                        if hasattr(armor, 'cost') and isinstance(armor.cost, dict):
                            cost = armor.cost.get('quantity', 10)

                        merchant.add_item(f"armor_{i}",
                            Armor(name=name, description=f"AC {ac_base} - {armor_type}",
                                  value=cost, armor_class=ac_base, armor_type=armor_type),
                            quantity=1, price=cost)
                        armors_added += 1
                except Exception:
                    pass

        # Si aucune armure n'a été ajoutée, utiliser le fallback
        if armors_added == 0:
            # Fallback: armures basiques
            merchant.add_item("leather_armor",
                Armor(name="Armure de Cuir", description="Armure légère AC 11", value=10,
                      armor_class=11, armor_type="light"),
                quantity=2, price=10)

            merchant.add_item("chain_mail",
                Armor(name="Cotte de Mailles", description="Armure moyenne AC 16", value=75,
                      armor_class=16, armor_type="medium"),
                quantity=1, price=75)

            merchant.add_item("plate_armor",
                Armor(name="Armure de Plaques", description="Armure lourde AC 18", value=1500,
                      armor_class=18, armor_type="heavy"),
                quantity=1, price=1500)

            merchant.add_item("shield",
                Armor(name="Bouclier", description="+2 AC", value=10,
                      armor_class=2, armor_type="shield"),
                quantity=3, price=10)

        cls.MERCHANTS["village"] = merchant
        cls.MERCHANTS["desert_merchant"] = merchant  # Réutiliser pour le désert
        return merchant

    @classmethod
    def get_merchant(cls, merchant_id: str, weapons=None, armors=None) -> Optional[MerchantStock]:
        """Get merchant by ID"""
        # Si weapons ou armors sont fournis, recréer le marchand
        if merchant_id in ["village", "desert_merchant"]:
            if weapons is not None or armors is not None:
                # Recréer avec les nouvelles armes/armures
                return cls.create_village_merchant(weapons, armors)
            elif merchant_id not in cls.MERCHANTS:
                # Créer pour la première fois
                return cls.create_village_merchant(None, None)

        return cls.MERCHANTS.get(merchant_id)

    def __init__(self):
        self.transaction_log: List[Dict] = []

    def buy_item(self, character, merchant: MerchantStock, item_id: str,
                 quantity: int = 1) -> bool:
        """Character buys item from merchant"""
        if not merchant.has_item(item_id, quantity):
            return False

        item, stock_qty, price = merchant.get_item(item_id)
        total_cost = price * quantity

        # Check if character has enough gold
        if character.gold < total_cost:
            return False

        # Process transaction
        character.gold -= total_cost
        merchant.remove_quantity(item_id, quantity)

        # Add items to character using CharacterExtensions
        for _ in range(quantity):
            # Create new instance of item
            if isinstance(item, Potion):
                new_item = Potion(name=item.name, description=item.description, value=item.value,
                                effect_type=item.effect_type, effect_value=item.effect_value)
            elif isinstance(item, Weapon):
                new_item = Weapon(name=item.name, description=item.description, value=item.value,
                                damage_dice=item.damage_dice, damage_type=item.damage_type,
                                attack_bonus=item.attack_bonus)
            elif isinstance(item, Armor):
                new_item = Armor(name=item.name, description=item.description, value=item.value,
                               armor_class=item.armor_class, armor_type=item.armor_type)
            else:
                new_item = Item(item.name, item.description, item.value)

            # Use CharacterExtensions.add_item instead of character.add_item
            CharacterExtensions.add_item(character, new_item)

        # Log transaction
        self.transaction_log.append({
            'type': 'buy',
            'character': character.name,
            'merchant': merchant.name,
            'item': item.name,
            'quantity': quantity,
            'cost': total_cost
        })

        return True

    def sell_item(self, character, merchant: MerchantStock, item: Item) -> bool:
        """Character sells item to merchant"""
        # Check if character has item
        if not hasattr(character, 'inventory_items'):
            return False

        if item not in character.inventory_items:
            return False

        # Sell for 50% of value
        sell_price = item.value // 2

        # Process transaction
        CharacterExtensions.remove_item(character, item)
        character.gold += sell_price

        # Add to merchant stock (optional, simplified)
        # merchant.add_quantity(item_id, 1)

        # Log transaction
        self.transaction_log.append({
            'type': 'sell',
            'character': character.name,
            'merchant': merchant.name,
            'item': item.name,
            'profit': sell_price
        })

        return True

    def display_shop(self, merchant: MerchantStock, character) -> str:
        """Format shop display"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"  🛒 {merchant.name}")
        lines.append(f"{'='*60}")
        lines.append(f"💰 Votre or: {character.gold} po\n")

        if not merchant.items:
            lines.append("  Le marchand n'a rien à vendre pour le moment.")
        else:
            lines.append("  Articles disponibles:\n")
            for i, (item_id, (item, qty, price)) in enumerate(merchant.items.items(), 1):
                stock_str = f"({qty} en stock)" if qty < 10 else ""
                lines.append(f"  {i}. {item.name} - {price} po {stock_str}")
                lines.append(f"      {item.description}")

        lines.append(f"\n{'='*60}\n")
        return "\n".join(lines)

    def get_buyable_items(self, merchant: MerchantStock) -> List[Tuple[str, Item, int, int]]:
        """Get list of items character can interact with"""
        result = []
        for item_id, (item, qty, price) in merchant.items.items():
            result.append((item_id, item, qty, price))
        return result

