"""
Démonstration et comparaison des deux systèmes de génération de rencontres:
1. Système simplifié (ancien): get_appropriate_cr_range
2. Système basé sur les tables D&D 5e (nouveau): select_monsters_by_encounter_table
"""
import sys
sys.path.insert(0, '/Users/display/PycharmProjects/DnD-5th-Edition-API')

from dnd_5e_core.mechanics import (
    get_appropriate_cr_range,
    select_monsters_by_encounter_table,
    generate_encounter_distribution,
    get_encounter_info,
    ENCOUNTER_TABLE
)
from main import request_monster, populate
from fractions import Fraction


def demo_comparison():
    """Comparer les deux systèmes"""

    print("\n" + "=" * 80)
    print("  COMPARAISON DES SYSTÈMES DE GÉNÉRATION DE RENCONTRES")
    print("=" * 80)

    # Charger les monstres
    print("\n⏳ Chargement des monstres...")
    monster_names = populate(collection_name="monsters", key_name="results")
    monsters_db = []
    for name in monster_names:
        monster = request_monster(name)
        if monster:
            monsters_db.append(monster)
    print(f"✓ {len(monsters_db)} monstres chargés")

    # Tester pour différents niveaux de groupe
    test_levels = [1, 3, 5, 10, 15, 20]

    for party_level in test_levels:
        print("\n" + "=" * 80)
        print(f"  NIVEAU DU GROUPE: {party_level}")
        print("=" * 80)

        # Système 1: Simplifié (ancien)
        print("\n📊 SYSTÈME SIMPLIFIÉ (ancien):")
        print("─" * 80)
        min_cr, max_cr = get_appropriate_cr_range(party_level)
        print(f"   Range de CR: {min_cr} - {max_cr}")
        print(f"   Logique: party_level ± 3")

        suitable_monsters_old = [
            m for m in monsters_db
            if min_cr <= m.challenge_rating <= max_cr
        ]
        print(f"   Monstres correspondants: {len(suitable_monsters_old)}")

        # Afficher quelques exemples
        if suitable_monsters_old:
            examples = suitable_monsters_old[:5]
            print(f"   Exemples: {', '.join([f'{m.name} (CR {m.challenge_rating})' for m in examples])}")

        # Système 2: Table D&D 5e (nouveau)
        print("\n📋 SYSTÈME TABLE D&D 5e (nouveau):")
        print("─" * 80)

        # Obtenir les informations de rencontre
        encounter_info = get_encounter_info(party_level)
        pair_crs = encounter_info['pair_crs']
        group_options = encounter_info['group_options']

        print(f"   Paire de monstres: CR {float(pair_crs[0])} + CR {float(pair_crs[1])}")
        print(f"   Options de groupes:")
        for group_size, crs in group_options.items():
            cr_str = ', '.join([f"{float(cr)}" for cr in crs])
            print(f"      {group_size} monstres: CR [{cr_str}]")

        # Générer 3 exemples de rencontres
        print(f"\n   📌 Exemples de rencontres générées:")
        for i in range(3):
            monsters, encounter_type = select_monsters_by_encounter_table(
                party_level,
                monsters_db,
                spell_casters_only=False,
                allow_pairs=True
            )

            if monsters:
                if encounter_type == "pair":
                    print(f"      {i+1}. PAIRE: {monsters[0].name} (CR {monsters[0].challenge_rating}) "
                          f"+ {monsters[1].name} (CR {monsters[1].challenge_rating})")
                else:
                    print(f"      {i+1}. GROUPE: {len(monsters)}x {monsters[0].name} "
                          f"(CR {monsters[0].challenge_rating})")

        print("\n" + "─" * 80)
        print("   🔍 DIFFÉRENCES:")
        print("   - Ancien: Range simple ±3, pas de structure")
        print("   - Nouveau: Tables précises, paires ou groupes, suit les règles D&D 5e")

    print("\n" + "=" * 80)
    print("  DISTRIBUTION DES RENCONTRES (20 rencontres)")
    print("=" * 80)

    party_level = 5
    distribution = generate_encounter_distribution(party_level)

    print(f"\n   Pour un groupe de niveau {party_level}:")
    print(f"   Distribution: {distribution}")
    print(f"\n   Statistiques:")
    print(f"      Faciles (< {party_level}):  {len([e for e in distribution if e < party_level])} rencontres")
    print(f"      Moyennes (= {party_level}):  {len([e for e in distribution if e == party_level])} rencontres")
    print(f"      Difficiles (+1-4):   {len([e for e in distribution if party_level < e <= party_level + 4])} rencontres")
    print(f"      Mortelles (+5-20):   {len([e for e in distribution if e > party_level + 4])} rencontres")

    print("\n" + "=" * 80)
    print("  CONCLUSION")
    print("=" * 80)
    print("""
   Le NOUVEAU système (select_monsters_by_encounter_table) est SUPÉRIEUR car:
   
   ✅ Suit exactement les tables de rencontres D&D 5e officielles
   ✅ Prend en compte le nombre de monstres (paires, petits groupes, grands groupes)
   ✅ Ajuste les CR selon la taille du groupe
   ✅ Génère des rencontres plus équilibrées et variées
   ✅ Distribution de difficulté réaliste (30% facile, 50% moyen, 15% difficile, 5% mortel)
   
   L'ANCIEN système (get_appropriate_cr_range) est trop simpliste:
   
   ❌ Utilise seulement un range ±3
   ❌ Ne tient pas compte du nombre de monstres
   ❌ Pas de structure de groupe ou paire
   ❌ Peut générer des rencontres déséquilibrées
   
   RECOMMANDATION: Utiliser select_monsters_by_encounter_table pour vos scripts!
   """)

    print("=" * 80)


if __name__ == "__main__":
    demo_comparison()

