"""
Factory pour créer des monstres depuis JSON
"""
from typing import Dict, Optional
from dnd_5e_core import Monster, Abilities
from dnd_5e_core.combat import Action, ActionType, Damage
from dnd_5e_core.mechanics import DamageDice
from dnd_5e_core.equipment import DamageType


class MonsterFactory:
    """Factory pour créer monstres depuis données JSON"""

    def __init__(self, monsters_data: Dict):
        """
        Args:
            monsters_data: Dict chargé depuis all_monsters.json
        """
        self.monsters_data = monsters_data

    def create_monster(self, monster_id: str, name: Optional[str] = None) -> Optional[Monster]:
        """
        Créer un monstre depuis son ID

        Args:
            monster_id: ID du monstre (ex: "goblin", "snake_king")
            name: Nom personnalisé (optionnel)

        Returns:
            Monster ou None si non trouvé
        """
        if monster_id not in self.monsters_data:
            print(f"⚠️ Monstre non trouvé: {monster_id}")
            return None

        data = self.monsters_data[monster_id]

        # Nom
        monster_name = name if name else data['name']

        # Abilities
        abilities = Abilities(
            str=data['abilities']['str'],
            dex=data['abilities']['dex'],
            con=data['abilities']['con'],
            int=data['abilities']['int'],
            wis=data['abilities']['wis'],
            cha=data['abilities']['cha']
        )

        # Actions
        actions = []
        for action_data in data.get('actions', []):
            # Type de dégâts
            damage_type = DamageType(
                index=action_data['damage_type'],
                name=action_data['damage_type'].capitalize(),
                desc=f"{action_data['damage_type']} damage"
            )

            # Dégâts principaux
            damages = [Damage(
                type=damage_type,
                dd=DamageDice(action_data['damage'])
            )]

            # Dégâts additionnels (ex: nécrotique)
            if 'additional_damage' in action_data:
                add_type = DamageType(
                    index=action_data['additional_damage_type'],
                    name=action_data['additional_damage_type'].capitalize(),
                    desc=f"{action_data['additional_damage_type']} damage"
                )
                damages.append(Damage(
                    type=add_type,
                    dd=DamageDice(action_data['additional_damage'])
                ))

            # Type d'action
            action_type = ActionType.MELEE if action_data['type'] == 'melee' else ActionType.RANGED

            action = Action(
                name=action_data['name'],
                desc=action_data.get('desc', action_data['name']),
                type=action_type,
                attack_bonus=action_data['attack_bonus'],
                damages=damages,
                normal_range=action_data['range']
            )
            actions.append(action)

        # Créer le monstre
        monster = Monster(
            index=data['index'],
            name=monster_name,
            abilities=abilities,
            proficiencies=[],
            armor_class=data['armor_class'],
            hit_points=data['hit_points'],
            hit_dice=data['hit_dice'],
            xp=data['xp'],
            speed=data['speed'],
            challenge_rating=data['challenge_rating'],
            actions=actions
        )

        return monster

    def create_monsters(self, monster_ids: list) -> list:
        """
        Créer plusieurs monstres

        Args:
            monster_ids: Liste d'IDs (peut inclure tuples (id, name))

        Returns:
            Liste de Monster
        """
        monsters = []

        for item in monster_ids:
            if isinstance(item, tuple):
                monster_id, name = item
                monster = self.create_monster(monster_id, name)
            else:
                monster = self.create_monster(item)

            if monster:
                monsters.append(monster)

        return monsters

