"""
Combat automatique avec un groupe de 6 aventuriers aléatoires vs monstres
Version simplifiée qui lance le combat automatiquement
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
    print(f"✓ {len(monsters)} monstres chargés.")
    return monsters


def select_monsters_for_encounter(
    party_levels: List[int],
    monsters_db: List[Monster],
    difficulty: str = "medium"
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
    max_attempts = 50
    attempts = 0

    while attempts < max_attempts:
        monster = choice(suitable_monsters)
        test_monsters = selected_monsters + [monster]

        monster_crs = [m.challenge_rating for m in test_monsters]
        adjusted_xp, calc_difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

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
            break

        attempts += 1

        if len(selected_monsters) >= 8:
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

        # Ajuster les HP
        char.max_hit_points = (char.class_type.hit_die + char.ability_modifiers.con) * level
        char.hit_points = char.max_hit_points

        party.append(char)
        roster.append(char)

    return party


def display_party_info(party: List[Character]):
    """Afficher les informations du groupe"""
    front_line = party[:3]
    back_line = party[3:]

    print("\n🗡️  LIGNE DE FRONT (Attaques de mêlée):")
    for i, char in enumerate(front_line, 1):
        weapons = "Aucune arme"
        if hasattr(char, 'inventory') and char.inventory:
            equipped_weapons = [item for item in char.inventory if item and hasattr(item, 'equipped') and item.equipped]
            if equipped_weapons:
                weapons = ", ".join([w.name for w in equipped_weapons])

        print(f"  {i}. {char.name} ({char.race.name} {char.class_type.name} Niv.{char.level})")
        print(f"     HP: {char.hit_points}/{char.max_hit_points} | "
              f"STR: {char.abilities.str} DEX: {char.abilities.dex} CON: {char.abilities.con}")
        print(f"     Armes: {weapons}")

    print("\n🏹  LIGNE ARRIÈRE (Attaques à distance et sorts):")
    for i, char in enumerate(back_line, 1):
        spell_info = "Pas de magie"
        if hasattr(char, 'sc') and char.sc:
            spell_count = len(char.sc.learned_spells) if hasattr(char.sc, 'learned_spells') else 0
            spell_info = f"{spell_count} sorts connus"

        print(f"  {i}. {char.name} ({char.race.name} {char.class_type.name} Niv.{char.level})")
        print(f"     HP: {char.hit_points}/{char.max_hit_points} | "
              f"INT: {char.abilities.int} WIS: {char.abilities.wis} CHA: {char.abilities.cha}")
        print(f"     Magie: {spell_info}")


def run_combat(party: List[Character], monsters: List[Monster]):
    """Exécuter le combat entre le groupe et les monstres"""
    combat = CombatSystem(verbose=True)

    front_line = party[:3]
    back_line = party[3:]

    alive_chars = party.copy()
    alive_monsters = monsters.copy()

    # Affichage initial
    print("\n" + "=" * 80)
    print("  ⚔️  DÉBUT DU COMBAT  ⚔️")
    print("=" * 80)

    display_party_info(party)

    print("\n👹  MONSTRES:")
    for i, monster in enumerate(monsters, 1):
        print(f"  {i}. {monster.name} - CR {monster.challenge_rating} | "
              f"HP: {monster.hit_points}/{monster.max_hit_points} | "
              f"CA: {monster.armor_class}")

    # Calculer la difficulté
    party_levels = [char.level for char in party]
    monster_crs = [m.challenge_rating for m in monsters]
    adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

    print(f"\n📊  Difficulté: {difficulty.upper()} ({adjusted_xp} XP ajusté)")
    print("=" * 80)

    round_num = 1
    max_rounds = 30

    # Boucle de combat
    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'='*80}")
        print(f"  ROUND {round_num}")
        print(f"{'='*80}")

        # Phase 1: Tours des personnages
        print("\n--- ⚔️  Phase des Aventuriers ---")
        for char in alive_chars[:]:
            if not alive_monsters:
                break

            print(f"\n{char.name} ({char.class_type.name} Niv.{char.level}):")

            combat.character_turn(
                character=char,
                alive_chars=alive_chars,
                alive_monsters=alive_monsters,
                party=party
            )

        # Phase 2: Tours des monstres
        if alive_chars and alive_monsters:
            print("\n--- 👹  Phase des Monstres ---")
            for monster in alive_monsters[:]:
                if not alive_chars:
                    break

                print(f"\n{monster.name} (CR {monster.challenge_rating}):")

                combat.monster_turn(
                    monster=monster,
                    alive_monsters=alive_monsters,
                    alive_chars=alive_chars,
                    party=party,
                    round_num=round_num
                )

        round_num += 1

        # Afficher l'état après chaque round
        print(f"\n--- 📊  État après le round {round_num - 1} ---")
        if alive_chars:
            print("✅ Aventuriers survivants:")
            for char in alive_chars:
                hp_percent = (char.hit_points / char.max_hit_points) * 100
                status = "🟢" if hp_percent > 50 else ("🟡" if hp_percent > 25 else "🔴")
                print(f"  {status} {char.name}: {char.hit_points}/{char.max_hit_points} HP ({hp_percent:.0f}%)")

        if alive_monsters:
            print("👹 Monstres survivants:")
            for monster in alive_monsters:
                hp_percent = (monster.hit_points / monster.max_hit_points) * 100
                status = "🟢" if hp_percent > 50 else ("🟡" if hp_percent > 25 else "🔴")
                print(f"  {status} {monster.name}: {monster.hit_points}/{monster.max_hit_points} HP ({hp_percent:.0f}%)")

    # Résultats finaux
    print("\n" + "=" * 80)
    print("  🏆  RÉSULTAT DU COMBAT  🏆")
    print("=" * 80)

    if alive_chars and not alive_monsters:
        print("\n🎉 VICTOIRE! Les aventuriers ont triomphé!")
        print(f"\n✅ Survivants ({len(alive_chars)}/{len(party)}):")
        for char in alive_chars:
            hp_percent = (char.hit_points / char.max_hit_points) * 100
            print(f"  ✓ {char.name} ({char.class_type.name}): "
                  f"{char.hit_points}/{char.max_hit_points} HP ({hp_percent:.0f}%)")

        if len(alive_chars) < len(party):
            print(f"\n💀 Pertes ({len(party) - len(alive_chars)}/{len(party)}):")
            for char in party:
                if char not in alive_chars:
                    print(f"  ✝ {char.name} ({char.class_type.name}) est tombé au combat...")

        print(f"\n💰 XP gagnés: {adjusted_xp} (à répartir entre les survivants)")

    elif alive_monsters and not alive_chars:
        print("\n💀 DÉFAITE TOTALE! Tous les aventuriers ont été vaincus...")
        print("\n👹 Monstres survivants:")
        for monster in alive_monsters:
            print(f"  {monster.name}: {monster.hit_points}/{monster.max_hit_points} HP")

    elif round_num > max_rounds:
        print("\n⏱️  COMBAT INTERMINABLE! Le combat a duré trop longtemps...")
        print(f"Survivants: {len(alive_chars)} aventuriers, {len(alive_monsters)} monstres")

    else:
        print("\n💥 DESTRUCTION MUTUELLE! Les deux camps ont été anéantis...")

    print("=" * 80)


def main():
    """Programme principal"""
    print("=" * 80)
    print("  🎲  GÉNÉRATEUR DE COMBAT ALÉATOIRE D&D 5e  🎲")
    print("=" * 80)

    # Charger les collections
    print("\n📚 Chargement des données...")
    (races, subraces, classes, alignments, equipments,
     proficiencies, names, human_names, spells) = load_character_collections()
    print(f"✓ {len(races)} races, {len(classes)} classes, {len(spells)} sorts")

    # Charger les monstres
    monsters_db = load_monsters_database()

    # Créer le groupe de 6 aventuriers
    print("\n⚔️  Création du groupe d'aventuriers...")
    party = create_random_party(
        size=6,
        races=races,
        subraces=subraces,
        classes=classes,
        names=names,
        human_names=human_names,
        spells=spells,
        min_level=2,  # Niveau minimum 2 pour plus de fun
        max_level=5   # Niveau maximum 5
    )
    print(f"✓ Groupe de {len(party)} aventuriers créé")

    # Sélectionner les monstres
    print("\n👹 Sélection des monstres...")
    party_levels = [char.level for char in party]
    avg_level = sum(party_levels) / len(party_levels)
    print(f"   Niveau moyen du groupe: {avg_level:.1f}")

    monsters = select_monsters_for_encounter(
        party_levels=party_levels,
        monsters_db=monsters_db,
        difficulty="medium"  # 'easy', 'medium', 'hard', ou 'deadly'
    )
    print(f"✓ {len(monsters)} monstre(s) sélectionné(s)")

    # Lancer le combat
    run_combat(party, monsters)


if __name__ == "__main__":
    main()

