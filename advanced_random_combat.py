"""
Combat avancé avec un groupe de 6 aventuriers aléatoires vs monstres
Version avec mécanique améliorée de positionnement front/arrière
"""
import sys

# Ajouter le chemin du projet DnD-5th-Edition-API
sys.path.insert(0, '/Users/display/PycharmProjects/DnD-5th-Edition-API')

from main import (
    generate_random_character,
    load_character_collections,
    request_monster,
    populate
)

from dnd_5e_core import Monster, Character
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.mechanics import calculate_encounter_difficulty, get_appropriate_cr_range
from random import choice, randint, random
from typing import List, Tuple


def load_monsters_database() -> List[Monster]:
    """Charger tous les monstres disponibles"""
    print("Chargement de la base de données des monstres...")
    monster_names = populate(collection_name="monsters", key_name="results")
    monsters = []
    for name in monster_names:
        monster = request_monster(name)
        if monster:
            monsters.append(monster)
    print(f"✓ {len(monsters)} monstres chargés.")
    return monsters


def select_monsters_for_encounter(
    party_levels: List[int],
    monsters_db: List[Monster],
    difficulty: str = "medium",
    max_monsters: int = 8
) -> List[Monster]:
    """
    Sélectionner des monstres appropriés pour une rencontre équilibrée
    """
    avg_level = sum(party_levels) / len(party_levels)
    min_cr, max_cr = get_appropriate_cr_range(int(avg_level))

    # Filtrer les monstres par CR approprié
    suitable_monsters = [
        m for m in monsters_db
        if min_cr <= m.challenge_rating <= max_cr
    ]

    if not suitable_monsters:
        suitable_monsters = [m for m in monsters_db if m.challenge_rating <= 2]

    # Sélectionner des monstres jusqu'à obtenir une difficulté appropriée
    selected_monsters = []
    max_attempts = 100
    attempts = 0

    difficulty_map = {
        "trivial": 0,
        "easy": 1,
        "medium": 2,
        "hard": 3,
        "deadly": 4
    }

    target_difficulty = difficulty_map.get(difficulty, 2)

    while attempts < max_attempts:
        monster = choice(suitable_monsters)
        test_monsters = selected_monsters + [monster]

        monster_crs = [m.challenge_rating for m in test_monsters]
        adjusted_xp, calc_difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

        calc_diff_level = difficulty_map.get(calc_difficulty, 0)

        if calc_diff_level == target_difficulty:
            selected_monsters.append(monster)
            break
        elif calc_diff_level < target_difficulty:
            selected_monsters.append(monster)
        else:
            # On a dépassé, on s'arrête
            break

        attempts += 1

        if len(selected_monsters) >= max_monsters:
            break

    if not selected_monsters:
        selected_monsters = [choice(suitable_monsters)]

    return selected_monsters


def create_random_party(
    size: int,
    races: List,
    subraces: List,
    classes: List,
    names: dict,
    human_names: dict,
    spells: List,
    min_level: int = 1,
    max_level: int = 5
) -> List[Character]:
    """Créer un groupe de personnages aléatoires"""
    party = []
    roster = []

    # Classes préférées pour la ligne de front (mêlée)
    melee_classes = ["fighter", "paladin", "barbarian", "monk"]
    # Classes préférées pour la ligne arrière (distance/sorts)
    ranged_classes = ["wizard", "sorcerer", "warlock", "bard", "druid", "cleric"]

    for i in range(size):
        # Créer le personnage
        char = generate_random_character(
            roster=roster,
            races=races,
            subraces=subraces,
            classes=classes,
            names=names,
            human_names=human_names,
            spells=spells
        )

        # Définir un niveau aléatoire
        level = randint(min_level, max_level)
        char.level = level

        # Ajuster les HP
        char.max_hit_points = (char.class_type.hit_die + char.ability_modifiers.con) * level
        char.hit_points = char.max_hit_points

        # Marquer le rôle au combat (pour affichage)
        if i < 3:
            char.combat_role = "front"
        else:
            char.combat_role = "back"

        party.append(char)
        roster.append(char)

    return party


