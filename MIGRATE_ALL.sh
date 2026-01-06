#!/bin/bash
echo "=================================================================="
echo "  MIGRATION AUTOMATIQUE - Suppression dépendances main.py"
echo "=================================================================="
# Liste des fichiers à migrer
FILES=(
    "advanced_random_combat.py"
    "random_party_combat.py"  
    "demo_quick_combat.py"
    "official_encounter_combat.py"
    "demo_encounter_systems.py"
)
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo ""
        echo "🔄 Migration de $file..."
        # Créer backup
        cp "$file" "${file}.backup"
        # Supprimer sys.path.insert et import main
        sed -i '' '/sys\.path\.insert/d' "$file"
        sed -i '' 's/from main import/from dnd_5e_core.data import/g' "$file"
        sed -i '' 's/generate_random_character/simple_character_generator/g' "$file"
        sed -i '' '/load_character_collections/d' "$file"
        echo "✅ Migré (backup: ${file}.backup)"
    else
        echo "⚠️  Fichier non trouvé:            fi
done
echo ""
echo "=================================================================="
echo "  ✅ Migration terminée"
echo "=================================================================="
