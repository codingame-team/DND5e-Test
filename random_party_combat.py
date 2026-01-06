"""
Combat avec un groupe de 6 aventuriers aléatoires vs monstres
Utilise generate_random_character() de main.py et le système de Challenge Rating
"""
import sys
import os

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
from random import choice, randint
from typing import List


def load_monsters_database() -> List[Monster]:
    """Charger tous les monstres disponibles"""
    print("Chargement de la base de données des monstres...")
    monster_names = populate(collection_name="monsters", key_name="results")
    monsters = []
    for name in monster_names:
        monster = request_monster(name)
        if monster:
            monsters.append(monster)
    print(f"{len(monsters)} monstres chargés.")
    return monsters


def select_monsters_for_encounter(
    party_levels: List[int],
    monsters_db: List[Monster],
    difficulty: str = "medium"
) -> List[Monster]:
    """
    Sélectionner des monstres appropriés pour une rencontre équilibrée

    Args:
        party_levels: Liste des niveaux des personnages
        monsters_db: Base de données de tous les monstres
        difficulty: Difficulté souhaitée ('easy', 'medium', 'hard', 'deadly')

    Returns:
        Liste des monstres pour la rencontre
    """
    avg_level = sum(party_levels) / len(party_levels)
    min_cr, max_cr = get_appropriate_cr_range(int(avg_level))

    # Filtrer les monstres par CR approprié
    suitable_monsters = [
        m for m in monsters_db
        if min_cr <= m.challenge_rating <= max_cr
    ]

    if not suitable_monsters:
        # Fallback: prendre n'importe quel monstre de CR bas
        suitable_monsters = [m for m in monsters_db if m.challenge_rating <= 2]

    # Sélectionner des monstres jusqu'à obtenir une difficulté appropriée
    selected_monsters = []
    max_attempts = 50
    attempts = 0

    while attempts < max_attempts:
        # Ajouter un monstre aléatoire
        monster = choice(suitable_monsters)
        test_monsters = selected_monsters + [monster]

        # Calculer la difficulté
        monster_crs = [m.challenge_rating for m in test_monsters]
        adjusted_xp, calc_difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

        # Vérifier si on a atteint la difficulté souhaitée
        if calc_difficulty == difficulty:
            selected_monsters.append(monster)
            break
        elif calc_difficulty in ["trivial", "easy"] and difficulty in ["medium", "hard", "deadly"]:
            selected_monsters.append(monster)
        elif calc_difficulty == "medium" and difficulty in ["hard", "deadly"]:
            selected_monsters.append(monster)
        elif calc_difficulty == "hard" and difficulty == "deadly":
            selected_monsters.append(monster)
        else:
            # On a dépassé, on s'arrête
            break

        attempts += 1

        # Limiter le nombre de monstres
        if len(selected_monsters) >= 8:
            break

    # Si aucun monstre sélectionné, en prendre un au hasard
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
    """
    Créer un groupe de personnages aléatoires

    Args:
        size: Nombre de personnages
        races, subraces, classes, names, human_names, spells: Collections chargées
        min_level: Niveau minimum
        max_level: Niveau maximum

    Returns:
        Liste de personnages aléatoires
    """
    party = []
    roster = []  # Liste vide pour les noms réservés

    for i in range(size):
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

        # Ajuster les HP en fonction du niveau
        # Formule simplifiée: HP = (hit_die + con_mod) * level
        char.max_hit_points = (char.class_type.hit_die + char.ability_modifiers.con) * level
        char.hit_points = char.max_hit_points

        party.append(char)
        roster.append(char)

    return party


