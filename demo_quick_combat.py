#!/usr/bin/env python3
"""
DEMO RAPIDE - Combat D&D 5e avec personnages aléatoires
Lance un combat rapide pour démonstration
"""
import sys
sys.path.insert(0, '/Users/display/PycharmProjects/DnD-5th-Edition-API')

from main import generate_random_character, load_character_collections, request_monster, populate
from dnd_5e_core import Monster, Character
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.mechanics import calculate_encounter_difficulty
from random import choice, randint


def quick_demo():
    """Démonstration rapide d'un combat"""

    print("\n" + "="*80)
    print("  🎲 DÉMO RAPIDE - Combat D&D 5e avec Personnages Aléatoires 🎲")
    print("="*80)
    print("\n  Cette démo crée 6 aventuriers aléatoires et les fait combattre")
    print("  contre des monstres sélectionnés selon leur niveau.\n")
    print("="*80)

    # Chargement silencieux
    print("\n⏳ Chargement des données...", end="", flush=True)
    (races, subraces, classes, _, _, _, names, human_names, spells) = load_character_collections()
    print(" ✓")

    print("⏳ Chargement des monstres...", end="", flush=True)
    monster_names = populate(collection_name="monsters", key_name="results")
    monsters_db = [request_monster(name) for name in monster_names if request_monster(name)]
    print(" ✓")

    # Créer 6 personnages aléatoires
    print("\n⚔️  Création de 6 aventuriers aléatoires...\n")
    party = []
    roster = []

    for i in range(6):
        char = generate_random_character(roster, races, subraces, classes, names, human_names, spells)
        level = randint(2, 4)
        char.level = level
        char.max_hit_points = (char.class_type.hit_die + char.ability_modifiers.con) * level
        char.hit_points = char.max_hit_points
        char.combat_role = "front" if i < 3 else "back"

        role_icon = "🗡️" if i < 3 else "🏹"
        print(f"   {role_icon} {char.name:<18} ({char.race.name} {char.class_type.name} Niv.{level}) "
              f"HP: {char.hit_points}")

        party.append(char)
        roster.append(char)

    # Sélectionner 2-3 monstres
    print("\n👹 Sélection des adversaires...\n")
    party_levels = [c.level for c in party]
    avg_level = sum(party_levels) / len(party_levels)

    suitable_monsters = [m for m in monsters_db if 0.5 <= m.challenge_rating <= avg_level + 1]
    num_monsters = randint(2, 3)
    monsters = [choice(suitable_monsters) for _ in range(num_monsters)]

    for i, m in enumerate(monsters, 1):
        print(f"   👹 {m.name:<20} (CR {m.challenge_rating}) HP: {m.hit_points}")

    # Calculer difficulté
    monster_crs = [m.challenge_rating for m in monsters]
    adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

    print(f"\n📊 Difficulté: {difficulty.upper()} ({adjusted_xp} XP)")
    print("\n" + "="*80)

    input("\n⏸️  Appuyez sur Entrée pour lancer le combat...\n")

    # Combat
    combat = CombatSystem(verbose=True)
    alive_chars = party.copy()
    alive_monsters = monsters.copy()

    round_num = 1
    max_rounds = 20

    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'='*80}")
        print(f"  ⚔️  ROUND {round_num}  ⚔️")
        print(f"{'='*80}\n")

        # Aventuriers
        for char in alive_chars[:]:
            if not alive_monsters:
                break
            combat.character_turn(char, alive_chars, alive_monsters, party)

        # Monstres
        if alive_chars and alive_monsters:
            for monster in alive_monsters[:]:
                if not alive_chars:
                    break
                combat.monster_turn(monster, alive_monsters, alive_chars, party, round_num)

        round_num += 1

        # État
        if round_num % 3 == 0 or not (alive_chars and alive_monsters):  # Afficher tous les 3 rounds
            print(f"\n--- État (Round {round_num-1}) ---")
            if alive_chars:
                for c in alive_chars:
                    hp_pct = (c.hit_points / c.max_hit_points) * 100
                    status = "🟢" if hp_pct > 50 else ("🟡" if hp_pct > 25 else "🔴")
                    print(f"  {status} {c.name}: {c.hit_points}/{c.max_hit_points} HP")
            if alive_monsters:
                for m in alive_monsters:
                    hp_pct = (m.hit_points / m.max_hit_points) * 100
                    status = "🟢" if hp_pct > 50 else ("🟡" if hp_pct > 25 else "🔴")
                    print(f"  {status} {m.name}: {m.hit_points}/{m.max_hit_points} HP")

    # Résultat
    print("\n" + "="*80)
    print("  🏆 RÉSULTAT 🏆")
    print("="*80)

    if alive_chars and not alive_monsters:
        print(f"\n🎉 VICTOIRE! ({len(alive_chars)}/{len(party)} survivants)")
        for c in alive_chars:
            print(f"  ✓ {c.name} ({c.hit_points}/{c.max_hit_points} HP)")
        print(f"\n💰 {adjusted_xp} XP à répartir entre les survivants")
    elif alive_monsters and not alive_chars:
        print("\n💀 DÉFAITE! Tous les aventuriers sont tombés...")
    else:
        print("\n⏱️  MATCH NUL ou TIMEOUT")

    print("="*80 + "\n")


if __name__ == "__main__":
    quick_demo()

