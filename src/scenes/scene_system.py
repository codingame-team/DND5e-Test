"""
Scene System - Composite Pattern pour scénarios D&D
Permet de factoriser les scènes de jeu
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Callable
from enum import Enum
import time


class SceneType(Enum):
    """Types de scènes"""
    NARRATIVE = "narrative"
    CHOICE = "choice"
    COMBAT = "combat"
    MERCHANT = "merchant"
    REST = "rest"
    EXPLORATION = "exploration"


class SceneResult(Enum):
    """Résultats possibles d'une scène"""
    SUCCESS = "success"
    FAILURE = "failure"
    CONTINUE = "continue"
    EXIT = "exit"


class BaseScene(ABC):
    """
    Classe abstraite pour toutes les scènes
    Pattern Composite
    """

    def __init__(self, scene_id: str, title: str, description: str = ""):
        self.scene_id = scene_id
        self.title = title
        self.description = description
        self.next_scene_id: Optional[str] = None
        self.visited = False

    @abstractmethod
    def execute(self, game_context: Dict) -> SceneResult:
        """
        Exécuter la scène
        game_context contient: party, game_state, renderer, etc.
        """
        pass

    def on_enter(self, game_context: Dict):
        """Hook appelé en entrant dans la scène"""
        self.visited = True
        renderer = game_context.get('renderer')
        if renderer:
            renderer.print_header(self.title)

    def on_exit(self, game_context: Dict):
        """Hook appelé en quittant la scène"""
        pass


class NarrativeScene(BaseScene):
    """
    Scène narrative pure (texte, pas de choix)
    """

    def __init__(self, scene_id: str, title: str, text: str,
                 next_scene_id: str = None, delay: float = 0.02):
        super().__init__(scene_id, title)
        self.text = text
        self.next_scene_id = next_scene_id
        self.delay = delay

    def execute(self, game_context: Dict) -> SceneResult:
        self.on_enter(game_context)

        renderer = game_context['renderer']
        renderer.print_slow(self.text, self.delay)

        # 🆕 Proposer de sauvegarder après avoir lu le texte
        save_choice = input("\n💾 Sauvegarder la partie? (o/n): ").strip().lower()
        if save_choice in ['o', 'oui', 'y', 'yes']:
            scenario = game_context.get('scenario')
            if scenario:
                slot_name = input("Nom de la sauvegarde (ou ENTER pour autosave): ").strip()
                if not slot_name:
                    slot_name = "autosave"
                if scenario.save_game(slot_name):
                    print(f"✅ Partie sauvegardée: {slot_name}")
                else:
                    print("❌ Erreur lors de la sauvegarde")

        renderer.wait_for_input()

        self.on_exit(game_context)
        return SceneResult.CONTINUE


class ChoiceScene(BaseScene):
    """
    Scène avec choix multiples
    """

    def __init__(self, scene_id: str, title: str, description: str,
                 choices: List[Dict[str, any]]):
        """
        choices format: [
            {
                'text': "Texte du choix",
                'next_scene': "scene_id",
                'effects': {'reputation': +1},  # optionnel
                'condition': lambda ctx: True   # optionnel
            }
        ]
        """
        super().__init__(scene_id, title, description)
        self.choices = choices

    def execute(self, game_context: Dict) -> SceneResult:
        self.on_enter(game_context)

        renderer = game_context['renderer']
        if self.description:
            renderer.print_slow(self.description)

        # Filtrer choix selon conditions
        available_choices = []
        choice_mapping = []

        for i, choice in enumerate(self.choices):
            condition = choice.get('condition', lambda ctx: True)
            if condition(game_context):
                available_choices.append(choice['text'])
                choice_mapping.append(i)

        if not available_choices:
            print("Aucun choix disponible!")
            return SceneResult.FAILURE

        # 🆕 Ajouter option de sauvegarde
        available_choices.append("💾 Sauvegarder la partie")

        # Obtenir choix joueur
        choice_idx = renderer.get_choice(available_choices)

        # 🆕 Gérer la sauvegarde
        if choice_idx == len(available_choices) - 1:
            scenario = game_context.get('scenario')
            if scenario:
                slot_name = input("\nNom de la sauvegarde (ou ENTER pour autosave): ").strip()
                if not slot_name:
                    slot_name = "autosave"
                if scenario.save_game(slot_name):
                    print(f"✅ Partie sauvegardée: {slot_name}")
                else:
                    print("❌ Erreur lors de la sauvegarde")
                renderer.wait_for_input()
            # Ré-afficher les choix
            return self.execute(game_context)

        selected_choice = self.choices[choice_mapping[choice_idx]]

        # Appliquer effets
        if 'effects' in selected_choice:
            self._apply_effects(selected_choice['effects'], game_context)

        # Définir prochaine scène
        self.next_scene_id = selected_choice.get('next_scene')

        # Callback optionnel
        if 'callback' in selected_choice:
            selected_choice['callback'](game_context)

        self.on_exit(game_context)
        return SceneResult.CONTINUE

    def _apply_effects(self, effects: Dict, game_context: Dict):
        """Appliquer effets du choix"""
        game_state = game_context['game_state']

        for key, value in effects.items():
            if key in game_state:
                game_state[key] += value
            else:
                game_state[key] = value