def run_combat(party: List[Character], monsters: List[Monster]):
    """
    Exécuter le combat entre le groupe et les monstres

    Args:
        party: Groupe de personnages (6 aventuriers)
        monsters: Liste des monstres
    """
    combat = CombatSystem(verbose=True)

    # Diviser le groupe: 3 au front (mêlée), 3 à l'arrière (distance/sorts)
    front_line = party[:3]
    back_line = party[3:]

    alive_chars = party.copy()
    alive_monsters = monsters.copy()

    # Affichage initial
    print("=" * 80)
    print("  COMBAT: Groupe d'aventuriers vs Monstres")
    print("=" * 80)

    print("\n🗡️  LIGNE DE FRONT (Mêlée):")
    for i, char in enumerate(front_line, 1):
        print(f"  {i}. {char.name} - {char.class_type.name} Niv.{char.level} "
              f"(HP: {char.hit_points}/{char.max_hit_points})")

    print("\n🏹  LIGNE ARRIÈRE (Distance/Sorts):")
    for i, char in enumerate(back_line, 1):
        print(f"  {i}. {char.name} - {char.class_type.name} Niv.{char.level} "
              f"(HP: {char.hit_points}/{char.max_hit_points})")

    print("\n👹  MONSTRES:")
    for i, monster in enumerate(monsters, 1):
        print(f"  {i}. {monster.name} - CR {monster.challenge_rating} "
              f"(HP: {monster.hit_points}/{monster.max_hit_points})")

    # Calculer la difficulté
    party_levels = [char.level for char in party]
    monster_crs = [m.challenge_rating for m in monsters]
    adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

    print(f"\n📊  Difficulté de la rencontre: {difficulty.upper()} ({adjusted_xp} XP ajusté)")
    print("=" * 80)
    print()

    round_num = 1
    max_rounds = 30

    # Boucle de combat
    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'='*80}")
        print(f"  ROUND {round_num}")
        print(f"{'='*80}")

        # Phase 1: Tours des personnages
        print("\n--- Phase des Aventuriers ---")
        for char in alive_chars[:]:
            if not alive_monsters:
                break

            # Déterminer si le personnage est en ligne de front ou arrière
            is_front_line = char in front_line

            # Les personnages de la ligne arrière ne peuvent attaquer que les monstres
            # qui ne sont pas en mêlée avec la ligne de front (simplifié)
            if is_front_line:
                # Attaque de mêlée sur un monstre aléatoire
                target = choice(alive_monsters)
            else:
                # Attaque à distance ou sort sur un monstre aléatoire
                target = choice(alive_monsters)

            print(f"\n{char.name} ({char.class_type.name}):")

            # Utiliser le système de combat (simplifié)
            combat.character_turn(
                character=char,
                alive_chars=alive_chars,
                alive_monsters=alive_monsters,
                party=party
            )

        # Phase 2: Tours des monstres
        if alive_chars and alive_monsters:
            print("\n--- Phase des Monstres ---")
            for monster in alive_monsters[:]:
                if not alive_chars:
                    break

                print(f"\n{monster.name}:")

                # Les monstres attaquent prioritairement la ligne de front
                # S'il n'y a plus personne au front, ils attaquent l'arrière
                front_alive = [c for c in front_line if c in alive_chars]
                back_alive = [c for c in back_line if c in alive_chars]

                combat.monster_turn(
                    monster=monster,
                    alive_monsters=alive_monsters,
                    alive_chars=alive_chars,
                    party=party,
                    round_num=round_num
                )

        round_num += 1

        # Afficher l'état après chaque round
        print(f"\n--- État après le round {round_num - 1} ---")
        if alive_chars:
            print("Aventuriers survivants:")
            for char in alive_chars:
                status = "💀" if char.hit_points <= 0 else "✓"
                print(f"  {status} {char.name}: {char.hit_points}/{char.max_hit_points} HP")

        if alive_monsters:
            print("Monstres survivants:")
            for monster in alive_monsters:
                status = "💀" if monster.hit_points <= 0 else "✓"
                print(f"  {status} {monster.name}: {monster.hit_points}/{monster.max_hit_points} HP")

    # Résultats finaux
    print("\n" + "=" * 80)
    print("  RÉSULTAT DU COMBAT")
    print("=" * 80)

    if alive_chars and not alive_monsters:
        print("\n🎉 VICTOIRE! Les aventuriers ont triomphé!")
        print("\nSurvivants:")
        for char in alive_chars:
            print(f"  ✓ {char.name} ({char.class_type.name}): {char.hit_points}/{char.max_hit_points} HP")

        if len(alive_chars) < len(party):
            print("\nPertes:")
            for char in party:
                if char not in alive_chars:
                    print(f"  💀 {char.name} ({char.class_type.name}) est tombé au combat...")

    elif alive_monsters and not alive_chars:
        print("\n💀 DÉFAITE! Tous les aventuriers ont été vaincus...")
        print("\nMonstres survivants:")
        for monster in alive_monsters:
            print(f"  {monster.name}: {monster.hit_points}/{monster.max_hit_points} HP")

    elif round_num > max_rounds:
        print("\n⏱️  MATCH NUL! Le combat a duré trop longtemps...")

    else:
        print("\n🤝 ÉGALITÉ! Les deux camps ont été anéantis...")

    print("=" * 80)


def main():
    """Programme principal"""
    print("=" * 80)
    print("  GÉNÉRATEUR DE COMBAT ALÉATOIRE D&D 5e")
    print("=" * 80)
    print()

    # Charger les collections
    print("Chargement des données de personnages...")
    (races, subraces, classes, alignments, equipments,
     proficiencies, names, human_names, spells) = load_character_collections()
    print(f"✓ {len(races)} races, {len(classes)} classes, {len(spells)} sorts chargés")

    # Charger les monstres
    monsters_db = load_monsters_database()

    # Créer le groupe de 6 aventuriers avec niveaux variés
    print("\nCréation du groupe d'aventuriers...")
    party = create_random_party(
        size=6,
        races=races,
        subraces=subraces,
        classes=classes,
        names=names,
        human_names=human_names,
        spells=spells,
        min_level=1,
        max_level=5
    )
    print(f"✓ Groupe de {len(party)} aventuriers créé")

    # Sélectionner les monstres en fonction du CR
    print("\nSélection des monstres pour une rencontre équilibrée...")
    party_levels = [char.level for char in party]
    monsters = select_monsters_for_encounter(
        party_levels=party_levels,
        monsters_db=monsters_db,
        difficulty="medium"  # Peut être 'easy', 'medium', 'hard', ou 'deadly'
    )
    print(f"✓ {len(monsters)} monstre(s) sélectionné(s)")

    # Lancer le combat
    input("\nAppuyez sur Entrée pour commencer le combat...")
    run_combat(party, monsters)


if __name__ == "__main__":
    main()