def display_combat_stats(party: List[Character], monsters: List[Monster]):
    """Afficher les statistiques du combat"""
    front_line = [c for c in party if getattr(c, 'combat_role', 'front') == 'front']
    back_line = [c for c in party if getattr(c, 'combat_role', 'back') == 'back']

    print("\n" + "=" * 80)
    print("  ⚔️  COMPOSITION DES FORCES  ⚔️")
    print("=" * 80)

    print("\n🛡️  LIGNE DE FRONT (3 combattants au corps-à-corps):")
    print("   " + "─" * 76)
    for i, char in enumerate(front_line, 1):
        spell_info = ""
        if hasattr(char, 'sc') and char.sc and hasattr(char.sc, 'learned_spells'):
            spell_count = len(char.sc.learned_spells)
            if spell_count > 0:
                spell_info = f" | 🔮 {spell_count} sorts"

        print(f"   {i}. {char.name:<20} {char.race.name:<12} {char.class_type.name:<10} Niv.{char.level}")
        print(f"      💚 HP: {char.hit_points:>3}/{char.max_hit_points:<3} | "
              f"⚔️ FOR:{char.abilities.str:>2} DEX:{char.abilities.dex:>2} CON:{char.abilities.con:>2}"
              f"{spell_info}")

    print("\n🏹  LIGNE ARRIÈRE (3 combattants à distance/sorts):")
    print("   " + "─" * 76)
    for i, char in enumerate(back_line, 1):
        spell_info = "Pas de magie"
        if hasattr(char, 'sc') and char.sc and hasattr(char.sc, 'learned_spells'):
            spell_count = len(char.sc.learned_spells)
            if spell_count > 0:
                cantrips = len([s for s in char.sc.learned_spells if s.level == 0])
                spells = spell_count - cantrips
                spell_info = f"{cantrips} cantrips, {spells} sorts"

        print(f"   {i}. {char.name:<20} {char.race.name:<12} {char.class_type.name:<10} Niv.{char.level}")
        print(f"      💚 HP: {char.hit_points:>3}/{char.max_hit_points:<3} | "
              f"🧠 INT:{char.abilities.int:>2} SAG:{char.abilities.wis:>2} CHA:{char.abilities.cha:>2} | "
              f"🔮 {spell_info}")

    print("\n👹  FORCES ENNEMIES:")
    print("   " + "─" * 76)
    for i, monster in enumerate(monsters, 1):
        print(f"   {i}. {monster.name:<25} CR {monster.challenge_rating:<4} | "
              f"💚 HP: {monster.hit_points:>3}/{monster.max_hit_points:<3} | "
              f"🛡️ CA: {monster.armor_class:>2}")