class CombatScene(BaseScene):
    """
    Scène de combat
    """

    def __init__(self, scene_id: str, title: str, description: str,
                 enemies_factory: Callable,
                 on_victory_scene: str,
                 on_defeat_scene: str = "game_over"):
        super().__init__(scene_id, title, description)
        self.enemies_factory = enemies_factory  # Function qui retourne liste de monstres
        self.on_victory_scene = on_victory_scene
        self.on_defeat_scene = on_defeat_scene

    def execute(self, game_context: Dict) -> SceneResult:
        self.on_enter(game_context)

        renderer = game_context['renderer']
        if self.description:
            renderer.print_slow(self.description)

        # Créer ennemis
        enemies = self.enemies_factory(game_context)

        # Lancer combat
        combat_system = game_context.get('combat_system')
        if not combat_system:
            print("❌ Système de combat non disponible!")
            return SceneResult.FAILURE

        party = game_context['party']
        alive_chars = [c for c in party if c.hit_points > 0]
        alive_monsters = enemies.copy()

        # Afficher info combat
        print(f"\n⚔️  Votre groupe:")
        for char in alive_chars:
            print(f"  - {char.name}: {char.hit_points}/{char.max_hit_points} HP")

        print(f"\n👹 Ennemis:")
        for monster in alive_monsters:
            print(f"  - {monster.name}: {monster.hit_points} HP")

        renderer.wait_for_input("\n[Combat! Appuyez sur ENTRÉE]")

        # Combat loop - utilise CombatSystem correctement
        round_num = 1
        max_rounds = 50

        while alive_chars and alive_monsters and round_num <= max_rounds:
            print(f"\n{'─' * 60}")
            print(f"  TOUR {round_num}")
            print(f"{'─' * 60}\n")

            # Tours personnages
            for char in alive_chars[:]:
                if not alive_monsters:
                    break
                if char.hit_points <= 0:
                    if char in alive_chars:
                        alive_chars.remove(char)
                    continue

                # Appeler character_turn avec TOUS les paramètres
                combat_system.character_turn(
                    character=char,
                    alive_chars=alive_chars,
                    alive_monsters=alive_monsters,
                    party=party,
                    weapons=game_context.get('weapons', []),
                    armors=game_context.get('armors', []),
                    equipments=game_context.get('equipments', []),
                    potions=game_context.get('potions', [])
                )

            # Tours monstres
            for monster in alive_monsters[:]:
                if not alive_chars:
                    break
                if monster.hit_points <= 0:
                    if monster in alive_monsters:
                        alive_monsters.remove(monster)
                    continue

                # Limiter attaque à la ligne de front (comme dans advanced_combat)
                char_indices = {party.index(c): c for c in alive_chars if c in party}
                melee_chars = [c for idx, c in char_indices.items() if idx < 3]
                ranged_chars = [c for idx, c in char_indices.items() if idx >= 3]
                accessible_chars = melee_chars if melee_chars else ranged_chars

                combat_system.monster_turn(
                    monster=monster,
                    alive_monsters=alive_monsters,
                    alive_chars=accessible_chars if accessible_chars else alive_chars,
                    party=party,
                    round_num=round_num
                )

            round_num += 1

        # Résultat
        if alive_chars:
            print("\n✅ VICTOIRE!")

            # Récompenses
            total_xp = sum(m.xp for m in enemies)
            game_context['game_state']['total_xp'] = game_context['game_state'].get('total_xp', 0) + total_xp

            self.next_scene_id = self.on_victory_scene
            self.on_exit(game_context)
            return SceneResult.SUCCESS
        else:
            print("\n❌ DÉFAITE!")
            self.next_scene_id = self.on_defeat_scene
            self.on_exit(game_context)
            return SceneResult.FAILURE


