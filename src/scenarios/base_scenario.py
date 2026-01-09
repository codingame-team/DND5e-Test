"""
Classe de base pour tous les scénarios D&D 5e
Factorisation du code commun entre scénarios
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dnd_5e_core import Character, Monster
from dnd_5e_core.combat import CombatSystem

from ..utils.pdf_reader import PDFScenarioReader
from ..utils.save_manager import SaveGameManager, JSONLoader
from ..utils.exploration_map import ExplorationMap
from ..utils.level_manager import LevelUpManager, VillageRestManager
from ..utils.monster_factory import MonsterFactory
from ..scenes.scene_system import SceneManager
from ..rendering.renderer import create_renderer, Renderer
from ..systems.spellcasting_v2 import SpellcastingManager
from ..systems.merchant import MerchantSystem


class BaseScenario(ABC):
    """
    Classe de base abstraite pour tous les scénarios
    Fournit les fonctionnalités communes
    """

    def __init__(self, pdf_path: str, use_ncurses: bool = False):
        """
        Initialiser le scénario

        Args:
            pdf_path: Chemin vers le PDF du scénario
            use_ncurses: Utiliser interface ncurses ou console
        """
        self.pdf_path = pdf_path

        # Systèmes de jeu
        self.renderer = create_renderer(use_ncurses)
        # 🔧 Utiliser EnhancedCombatSystem pour calculer correctement les dommages
        from ..systems.enhanced_combat import EnhancedCombatSystem
        self.combat_system = EnhancedCombatSystem(verbose=True)
        self.spellcasting = SpellcastingManager()
        self.merchant_system = MerchantSystem()
        self.scene_manager = SceneManager()

        # 🆕 Nouveaux systèmes
        self.save_manager = SaveGameManager()
        self.json_loader = JSONLoader()
        self.exploration_map: Optional[ExplorationMap] = None
        self.level_manager = LevelUpManager()
        self.village_rest = VillageRestManager()

        # 🆕 Monster factory depuis JSON
        monsters_data = self.json_loader.load_monsters()
        self.monster_factory = MonsterFactory(monsters_data)

        # Données du scénario
        self.scenario_data: Optional[Dict] = None
        self.party: List[Character] = []

        # État du jeu
        self.game_state = self._init_game_state()

    def _init_game_state(self) -> Dict:
        """Initialiser l'état du jeu (peut être surchargé)"""
        return {
            'combat_victories': 0,
            'total_xp': 0,
            'gold': 0,
            'gold_spent': 0,
            'locations_visited': 0,
            'npcs_met': 0,
            'quests_completed': 0,
            'deaths': 0,
        }

    @abstractmethod
    def get_scenario_name(self) -> str:
        """Retourner le nom du scénario"""
        pass

    @abstractmethod
    def create_party(self) -> List[Character]:
        """Créer le groupe de personnages spécifique au scénario"""
        pass

    @abstractmethod
    def build_custom_scenes(self):
        """
        Construire les scènes personnalisées du scénario
        Cette méthode doit ajouter les scènes au scene_manager
        """
        pass

    def load_scenario_from_pdf(self):
        """Charger et analyser le PDF du scénario"""
        self.renderer.print_header(f"📖 CHARGEMENT: {self.get_scenario_name()}")

        print(f"Lecture du PDF...")

        try:
            with PDFScenarioReader(self.pdf_path) as reader:
                self.scenario_data = {
                    'title': reader.pdf_path.stem,
                    'sections': reader.extract_sections(),
                    'locations': reader.extract_locations(),
                    'npcs': reader.extract_npcs(),
                    'encounters': reader.extract_encounters(),
                    'maps': reader.extract_maps_as_ascii()
                }

            print(f"✅ Scénario chargé:")
            print(f"   - Titre: {self.scenario_data['title']}")
            print(f"   - Sections: {len(self.scenario_data['sections'])}")
            print(f"   - Lieux: {len(self.scenario_data['locations'])}")
            print(f"   - PNJs: {len(self.scenario_data['npcs'])}")

        except Exception as e:
            print(f"⚠️  Erreur lors du chargement du PDF: {e}")
            print("   Le jeu continuera avec les scènes prédéfinies.")
            self.scenario_data = {
                'title': self.get_scenario_name(),
                'sections': {},
                'locations': [],
                'npcs': [],
                'encounters': [],
                'maps': []
            }

        self.renderer.wait_for_input()

    def setup_party(self):
        """Configurer le groupe de personnages"""
        self.renderer.print_header("⚔️ CRÉATION DU GROUPE")

        self.party = self.create_party()

        print(f"\n👥 Groupe créé ({len(self.party)} membres):")
        for char in self.party:
            class_name = char.class_type.name if char.class_type else "Aventurier"
            print(f"  - {char.name} ({class_name} niveau {char.level})")
            print(f"    HP: {char.hit_points}/{char.max_hit_points}, "
                  f"CA: {char.armor_class}")

        self.renderer.wait_for_input()

    def build_scenes(self):
        """Construire toutes les scènes du scénario"""
        self.renderer.print_header("🎬 PRÉPARATION DE L'AVENTURE")

        print("Construction des scènes...")

        # Scènes personnalisées du scénario
        self.build_custom_scenes()

        # Scène de game over (commune à tous)
        from ..scenes.scene_system import NarrativeScene
        self.scene_manager.add_scene(NarrativeScene(
            scene_id="game_over",
            title="💀 GAME OVER",
            text="Votre groupe a été vaincu... L'aventure se termine ici.",
            next_scene_id=None
        ))

        print(f"✅ {len(self.scene_manager.scenes)} scènes créées")
        self.renderer.wait_for_input()

    def play(self):
        """Lancer le scénario complet"""
        self.renderer.print_header(f"🎲 {self.get_scenario_name().upper()}")

        print("Bienvenue dans cette aventure D&D 5e!")

        # 🆕 Proposer de charger une partie
        if self._ask_load_game():
            return

        self.renderer.wait_for_input()

        # 1. Charger le PDF
        self.load_scenario_from_pdf()

        # 2. Créer le groupe
        self.setup_party()

        # 3. Construire les scènes
        self.build_scenes()

        # 3.5 🆕 Charger équipements pour le combat
        print(f"\n📦 Chargement des équipements...")
        weapons, armors, equipments, potions = self._load_equipment()
        print(f"  Armes: {len(weapons)}, Armures: {len(armors)}, Équipements: {len(equipments)}, Potions: {len(potions)}")

        # 4. Préparer le contexte de jeu
        game_context = {
            'party': self.party,
            'game_state': self.game_state,
            'renderer': self.renderer,
            'combat_system': self.combat_system,
            'spellcasting': self.spellcasting,
            'merchant_system': self.merchant_system,
            'scenario_data': self.scenario_data,
            'weapons': weapons,        # 🆕
            'armors': armors,          # 🆕
            'equipments': equipments,  # 🆕
            'potions': potions,        # 🆕
            'scenario': self           # 🆕 Pour permettre la sauvegarde depuis les scènes
        }

        # 5. Lancer le scénario
        self.renderer.print_header("🎬 DÉBUT DE L'AVENTURE")
        self.renderer.wait_for_input()

        self.scene_manager.run(game_context, start_scene_id=self.get_start_scene_id())

        # 6. Statistiques finales
        self.show_final_stats()

    def get_start_scene_id(self) -> str:
        """Retourner l'ID de la scène de départ (peut être surchargé)"""
        return "intro"

    def show_final_stats(self):
        """Afficher les statistiques finales"""
        self.renderer.print_header("📊 STATISTIQUES FINALES")

        print(f"\n⚔️  Victoires en combat: {self.game_state['combat_victories']}")
        print(f"⭐ XP total gagné: {self.game_state['total_xp']}")
        print(f"💰 Or gagné: {self.game_state['gold']} po")
        print(f"💸 Or dépensé: {self.game_state['gold_spent']} po")
        print(f"🗺️  Lieux visités: {self.game_state['locations_visited']}")
        print(f"👥 PNJs rencontrés: {self.game_state['npcs_met']}")
        print(f"🎯 Quêtes complétées: {self.game_state['quests_completed']}")

        print("\n👥 État du groupe:")
        survivors = [c for c in self.party if c.hit_points > 0]
        print(f"   Survivants: {len(survivors)}/{len(self.party)}")

        for char in self.party:
            if char.hit_points > 0:
                hp_percent = int((char.hit_points / char.max_hit_points) * 100)
                status = "✅" if hp_percent > 50 else "⚠️"
                print(f"   {status} {char.name}: {char.hit_points}/{char.max_hit_points} HP ({hp_percent}%)")
            else:
                print(f"   ❌ {char.name}: KO")

        # Score final
        score = self._calculate_score()
        print(f"\n🏆 SCORE FINAL: {score} points")

        rank = self._get_rank(score)
        print(f"   Rang: {rank}")

        print("\n🎉 Merci d'avoir joué!")
        self.renderer.wait_for_input()

    def _calculate_score(self) -> int:
        """Calculer le score final"""
        score = 0

        # Points pour XP
        score += self.game_state['total_xp']

        # Points pour or (10 po = 1 point)
        score += (self.game_state['gold'] - self.game_state['gold_spent']) // 10

        # Bonus survivants
        survivors = [c for c in self.party if c.hit_points > 0]
        score += len(survivors) * 100

        # Bonus HP restants
        for char in survivors:
            hp_percent = (char.hit_points / char.max_hit_points)
            score += int(hp_percent * 50)

        # Bonus quêtes
        score += self.game_state['quests_completed'] * 200

        # Malus morts
        score -= self.game_state['deaths'] * 100

        return max(0, score)

    def _get_rank(self, score: int) -> str:
        """Obtenir le rang selon le score"""
        if score >= 2000:
            return "Légendaire 🏆✨"
        elif score >= 1500:
            return "Héroïque ⭐⭐⭐"
        elif score >= 1000:
            return "Vaillant ⭐⭐"
        elif score >= 500:
            return "Courageux ⭐"
        else:
            return "Débutant"

    def create_basic_fighter(self, name: str, level: int = 3) -> Character:
        """Utilitaire: créer un guerrier de base"""
        from dnd_5e_core import Abilities
        from dnd_5e_core.races import Race
        from dnd_5e_core.classes import ClassType
        from dnd_5e_core.abilities import AbilityType
        from ..core.adapters import CharacterExtensions

        race = Race(
            index='human', name='Humain', speed=30, ability_bonuses={},
            alignment='Any', age='Adult', size='Medium', size_description='5-6 ft',
            starting_proficiencies=[], starting_proficiency_options=[],
            languages=[], language_desc='Common', traits=[], subraces=[]
        )

        fighter_class = ClassType(
            index='fighter', name='Fighter', hit_die=10, proficiency_choices=[],
            proficiencies=[], saving_throws=[AbilityType.STR, AbilityType.CON],
            starting_equipment=[], starting_equipment_options=[], class_levels=[],
            multi_classing=[], subclasses=[], spellcasting_level=0,
            spellcasting_ability=None, can_cast=False, spell_slots={},
            spells_known=[], cantrips_known=[]
        )

        char = Character(
            name=name, race=race, subrace=None, ethnic='Human', gender='Male',
            height='6ft', weight='180 lbs', age=30,
            class_type=fighter_class, proficiencies=[],
            abilities=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=10),
            ability_modifiers=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=10),
            hit_points=10 + (level-1)*6 + level*2,  # HD + Con
            max_hit_points=10 + (level-1)*6 + level*2,
            speed=30, haste_timer=0.0, hasted=False,
            xp=level * 300, level=level,
            inventory=[], gold=50, sc=None, conditions=[]
        )

        CharacterExtensions.add_inventory_management(char)
        return char

    def create_basic_cleric(self, name: str, level: int = 3) -> Character:
        """Utilitaire: créer un clerc de base"""
        from dnd_5e_core import Abilities
        from dnd_5e_core.races import Race
        from dnd_5e_core.classes import ClassType
        from dnd_5e_core.abilities import AbilityType
        from ..core.adapters import CharacterExtensions

        race = Race(
            index='human', name='Humain', speed=30, ability_bonuses={},
            alignment='Good', age='Adult', size='Medium', size_description='5-6 ft',
            starting_proficiencies=[], starting_proficiency_options=[],
            languages=[], language_desc='Common', traits=[], subraces=[]
        )

        cleric_class = ClassType(
            index='cleric', name='Cleric', hit_die=8, proficiency_choices=[],
            proficiencies=[], saving_throws=[AbilityType.WIS, AbilityType.CHA],
            starting_equipment=[], starting_equipment_options=[], class_levels=[],
            multi_classing=[], subclasses=[], spellcasting_level=level,
            spellcasting_ability='wis', can_cast=True, spell_slots={},
            spells_known=[], cantrips_known=[]
        )

        char = Character(
            name=name, race=race, subrace=None, ethnic='Human', gender='Female',
            height='5ft6', weight='140 lbs', age=28,
            class_type=cleric_class, proficiencies=[],
            abilities=Abilities(str=12, dex=10, con=14, int=13, wis=16, cha=14),
            ability_modifiers=Abilities(str=12, dex=10, con=14, int=13, wis=16, cha=14),
            hit_points=8 + (level-1)*5 + level*2,
            max_hit_points=8 + (level-1)*5 + level*2,
            speed=30, haste_timer=0.0, hasted=False,
            xp=level * 300, level=level,
            inventory=[], gold=30, sc=None, conditions=[]
        )

        CharacterExtensions.add_inventory_management(char)
        CharacterExtensions.init_spell_slots(char)
        return char

    # 🆕 NOUVELLES MÉTHODES

    def save_game(self, slot_name: str = "autosave") -> bool:
        """Sauvegarder la partie en cours"""
        return self.save_manager.save_game(
            scenario_name=self.get_scenario_name(),
            party=self.party,
            game_state=self.game_state,
            scene_id=self.scene_manager.current_scene_id,
            slot_name=slot_name
        )

    def load_game(self, slot_name: str = "autosave") -> bool:
        """Charger une partie sauvegardée"""
        save_data = self.save_manager.load_game(slot_name)

        if not save_data:
            return False

        self.party = save_data['party']
        self.game_state = save_data['game_state']
        self.scene_manager.current_scene_id = save_data['scene_id']

        return True

    def show_map(self):
        """Afficher la carte d'exploration"""
        if self.exploration_map:
            print(self.exploration_map.get_ascii_map())
            print()
            print(self.exploration_map.get_location_info())

            visited, total, percentage = self.exploration_map.get_exploration_progress()
            print(f"\n📊 Exploration: {visited}/{total} ({percentage:.1f}%)")
        else:
            print("⚠️ Carte non disponible pour ce scénario")

    def update_map_location(self, location_id: str):
        """Mettre à jour la position sur la carte"""
        if self.exploration_map:
            self.exploration_map.visit_location(location_id)

    def check_level_up(self):
        """Vérifier et gérer les montées de niveau"""
        leveled_up = []

        for char in self.party:
            while self.level_manager.can_level_up(char):
                old_level = char.level
                if self.level_manager.level_up(char):
                    summary = self.level_manager.get_level_up_summary(char, old_level, char.level)
                    print(summary)
                    leveled_up.append(char.name)
                    self.renderer.wait_for_input()

        return leveled_up

    def rest_at_village(self):
        """Repos au village avec montée de niveau possible"""
        self.renderer.print_header("🏘️ REPOS AU VILLAGE")

        print("Vous vous reposez à l'auberge du village...")
        print()

        results = self.village_rest.rest_at_village(self.party)

        # Afficher soins
        if results['healed']:
            print(f"✅ Soignés: {', '.join(results['healed'])}")

        # Afficher montées de niveau
        if results['leveled_up']:
            print("\n⭐ MONTÉE DE NIVEAU!")
            for level_up_info in results['leveled_up']:
                char_name = level_up_info['name']
                old_level = level_up_info['old_level']
                new_level = level_up_info['new_level']

                # Trouver le personnage
                char = next((c for c in self.party if c.name == char_name), None)
                if char:
                    summary = self.level_manager.get_level_up_summary(char, old_level, new_level)
                    print(summary)
                    self.renderer.wait_for_input()

        print(f"\n💰 Coût de l'auberge: {results['cost']} po")

        # Déduire le coût
        for char in self.party:
            if char.gold >= 5:
                char.gold -= 5
                break

        self.renderer.wait_for_input()

    def quit_menu(self) -> str:
        """
        Menu de sortie

        Returns:
            'save_quit', 'quit', 'continue'
        """
        self.renderer.print_header("⏸️ MENU")

        choice = self.renderer.get_choice([
            "💾 Sauvegarder et quitter",
            "🚪 Quitter sans sauvegarder",
            "▶️  Continuer l'aventure"
        ])

        if choice == 0:
            # Sauvegarder
            slot_name = input("\nNom de la sauvegarde (ou ENTER pour autosave): ").strip()
            if not slot_name:
                slot_name = "autosave"

            if self.save_game(slot_name):
                print(f"✅ Partie sauvegardée: {slot_name}")
            else:
                print("❌ Erreur de sauvegarde")

            return 'save_quit'

        elif choice == 1:
            confirm = input("\n⚠️ Quitter sans sauvegarder? (oui/non): ").strip().lower()
            if confirm in ['oui', 'o', 'yes', 'y']:
                return 'quit'
            return 'continue'

        else:
            return 'continue'

    def _ask_load_game(self) -> bool:
        """Demander si charger une partie sauvegardée"""
        saves = self.save_manager.list_saves()
        if not saves:
            return False

        print("\n💾 Parties sauvegardées trouvées:")
        for i, save in enumerate(saves, 1):
            print(f"  {i}. {save['slot_name']} - {save.get('scenario', 'Unknown')} - {save.get('timestamp', '')[:19]}")

        print(f"  0. Nouvelle partie")

        try:
            choice = input("\nCharger une partie? (numéro ou 0): ").strip()
            if choice and choice.isdigit():
                idx = int(choice)
                if idx == 0:
                    return False
                if 1 <= idx <= len(saves):
                    if self.load_game(saves[idx - 1]['slot_name']):
                        print("✅ Partie chargée!")
                        self._resume_game()
                        return True
        except:
            pass

        return False

    def _resume_game(self):
        """Reprendre une partie chargée"""
        # Reconstruire les scènes
        self.build_scenes()

        # Préparer contexte
        game_context = {
            'party': self.party,
            'game_state': self.game_state,
            'renderer': self.renderer,
            'combat_system': self.combat_system,
            'spellcasting': self.spellcasting,
            'merchant_system': self.merchant_system,
            'scenario_data': self.scenario_data
        }

        # Reprendre à la scène sauvegardée
        print(f"\n🎬 Reprise à: {self.scene_manager.current_scene_id}")
        self.renderer.wait_for_input()

        self.scene_manager.run(game_context, start_scene_id=self.scene_manager.current_scene_id)

        # Stats finales
        self.show_final_stats()

    def _load_equipment(self):
        """Charger armes, armures, équipements et potions depuis dnd_5e_core"""
        weapons = []
        armors = []
        equipments = []
        potions = []

        try:
            # 🆕 Utiliser directement dnd_5e_core.data
            from dnd_5e_core.data import (
                list_weapons, list_armors, list_equipment,
                load_weapon, load_armor, load_equipment
            )
            from dnd_5e_core.equipment import HealingPotion, PotionRarity

            # Charger armes
            for name in list_weapons()[:20]:
                weapon = load_weapon(name)
                if weapon:
                    weapons.append(weapon)

            # Charger armures
            for name in list_armors()[:15]:
                armor = load_armor(name)
                if armor:
                    armors.append(armor)

            # Charger équipements
            for name in list_equipment()[:20]:
                equipment = load_equipment(name)
                if equipment:
                    equipments.append(equipment)

            # Créer quelques potions de base
            potions = [
                HealingPotion("Potion of Healing", PotionRarity.COMMON),
                HealingPotion("Potion of Greater Healing", PotionRarity.UNCOMMON),
            ]

            if weapons or armors or equipments:
                print(f"  ✅ Chargés depuis dnd_5e_core.data")
            else:
                print(f"  ℹ️  Aucune donnée disponible (normal)")


        except Exception as e:
            print(f"  ⚠️  Erreur chargement: {e}")
            print(f"  ℹ️  Combat fonctionnera avec équipements par défaut")

        return weapons, armors, equipments, potions