def run_advanced_combat(party: List[Character], monsters: List[Monster]):
    """
    Exécuter le combat avec mécanique améliorée de positionnement
    """
    combat = CombatSystem(verbose=True)

    front_line = [c for c in party if getattr(c, 'combat_role', 'front') == 'front']
    back_line = [c for c in party if getattr(c, 'combat_role', 'back') == 'back']

    alive_chars = party.copy()
    alive_monsters = monsters.copy()

    # Affichage initial
    display_combat_stats(party, monsters)

    # Calculer la difficulté
    party_levels = [char.level for char in party]
    monster_crs = [m.challenge_rating for m in monsters]
    adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

    avg_level = sum(party_levels) / len(party_levels)
    total_party_hp = sum(c.max_hit_points for c in party)
    total_monster_hp = sum(m.max_hit_points for m in monsters)

    print("\n" + "=" * 80)
    print("  📊  ANALYSE DE LA RENCONTRE  📊")
    print("=" * 80)
    print(f"  Niveau moyen du groupe: {avg_level:.1f}")
    print(f"  HP total groupe: {total_party_hp} | HP total monstres: {total_monster_hp}")
    print(f"  Difficulté: {difficulty.upper()} ({adjusted_xp} XP ajustés)")
    print(f"  Nombre de monstres: {len(monsters)} | Multiplicateur: variable selon effectif")
    print("=" * 80)

    input("\n⏸️  Appuyez sur Entrée pour lancer le combat...")

    round_num = 1
    max_rounds = 30

    # Boucle de combat
    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'='*80}")
        print(f"  ⚔️  ROUND {round_num}  ⚔️")
        print(f"{'='*80}")

        # Phase 1: Tours des personnages
        print("\n--- 🗡️  Phase des Aventuriers ---\n")

        for char in alive_chars[:]:
            if not alive_monsters:
                break

            # Déterminer le rôle
            is_front_line = char in front_line

            print(f"➤ {char.name} ({char.class_type.name} Niv.{char.level}) "
                  f"[{'FRONT' if is_front_line else 'ARRIÈRE'}]:")

            combat.character_turn(
                character=char,
                alive_chars=alive_chars,
                alive_monsters=alive_monsters,
                party=party
            )

        # Phase 2: Tours des monstres
        if alive_chars and alive_monsters:
            print("\n--- 👹  Phase des Monstres ---\n")

            for monster in alive_monsters[:]:
                if not alive_chars:
                    break

                # Les monstres ciblent prioritairement la ligne de front
                front_alive = [c for c in front_line if c in alive_chars]
                back_alive = [c for c in back_line if c in alive_chars]

                target_info = f"[Cible: "
                if front_alive:
                    target_info += f"{len(front_alive)} front"
                    if back_alive:
                        target_info += f", {len(back_alive)} arrière"
                else:
                    target_info += f"{len(back_alive)} arrière"
                target_info += "]"

                print(f"➤ {monster.name} (CR {monster.challenge_rating}) {target_info}:")

                combat.monster_turn(
                    monster=monster,
                    alive_monsters=alive_monsters,
                    alive_chars=alive_chars,
                    party=party,
                    round_num=round_num
                )

        round_num += 1

        # Afficher l'état après chaque round
        print(f"\n{'─'*80}")
        print(f"  📊  ÉTAT APRÈS LE ROUND {round_num - 1}")
        print(f"{'─'*80}")

        if alive_chars:
            front_alive = [c for c in front_line if c in alive_chars]
            back_alive = [c for c in back_line if c in alive_chars]

            if front_alive:
                print("\n🛡️  Ligne de Front:")
                for char in front_alive:
                    hp_percent = (char.hit_points / char.max_hit_points) * 100
                    status = "🟢" if hp_percent > 50 else ("🟡" if hp_percent > 25 else "🔴")
                    print(f"   {status} {char.name:<20} {char.hit_points:>3}/{char.max_hit_points:<3} HP ({hp_percent:>5.1f}%)")

            if back_alive:
                print("\n🏹  Ligne Arrière:")
                for char in back_alive:
                    hp_percent = (char.hit_points / char.max_hit_points) * 100
                    status = "🟢" if hp_percent > 50 else ("🟡" if hp_percent > 25 else "🔴")
                    print(f"   {status} {char.name:<20} {char.hit_points:>3}/{char.max_hit_points:<3} HP ({hp_percent:>5.1f}%)")

        if alive_monsters:
            print("\n👹  Monstres:")
            for monster in alive_monsters:
                hp_percent = (monster.hit_points / monster.max_hit_points) * 100
                status = "🟢" if hp_percent > 50 else ("🟡" if hp_percent > 25 else "🔴")
                print(f"   {status} {monster.name:<25} {monster.hit_points:>3}/{monster.max_hit_points:<3} HP ({hp_percent:>5.1f}%)")

        print(f"{'─'*80}")

    # Résultats finaux
    print("\n" + "=" * 80)
    print("  🏆  RÉSULTAT FINAL DU COMBAT  🏆")
    print("=" * 80)

    if alive_chars and not alive_monsters:
        print("\n🎉 ✨ VICTOIRE HÉROÏQUE! ✨ Les aventuriers ont triomphé!")

        survivors = len(alive_chars)
        casualties = len(party) - survivors
        survival_rate = (survivors / len(party)) * 100

        print(f"\n📊  Statistiques:")
        print(f"   Survivants: {survivors}/{len(party)} ({survival_rate:.0f}%)")
        print(f"   Pertes: {casualties}/{len(party)}")
        print(f"   Rounds de combat: {round_num - 1}")
        print(f"   XP gagnés: {adjusted_xp} (à répartir)")

        print(f"\n✅  Survivants:")
        for char in alive_chars:
            hp_percent = (char.hit_points / char.max_hit_points) * 100
            xp_share = adjusted_xp // len(alive_chars)
            print(f"   ✓ {char.name:<20} {char.class_type.name:<10} | "
                  f"{char.hit_points:>3}/{char.max_hit_points:<3} HP ({hp_percent:>5.1f}%) | "
                  f"+{xp_share} XP")

        if casualties > 0:
            print(f"\n💀  Tombés au combat:")
            for char in party:
                if char not in alive_chars:
                    print(f"   ✝ {char.name} ({char.class_type.name} Niv.{char.level}) - "
                          f"\"Nous nous souviendrons de son sacrifice...\"")

    elif alive_monsters and not alive_chars:
        print("\n💀 ⚰️  DÉFAITE CATASTROPHIQUE! ⚰️")
        print("\n   Tous les aventuriers ont péri au combat...")
        print(f"   Le groupe a tenu {round_num - 1} rounds avant d'être anéanti.")

        print(f"\n👹  Monstres victorieux:")
        for monster in alive_monsters:
            hp_percent = (monster.hit_points / monster.max_hit_points) * 100
            print(f"   {monster.name}: {monster.hit_points}/{monster.max_hit_points} HP ({hp_percent:.1f}%)")

    elif round_num > max_rounds:
        print("\n⏱️  ⚔️  COMBAT INTERMINABLE!")
        print(f"\n   Le combat a duré {max_rounds} rounds sans vainqueur clair.")
        print(f"   Survivants: {len(alive_chars)} aventuriers, {len(alive_monsters)} monstres")
        print("\n   Les deux camps se retirent, épuisés...")

    else:
        print("\n💥  🌪️  DESTRUCTION MUTUELLE!")
        print("\n   Les deux camps se sont annihilés mutuellement...")
        print("   Un silence mortel règne sur le champ de bataille...")

    print("=" * 80)