class MerchantScene(BaseScene):
    """
    Scène de marchand
    """

    def __init__(self, scene_id: str, title: str, merchant_id: str,
                 next_scene_id: str):
        super().__init__(scene_id, title)
        self.merchant_id = merchant_id
        self.next_scene_id = next_scene_id

    def execute(self, game_context: Dict) -> SceneResult:
        self.on_enter(game_context)

        # Import ici pour éviter dépendance circulaire
        from src.systems.merchant import MerchantSystem

        merchant_system = game_context.get('merchant_system')
        if not merchant_system:
            merchant_system = MerchantSystem()

        # 🆕 Passer weapons et armors au marchand
        weapons = game_context.get('weapons', [])
        armors = game_context.get('armors', [])
        merchant = MerchantSystem.get_merchant(self.merchant_id, weapons, armors)

        if not merchant:
            print(f"❌ Marchand {self.merchant_id} non trouvé!")
            return SceneResult.FAILURE

        party = game_context['party']
        renderer = game_context['renderer']

        # Boucle d'achat
        shopping = True
        while shopping:
            print(merchant_system.display_shop(merchant, party[0]))

            choice = renderer.get_choice([
                "Acheter pour un personnage",
                "Voir inventaires du groupe",
                "Quitter la boutique"
            ])

            if choice == 0:
                # Acheter pour un personnage
                items = merchant_system.get_buyable_items(merchant)
                if not items:
                    print("\n❌ Le marchand n'a plus rien à vendre!")
                    renderer.wait_for_input()
                    continue

                # Choisir personnage
                print("\nPour quel personnage voulez-vous acheter?")
                char_choices = [f"{char.name} ({char.gold} po)" for char in party]
                char_idx = renderer.get_choice(char_choices)
                character = party[char_idx]

                # Choisir article
                print(f"\n💰 {character.name} a {character.gold} po")
                print("\nQue voulez-vous acheter?")

                item_choices = []
                item_mapping = []

                for item_id, item, qty, price in items:
                    if price <= character.gold:  # Seulement items abordables
                        stock_str = f"({qty} en stock)" if qty < 10 else ""
                        item_choices.append(f"{item.name} - {price} po {stock_str}")
                        item_mapping.append((item_id, price))

                if not item_choices:
                    print(f"\n❌ {character.name} n'a pas assez d'or pour acheter quoi que ce soit!")
                    renderer.wait_for_input()
                    continue

                item_choices.append("Annuler")
                item_idx = renderer.get_choice(item_choices)

                if item_idx < len(item_mapping):
                    # Acheter l'article
                    item_id, price = item_mapping[item_idx]

                    if merchant_system.buy_item(character, merchant, item_id):
                        print(f"\n✅ {character.name} a acheté {item_id.replace('_', ' ')} pour {price} po!")
                        print(f"   Or restant: {character.gold} po")

                        # Obtenir l'article acheté (dernier dans l'inventaire)
                        from src.core.adapters import CharacterExtensions
                        from src.systems.merchant import Weapon, Armor

                        if hasattr(character, 'inventory_items') and character.inventory_items:
                            purchased_item = character.inventory_items[-1]

                            # Proposer d'équiper si c'est une arme ou armure
                            if isinstance(purchased_item, Weapon):
                                print(f"\n🗡️  Voulez-vous équiper {purchased_item.name} maintenant?")
                                equip_choice = renderer.get_choice(["Oui, équiper", "Non, garder dans l'inventaire"])

                                if equip_choice == 0:
                                    CharacterExtensions.equip_weapon(character, purchased_item)
                                    print(f"   ✅ {purchased_item.name} équipé!")
                                    print(f"   ⚔️  Dégâts: {purchased_item.damage_dice}")

                            elif isinstance(purchased_item, Armor):
                                print(f"\n🛡️  Voulez-vous équiper {purchased_item.name} maintenant?")
                                equip_choice = renderer.get_choice(["Oui, équiper", "Non, garder dans l'inventaire"])

                                if equip_choice == 0:
                                    CharacterExtensions.equip_armor(character, purchased_item)
                                    print(f"   ✅ {purchased_item.name} équipé!")
                                    print(f"   🛡️  CA: {CharacterExtensions.get_armor_class(character)}")

                            # Afficher inventaire mis à jour
                            print(f"\n📦 Inventaire de {character.name}:")
                            for item in character.inventory_items:
                                print(f"   - {item.name}")

                        # Mettre à jour état du jeu
                        game_context['game_state']['gold_spent'] = game_context['game_state'].get('gold_spent', 0) + price
                    else:
                        print(f"\n❌ Impossible d'acheter cet article!")

                    renderer.wait_for_input()
                # Sinon, annuler (ne fait rien)

            elif choice == 1:
                # Voir inventaires
                print("\n" + "="*60)
                print("  📦 INVENTAIRES DU GROUPE")
                print("="*60)

                for char in party:
                    print(f"\n👤 {char.name}")
                    print(f"   💰 Or: {char.gold} po")

                    if hasattr(char, 'equipped_weapon') and char.equipped_weapon:
                        print(f"   🗡️  Arme: {char.equipped_weapon.name}")

                    if hasattr(char, 'equipped_armor') and char.equipped_armor:
                        print(f"   🛡️  Armure: {char.equipped_armor.name}")

                    if hasattr(char, 'inventory_items') and char.inventory_items:
                        print(f"   📦 Inventaire ({len(char.inventory_items)} objets):")
                        for item in char.inventory_items:
                            print(f"      - {item.name}")
                    else:
                        print(f"   📦 Inventaire vide")

                print("\n" + "="*60)
                renderer.wait_for_input()

            else:
                shopping = False

        self.on_exit(game_context)
        return SceneResult.CONTINUE


