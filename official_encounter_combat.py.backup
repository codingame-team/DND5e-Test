"""
Combat Avancé Utilisant le Nouveau Système de Rencontres D&D 5e
Basé sur les tables officielles du Dungeon Master's Guide
"""
import sys
sys.path.insert(0, '/Users/display/PycharmProjects/DnD-5th-Edition-API')

from main import (
    generate_random_character,
    load_character_collections,
    request_monster,
    populate
)

from dnd_5e_core import Monster, Character
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.mechanics import (
    select_monsters_by_encounter_table,
    generate_encounter_distribution,
    get_encounter_info,
    calculate_encounter_difficulty
)
from random import randint
from typing import List


def load_monsters_database() -> List[Monster]:
    """Charger tous les monstres disponibles"""
    print("⏳ Chargement des monstres...")
    monster_names = populate(collection_name="monsters", key_name="results")
    monsters = []
    for name in monster_names:
        monster = request_monster(name)
        if monster:
            monsters.append(monster)
    print(f"✓ {len(monsters)} monstres chargés")
    return monsters


def create_random_party(
    size: int,
    races: List,
    subraces: List,
    classes: List,
    names: dict,
    human_names: dict,
    spells: List,
    min_level: int = 2,
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

        level = randint(min_level, max_level)
        char.level = level
        char.max_hit_points = (char.class_type.hit_die + char.ability_modifiers.con) * level
        char.hit_points = char.max_hit_points
        char.combat_role = "front" if i < 3 else "back"

        party.append(char)
        roster.append(char)

    return party


def display_encounter_info(party_level: int):
    """Afficher les informations de rencontre pour un niveau"""
    info = get_encounter_info(party_level)

    print(f"\n📋 Informations de rencontre (Niveau {party_level}):")
    print(f"   Paires possibles: CR {float(info['pair_crs'][0])} + CR {float(info['pair_crs'][1])}")
    print(f"   Options de groupes:")
    for size, crs in info['group_options'].items():
        cr_list = ', '.join([str(float(cr)) for cr in crs])
        print(f"      {size} monstres: CR {cr_list}")


def run_dnd_encounter_combat(party: List[Character], monsters_db: List[Monster]):
    """
    Exécuter un combat avec le système de rencontres D&D 5e exact
    """
    combat = CombatSystem(verbose=True)

    front_line = [c for c in party if getattr(c, 'combat_role', 'front') == 'front']
    back_line = [c for c in party if getattr(c, 'combat_role', 'back') == 'back']

    alive_chars = party.copy()

    # Calculer le niveau moyen du groupe
    party_levels = [char.level for char in party]
    avg_level = sum(party_levels) / len(party_levels)
    party_level = round(avg_level)

    print("\n" + "=" * 80)
    print("  ⚔️  COMBAT D&D 5e - SYSTÈME DE RENCONTRES OFFICIEL  ⚔️")
    print("=" * 80)

    print(f"\n👥 GROUPE D'AVENTURIERS (Niveau moyen: {avg_level:.1f})")
    print("─" * 80)

    print("\n🗡️  Ligne de Front:")
    for char in front_line:
        print(f"   • {char.name:<20} {char.race.name:<12} {char.class_type.name:<10} Niv.{char.level} "
              f"HP: {char.hit_points}/{char.max_hit_points}")

    print("\n🏹 Ligne Arrière:")
    for char in back_line:
        spell_info = ""
        if hasattr(char, 'sc') and char.sc and hasattr(char.sc, 'learned_spells'):
            spell_count = len(char.sc.learned_spells)
            if spell_count > 0:
                spell_info = f" ({spell_count} sorts)"
        print(f"   • {char.name:<20} {char.race.name:<12} {char.class_type.name:<10} Niv.{char.level} "
              f"HP: {char.hit_points}/{char.max_hit_points}{spell_info}")

    # Afficher les infos de rencontre possibles
    display_encounter_info(party_level)

    # Générer une rencontre selon les règles D&D 5e
    print(f"\n🎲 Génération de la rencontre selon les tables D&D 5e...")
    monsters, encounter_type = select_monsters_by_encounter_table(
        encounter_level=party_level,
        available_monsters=monsters_db,
        spell_casters_only=False,
        allow_pairs=True
    )

    if not monsters:
        print("❌ Impossible de générer une rencontre appropriée!")
        return

    alive_monsters = monsters.copy()

    # Afficher la rencontre générée
    print("\n👹 RENCONTRE GÉNÉRÉE:")
    print("─" * 80)

    if encounter_type == "pair":
        print(f"   Type: PAIRE de monstres différents")
        print(f"   1. {monsters[0].name} (CR {monsters[0].challenge_rating}) - "
              f"HP: {monsters[0].hit_points}/{monsters[0].max_hit_points}")
        print(f"   2. {monsters[1].name} (CR {monsters[1].challenge_rating}) - "
              f"HP: {monsters[1].hit_points}/{monsters[1].max_hit_points}")
    else:
        print(f"   Type: GROUPE de {len(monsters)} {monsters[0].name}")
        for i, monster in enumerate(monsters, 1):
            print(f"   {i}. {monster.name} (CR {monster.challenge_rating}) - "
                  f"HP: {monster.hit_points}/{monster.max_hit_points}")

    # Calculer la difficulté
    monster_crs = [m.challenge_rating for m in monsters]
    adjusted_xp, difficulty = calculate_encounter_difficulty(party_levels, monster_crs)

    total_party_hp = sum(c.max_hit_points for c in party)
    total_monster_hp = sum(m.max_hit_points for m in monsters)

    print(f"\n📊 ANALYSE DE LA RENCONTRE:")
    print(f"   Difficulté: {difficulty.upper()}")
    print(f"   XP ajustés: {adjusted_xp}")
    print(f"   HP total groupe: {total_party_hp}")
    print(f"   HP total monstres: {total_monster_hp}")
    print(f"   Rapport de force: {total_party_hp / total_monster_hp:.2f}:1")

    print("\n" + "=" * 80)

    input("\n⏸️  Appuyez sur Entrée pour commencer le combat...")

    round_num = 1
    max_rounds = 30

    # Boucle de combat
    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'='*80}")
        print(f"  ⚔️  ROUND {round_num}  ⚔️")
        print(f"{'='*80}")

        # Phase aventuriers
        print("\n--- 🗡️  Phase des Aventuriers ---\n")
        for char in alive_chars[:]:
            if not alive_monsters:
                break

            is_front = char in front_line
            role = "FRONT" if is_front else "ARRIÈRE"
            print(f"➤ {char.name} ({char.class_type.name} Niv.{char.level}) [{role}]:")

            combat.character_turn(
                character=char,
                alive_chars=alive_chars,
                alive_monsters=alive_monsters,
                party=party
            )

        # Phase monstres
        if alive_chars and alive_monsters:
            print("\n--- 👹  Phase des Monstres ---\n")
            for monster in alive_monsters[:]:
                if not alive_chars:
                    break

                print(f"➤ {monster.name} (CR {monster.challenge_rating}):")

                combat.monster_turn(
                    monster=monster,
                    alive_monsters=alive_monsters,
                    alive_chars=alive_chars,
                    party=party,
                    round_num=round_num
                )

        round_num += 1

        # État après chaque round
        if round_num % 2 == 0:  # Afficher tous les 2 rounds
            print(f"\n{'─'*80}")
            print(f"  📊  ÉTAT APRÈS LE ROUND {round_num - 1}")
            print(f"{'─'*80}")

            if alive_chars:
                print("✅ Aventuriers:")
                for char in alive_chars:
                    hp_percent = (char.hit_points / char.max_hit_points) * 100
                    status = "🟢" if hp_percent > 50 else ("🟡" if hp_percent > 25 else "🔴")
                    print(f"   {status} {char.name:<20} {char.hit_points:>3}/{char.max_hit_points:<3} HP")

            if alive_monsters:
                print("👹 Monstres:")
                for monster in alive_monsters:
                    hp_percent = (monster.hit_points / monster.max_hit_points) * 100
                    status = "🟢" if hp_percent > 50 else ("🟡" if hp_percent > 25 else "🔴")
                    print(f"   {status} {monster.name:<20} {monster.hit_points:>3}/{monster.max_hit_points:<3} HP")

    # Résultats
    print("\n" + "=" * 80)
    print("  🏆  RÉSULTAT FINAL  🏆")
    print("=" * 80)

    if alive_chars and not alive_monsters:
        print("\n🎉 ✨ VICTOIRE! ✨")
        survivors = len(alive_chars)
        casualties = len(party) - survivors
        survival_rate = (survivors / len(party)) * 100

        print(f"\n📊  Statistiques:")
        print(f"   Survivants: {survivors}/{len(party)} ({survival_rate:.0f}%)")
        print(f"   Pertes: {casualties}/{len(party)}")
        print(f"   Rounds: {round_num - 1}")
        print(f"   XP gagnés: {adjusted_xp} (à répartir)")

        if alive_chars:
            xp_per_char = adjusted_xp // len(alive_chars)
            print(f"\n✅ Survivants (+{xp_per_char} XP chacun):")
            for char in alive_chars:
                hp_percent = (char.hit_points / char.max_hit_points) * 100
                print(f"   ✓ {char.name:<20} {char.hit_points:>3}/{char.max_hit_points:<3} HP ({hp_percent:.0f}%)")

    elif alive_monsters and not alive_chars:
        print("\n💀 DÉFAITE TOTALE!")
        print(f"\n   Le groupe a été anéanti après {round_num - 1} rounds...")

    elif round_num > max_rounds:
        print("\n⏱️  TIMEOUT!")
        print(f"\n   Combat interrompu après {max_rounds} rounds")

    else:
        print("\n💥 DESTRUCTION MUTUELLE!")

    print("=" * 80)


def main():
    """Programme principal"""
    print("\n" + "=" * 80)
    print("  🎲  COMBAT D&D 5e - SYSTÈME DE RENCONTRES OFFICIEL  🎲")
    print("=" * 80)
    print("\n  Utilise les tables de rencontres du Dungeon Master's Guide")
    print("  Génère des rencontres équilibrées selon les règles officielles")
    print("=" * 80)

    # Charger les données
    print("\n📚 Chargement des données...")
    (races, subraces, classes, _, _, _, names, human_names, spells) = load_character_collections()
    print(f"✓ {len(races)} races, {len(classes)} classes, {len(spells)} sorts")

    monsters_db = load_monsters_database()

    # Créer le groupe
    print("\n⚔️  Génération du groupe d'aventuriers...")
    party = create_random_party(
        size=6,
        races=races,
        subraces=subraces,
        classes=classes,
        names=names,
        human_names=human_names,
        spells=spells,
        min_level=3,
        max_level=6
    )
    print(f"✓ Groupe de {len(party)} aventuriers généré")

    # Lancer le combat
    run_dnd_encounter_combat(party, monsters_db)


if __name__ == "__main__":
    main()