def main():
    """Programme principal"""
    print("\n" + "=" * 80)
    print("  🎲  SIMULATEUR DE COMBAT D&D 5e - VERSION AVANCÉE  🎲")
    print("=" * 80)
    print("\n  Combat tactique avec positionnement stratégique")
    print("  - 3 aventuriers en ligne de FRONT (mêlée)")
    print("  - 3 aventuriers en ligne ARRIÈRE (distance/sorts)")
    print("  - Monstres sélectionnés par Challenge Rating")
    print("=" * 80)

    # Charger les collections
    print("\n📚  Chargement des données...")
    (races, subraces, classes, alignments, equipments,
     proficiencies, names, human_names, spells) = load_character_collections()
    print(f"✓ {len(races)} races, {len(classes)} classes, {len(spells)} sorts")

    # Charger les monstres
    monsters_db = load_monsters_database()

    # Créer le groupe de 6 aventuriers
    print("\n⚔️  Génération du groupe d'aventuriers...")
    party = create_random_party(
        size=6,
        races=races,
        subraces=subraces,
        classes=classes,
        names=names,
        human_names=human_names,
        spells=spells,
        min_level=2,
        max_level=5
    )
    print(f"✓ Groupe de {len(party)} aventuriers générés aléatoirement")

    # Sélectionner les monstres
    print("\n👹  Sélection des adversaires...")
    party_levels = [char.level for char in party]
    avg_level = sum(party_levels) / len(party_levels)
    print(f"   Niveau moyen du groupe: {avg_level:.1f}")

    # Vous pouvez changer la difficulté ici: 'easy', 'medium', 'hard', 'deadly'
    difficulty = "medium"

    monsters = select_monsters_for_encounter(
        party_levels=party_levels,
        monsters_db=monsters_db,
        difficulty=difficulty,
        max_monsters=6
    )
    print(f"✓ {len(monsters)} monstre(s) sélectionné(s) (difficulté: {difficulty})")

    # Lancer le combat
    run_advanced_combat(party, monsters)


if __name__ == "__main__":
    main()