class RestScene(BaseScene):
    """
    Scène de repos
    """

    def __init__(self, scene_id: str, title: str, rest_type: str = "long",
                 next_scene_id: str = None):
        super().__init__(scene_id, title)
        self.rest_type = rest_type  # "short" or "long"
        self.next_scene_id = next_scene_id

    def execute(self, game_context: Dict) -> SceneResult:
        self.on_enter(game_context)

        party = game_context['party']
        renderer = game_context['renderer']

        if self.rest_type == "long":
            renderer.print_slow("Vous installez un campement pour la nuit...")
            time.sleep(1)

            for char in party:
                if char.hit_points > 0:
                    old_hp = char.hit_points
                    char.hit_points = char.max_hit_points

                    # Restaurer sorts
                    from src.core.adapters import CharacterExtensions
                    CharacterExtensions.long_rest(char)

                    print(f"✨ {char.name}: {old_hp} → {char.hit_points} HP, sorts restaurés")

            renderer.print_slow("\n💤 Votre groupe est complètement reposé!")

        else:  # short rest
            renderer.print_slow("Vous prenez un court repos...")
            for char in party:
                if char.hit_points > 0:
                    from src.core.adapters import CharacterExtensions
                    old_hp = char.hit_points
                    CharacterExtensions.rest_short(char) if hasattr(CharacterExtensions, 'rest_short') else None
                    if char.hit_points > old_hp:
                        print(f"✨ {char.name}: +{char.hit_points - old_hp} HP")

        renderer.wait_for_input()
        self.on_exit(game_context)
        return SceneResult.CONTINUE


# Gestionnaire de scènes
class SceneManager:
    """
    Gestionnaire de scènes - Pattern Composite
    """

    def __init__(self):
        self.scenes: Dict[str, BaseScene] = {}
        self.current_scene_id: Optional[str] = None
        self.history: List[str] = []

    def add_scene(self, scene: BaseScene):
        """Ajouter une scène"""
        self.scenes[scene.scene_id] = scene

    def set_start_scene(self, scene_id: str):
        """Définir scène de départ"""
        self.current_scene_id = scene_id

    def execute_scene(self, scene_id: str, game_context: Dict) -> SceneResult:
        """Exécuter une scène"""
        if scene_id not in self.scenes:
            print(f"❌ Scène {scene_id} non trouvée!")
            return SceneResult.FAILURE

        scene = self.scenes[scene_id]
        self.history.append(scene_id)

        result = scene.execute(game_context)

        # Mettre à jour scène courante
        # Si next_scene_id est None, on termine le scénario
        self.current_scene_id = scene.next_scene_id

        return result

    def run(self, game_context: Dict, start_scene_id: Optional[str] = None):
        """
        Exécuter le scénario complet
        Boucle principale du jeu
        """
        if start_scene_id:
            self.current_scene_id = start_scene_id

        if not self.current_scene_id:
            print("❌ Aucune scène de départ définie!")
            return

        while self.current_scene_id:
            result = self.execute_scene(self.current_scene_id, game_context)

            if result == SceneResult.EXIT:
                print("\n" + "="*70)
                print("🏁 Fin du scénario")
                print("="*70)
                break
            elif result == SceneResult.FAILURE:
                # Gérer échec (game over, etc.)
                print("\n💀 Game Over")
                break

            # Si pas de prochaine scène, fin du scénario
            if not self.current_scene_id:
                print("\n" + "="*70)
                print("🏁 Fin du scénario - Merci d'avoir joué!")
                print("="*70)
                break

