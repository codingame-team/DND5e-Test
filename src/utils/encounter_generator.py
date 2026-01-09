"""
Générateur de rencontres aléatoires depuis tables PDF
"""
import random
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class EncounterTable:
    """Table de rencontres aléatoires"""
    name: str
    die_type: str  # "1d6", "1d20", etc.
    entries: List[Dict]  # [{'roll': '1-2', 'encounter': {...}}]


class RandomEncounterGenerator:
    """Génère des rencontres aléatoires"""

    def __init__(self, encounter_data: List[Dict]):
        """
        Args:
            encounter_data: Données extraites du PDF
        """
        self.tables = self._build_tables(encounter_data)

    def _build_tables(self, data: List[Dict]) -> List[EncounterTable]:
        """Construire tables depuis données"""
        # Grouper par type/zone
        tables = []

        # Pour l'instant, une seule table globale
        if data:
            entries = []
            for enc in data:
                entries.append({
                    'roll': enc['roll'],
                    'count': enc.get('count', '1'),
                    'monster_type': enc.get('monster_type', enc['description']),
                    'description': enc['description']
                })

            table = EncounterTable(
                name="Random Encounters",
                die_type="1d6",
                entries=entries
            )
            tables.append(table)

        return tables

    def roll_encounter(self, table_name: str = None) -> Optional[Dict]:
        """
        Lancer une rencontre aléatoire

        Returns:
            Dict avec détails de la rencontre ou None
        """
        if not self.tables:
            return None

        # Utiliser première table si pas de nom spécifié
        table = self.tables[0]

        if table_name:
            table = next((t for t in self.tables if t.name == table_name), self.tables[0])

        # Lancer le dé
        roll = self._roll_dice(table.die_type)

        # Trouver l'entrée correspondante
        for entry in table.entries:
            if self._matches_roll(roll, entry['roll']):
                return {
                    'rolled': roll,
                    'encounter': entry,
                    'table': table.name
                }

        return None

    def _roll_dice(self, die_spec: str) -> int:
        """Lancer un dé (ex: "1d6" -> 1-6)"""
        match = die_spec.split('d')
        if len(match) == 2:
            count = int(match[0])
            sides = int(match[1])
            return sum(random.randint(1, sides) for _ in range(count))
        return 1

    def _matches_roll(self, roll: int, roll_spec: str) -> bool:
        """Vérifier si le jet correspond au spec (ex: "1-2", "3", "4-6")"""
        if '-' in roll_spec:
            # Range: "1-2"
            low, high = map(int, roll_spec.split('-'))
            return low <= roll <= high
        else:
            # Valeur exacte: "3"
            try:
                return roll == int(roll_spec)
            except:
                return False

    def get_all_possible_encounters(self) -> List[Dict]:
        """Obtenir toutes les rencontres possibles"""
        all_encounters = []
        for table in self.tables:
            for entry in table.entries:
                all_encounters.append({
                    'table': table.name,
                    'roll_spec': entry['roll'],
                    'encounter': entry
                })
        return all_encounters


class EncounterDifficultyCalculator:
    """Calcule la difficulté d'une rencontre"""

    # XP par CR (D&D 5e)
    XP_BY_CR = {
        0: 10,
        0.125: 25,
        0.25: 50,
        0.5: 100,
        1: 200,
        2: 450,
        3: 700,
        4: 1100,
        5: 1800,
    }

    # Seuils XP par niveau de joueur
    THRESHOLDS = {
        1: {'easy': 25, 'medium': 50, 'hard': 75, 'deadly': 100},
        2: {'easy': 50, 'medium': 100, 'hard': 150, 'deadly': 200},
        3: {'easy': 75, 'medium': 150, 'hard': 225, 'deadly': 400},
        4: {'easy': 125, 'medium': 250, 'hard': 375, 'deadly': 500},
        5: {'easy': 250, 'medium': 500, 'hard': 750, 'deadly': 1100},
    }

    @classmethod
    def calculate_difficulty(cls, party_levels: List[int], monsters_cr: List[float]) -> Dict:
        """
        Calculer la difficulté d'une rencontre

        Args:
            party_levels: Niveaux des PJs
            monsters_cr: CRs des monstres

        Returns:
            Dict avec difficulté et détails
        """
        # XP total des monstres
        monster_xp = sum(cls.XP_BY_CR.get(cr, 0) for cr in monsters_cr)

        # Multiplicateur selon nombre de monstres
        multiplier = cls._get_multiplier(len(monsters_cr), len(party_levels))
        adjusted_xp = int(monster_xp * multiplier)

        # Seuils du groupe
        party_thresholds = {
            'easy': sum(cls.THRESHOLDS.get(lvl, cls.THRESHOLDS[1])['easy'] for lvl in party_levels),
            'medium': sum(cls.THRESHOLDS.get(lvl, cls.THRESHOLDS[1])['medium'] for lvl in party_levels),
            'hard': sum(cls.THRESHOLDS.get(lvl, cls.THRESHOLDS[1])['hard'] for lvl in party_levels),
            'deadly': sum(cls.THRESHOLDS.get(lvl, cls.THRESHOLDS[1])['deadly'] for lvl in party_levels),
        }

        # Déterminer difficulté
        if adjusted_xp < party_thresholds['easy']:
            difficulty = 'trivial'
        elif adjusted_xp < party_thresholds['medium']:
            difficulty = 'easy'
        elif adjusted_xp < party_thresholds['hard']:
            difficulty = 'medium'
        elif adjusted_xp < party_thresholds['deadly']:
            difficulty = 'hard'
        else:
            difficulty = 'deadly'

        return {
            'difficulty': difficulty,
            'monster_xp': monster_xp,
            'adjusted_xp': adjusted_xp,
            'multiplier': multiplier,
            'thresholds': party_thresholds
        }

    @staticmethod
    def _get_multiplier(num_monsters: int, num_players: int) -> float:
        """Multiplicateur selon nombre de monstres"""
        if num_monsters == 1:
            return 1.0
        elif num_monsters == 2:
            return 1.5
        elif num_monsters <= 6:
            return 2.0
        elif num_monsters <= 10:
            return 2.5
        elif num_monsters <= 14:
            return 3.0
        else:
            return 4.0

