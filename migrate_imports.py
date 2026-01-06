#!/usr/bin/env python3
"""
Script de migration automatique - Remplace les imports de main.py par dnd-5e-core
"""
import os
import re
from pathlib import Path

# Fichiers à migrer
FILES_TO_MIGRATE = [
    "advanced_random_combat.py",
    "random_party_combat.py",
    "demo_quick_combat.py",
    "official_encounter_combat.py",
    "demo_encounter_systems.py",
    "create_character.py",
    "create_monster.py",
]

def migrate_file(filepath):
    """Migrer un fichier pour utiliser dnd-5e-core au lieu de main.py"""
    print(f"\n🔄 Migration de {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Supprimer sys.path.insert
    content = re.sub(
        r'import sys\s+sys\.path\.insert\(0,\s*[\'"][^\'"]+[\'"]\)\s*',
        '',
        content
    )

    # Remplacer les imports de main
    replacements = {
        'from main import': 'from dnd_5e_core.data import',
        'generate_random_character': 'simple_character_generator',
        'load_character_collections': '# load_character_collections removed',
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    # Supprimer les appels à load_character_collections
    content = re.sub(
        r'\(races,\s*subraces,\s*classes,.*?\)\s*=\s*load_character_collections\(\)\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # Simplifier generate_random_character -> simple_character_generator
    content = re.sub(
        r'simple_character_generator\([^)]*roster[^)]*\)',
        'simple_character_generator(level=randint(2, 5))',
        content
    )

    if content != original_content:
        # Sauvegarder le backup
        backup_path = filepath + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)

        # Écrire le nouveau contenu
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Migré (backup: {backup_path})")
        return True
    else:
        print(f"  ℹ️  Aucun changement nécessaire")
        return False

def main():
    print("="*80)
    print("  MIGRATION AUTOMATIQUE - main.py → dnd-5e-core")
    print("="*80)

    os.chdir('/Users/display/PycharmProjects/DnD5e-Test')

    migrated_count = 0
    for filename in FILES_TO_MIGRATE:
        if os.path.exists(filename):
            if migrate_file(filename):
                migrated_count += 1
        else:
            print(f"⚠️  Fichier non trouvé: {filename}")

    print(f"\n{'='*80}")
    print(f"  ✅ Migration terminée: {migrated_count}/{len(FILES_TO_MIGRATE)} fichiers migrés")
    print(f"{'='*80}")
    print("\nPour restaurer un fichier:")
    print("  mv <filename>.backup <filename>")

if __name__ == "__main__":
    main()

