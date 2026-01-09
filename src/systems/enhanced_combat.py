"""
Enhanced Combat System - Améliore le CombatSystem de dnd-5e-core
Pour gérer les personnages sans méthode attack()
"""

from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.mechanics import DamageDice
from typing import List, Optional
from random import randint


class EnhancedCombatSystem(CombatSystem):
    """
    Système de combat amélioré qui calcule les dommages correctement
    même pour les personnages qui n'ont pas de méthode attack()
    """

    def character_turn(self,
                      character,
                      alive_chars: List,
                      alive_monsters: List,
                      party: List,
                      weapons: Optional[List] = None,
                      armors: Optional[List] = None,
                      equipments: Optional[List] = None,
                      potions: Optional[List] = None) -> None:
        """
        Tour de personnage avec calcul de dommages D&D 5e correct
        """
        if not alive_monsters:
            return

        # Même priorité de soins/potions que le parent
        # 1. Vérifier soins magiques
        healing_spells = []
        if hasattr(character, 'is_spell_caster') and character.is_spell_caster:
            if hasattr(character, 'sc') and hasattr(character.sc, 'learned_spells'):
                healing_spells = [s for s in character.sc.learned_spells
                                  if hasattr(s, 'heal_at_slot_level') and s.heal_at_slot_level
                                  and character.sc.spell_slots[s.level - 1] > 0]

        if healing_spells and any(c for c in alive_chars if c.hit_points < 0.5 * c.max_hit_points):
            # Appeler la version parente pour les soins
            super().character_turn(character, alive_chars, alive_monsters, party,
                                 weapons, armors, equipments, potions)
            return

        # 2. Potions
        if hasattr(character, 'healing_potions') and character.hit_points < 0.3 * character.max_hit_points and character.healing_potions:
            super().character_turn(character, alive_chars, alive_monsters, party,
                                 weapons, armors, equipments, potions)
            return

        # 3. ATTAQUE - Version améliorée
        monster = self._select_target_monster(character, alive_chars, alive_monsters)

        self.log_message(f"⚔️  {character.name} attaque {monster.name.title()}!")

        # Calcul de dommages D&D 5e correct (ne pas utiliser character.attack())
        damage = self._calculate_character_damage(character)

        # Jet d'attaque
        attack_roll = randint(1, 20)
        str_mod = (character.abilities.str - 10) // 2
        dex_mod = (character.abilities.dex - 10) // 2

        # Choisir STR ou DEX selon la classe
        attack_bonus = str_mod
        if hasattr(character, 'class_type') and 'rogue' in character.class_type.index.lower():
            attack_bonus = dex_mod

        attack_bonus += character.level // 4 + 2  # Bonus de maîtrise

        total_attack = attack_roll + attack_bonus

        # CA du monstre
        monster_ac = getattr(monster, 'armor_class', 12)

        if attack_roll == 1:
            self.log_message(f"❌ ÉCHEC CRITIQUE! (jet: 1)")
            return
        elif attack_roll == 20:
            damage *= 2  # Coup critique
            self.log_message(f"🎯 COUP CRITIQUE! (jet: 20)")
            self.log_message(f"💥 {character.name} inflige {damage} dommages!")
        elif total_attack >= monster_ac:
            self.log_message(f"✅ Touché! (jet: {attack_roll}+{attack_bonus}={total_attack} vs CA {monster_ac})")
            self.log_message(f"💥 {character.name} inflige {damage} dommages!")
        else:
            self.log_message(f"❌ Raté! (jet: {attack_roll}+{attack_bonus}={total_attack} vs CA {monster_ac})")
            return

        # Appliquer dommages
        monster.hit_points -= damage

        if monster.hit_points <= 0:
            if monster in alive_monsters:
                alive_monsters.remove(monster)
            self.log_message(f"💀 {monster.name.title()} est MORT!")
            self._handle_victory(character, monster, weapons, armors, equipments, potions)

    def _calculate_character_damage(self, character) -> int:
        """
        Calculer les dommages d'un personnage selon D&D 5e
        """
        # Modificateurs d'aptitudes
        str_mod = (character.abilities.str - 10) // 2
        dex_mod = (character.abilities.dex - 10) // 2

        # Déterminer l'arme et le modificateur
        damage_dice = "1d8"  # Par défaut (épée longue)
        ability_mod = str_mod

        # Ajuster selon la classe
        if hasattr(character, 'class_type'):
            class_name = character.class_type.index.lower()

            if 'fighter' in class_name or 'paladin' in class_name:
                damage_dice = "1d8"  # Épée longue
                ability_mod = str_mod
            elif 'rogue' in class_name or 'ranger' in class_name:
                damage_dice = "1d6"  # Épée courte/arc
                ability_mod = dex_mod
            elif 'cleric' in class_name:
                damage_dice = "1d6"  # Masse d'armes
                ability_mod = str_mod
            elif 'wizard' in class_name or 'sorcerer' in class_name:
                damage_dice = "1d4"  # Dague
                ability_mod = dex_mod

        # Lancer les dés de dommages
        dice_parts = damage_dice.split('d')
        num_dice = int(dice_parts[0])
        dice_size = int(dice_parts[1])

        total_damage = sum(randint(1, dice_size) for _ in range(num_dice))
        total_damage += ability_mod

        # Minimum 1 dommage
        return max(1, total_damage)

