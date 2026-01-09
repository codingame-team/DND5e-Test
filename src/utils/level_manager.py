"""Système de progression et montée de niveau"""
from typing import Dict, List
from dnd_5e_core import Character


class LevelUpManager:
    """Gestionnaire de montée de niveau"""

    XP_TABLE = {1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500}
    HP_PER_LEVEL = {'fighter': 10, 'cleric': 8, 'wizard': 6, 'rogue': 8}

    @classmethod
    def can_level_up(cls, character: Character) -> bool:
        """Vérifier si montée de niveau possible"""
        next_level = character.level + 1
        if next_level > 5:
            return False
        required_xp = cls.XP_TABLE.get(next_level, 999999)
        return character.xp >= required_xp

    @classmethod
    def level_up(cls, character: Character) -> bool:
        """Monter d'un niveau"""
        if not cls.can_level_up(character):
            return False
        character.level += 1
        class_name = character.class_type.index if character.class_type else 'fighter'
        hit_die = cls.HP_PER_LEVEL.get(class_name, 8)
        con_mod = (character.abilities.con - 10) // 2
        hp_gain = (hit_die // 2 + 1) + con_mod
        character.max_hit_points += hp_gain
        character.hit_points = character.max_hit_points
        return True

    @classmethod
    def get_level_up_summary(cls, character: Character, old_level: int, new_level: int) -> str:
        """Résumé montée de niveau"""
        lines = ["=" * 60, f"  ⭐ {character.name} - NIVEAU {old_level} → {new_level}!",
                 f"  ❤️  HP Max: {character.max_hit_points}", "=" * 60]
        return '\n'.join(lines)


class VillageRestManager:
    """Gestionnaire repos au village"""

    @staticmethod
    def rest_at_village(party: List[Character], inn_cost: int = 5) -> Dict:
        """Repos auberge"""
        results = {'healed': [], 'leveled_up': [], 'cost': inn_cost * len(party), 'success': True}
        for char in party:
            if char.hit_points < char.max_hit_points:
                char.hit_points = char.max_hit_points
                results['healed'].append(char.name)
            if LevelUpManager.can_level_up(char):
                old_level = char.level
                if LevelUpManager.level_up(char):
                    results['leveled_up'].append({'name': char.name, 'old_level': old_level, 'new_level': char.level})
        return results

