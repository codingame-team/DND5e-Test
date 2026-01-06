#!/usr/bin/env python3
"""
Liste tous les scripts de combat disponibles
"""

import os
from pathlib import Path

print("\n" + "="*80)
print("  📚 SCRIPTS DE COMBAT D&D 5e - LISTE COMPLÈTE")
print("="*80)

scripts = [
    {
        "file": "combat.py",
        "name": "Combat Simple",
        "desc": "1 personnage vs 1 monstre (manuel)",
        "level": "⭐",
        "auto": "✅",
        "random": "❌"
    },
    {
        "file": "party_combat.py",
        "name": "Combat de Groupe",
        "desc": "6 personnages vs monstres (manuel)",
        "level": "⭐⭐",
        "auto": "✅",
        "random": "❌"
    },
    {
        "file": "random_party_combat.py",
        "name": "Combat Aléatoire",
        "desc": "6 personnages aléatoires vs monstres",
        "level": "⭐⭐⭐",
        "auto": "❌",
        "random": "✅"
    },
    {
        "file": "auto_random_combat.py",
        "name": "Combat Auto Aléatoire",
        "desc": "6 personnages aléatoires (auto)",
        "level": "⭐⭐⭐",
        "auto": "✅",
        "random": "✅"
    },
    {
        "file": "advanced_random_combat.py",
        "name": "Combat Avancé",
        "desc": "Version complète avec stats détaillées",
        "level": "⭐⭐⭐⭐",
        "auto": "❌",
        "random": "✅"
    },
    {
        "file": "demo_quick_combat.py",
        "name": "Démo Rapide",
        "desc": "Démonstration condensée",
        "level": "⭐",
        "auto": "❌",
        "random": "✅"
    },
]

print("\n📋 Scripts de Combat:\n")
print(f"{'N°':<4} {'Fichier':<30} {'Auto':<6} {'Aléa':<6} {'Niveau':<8}")
print("─" * 80)

for i, script in enumerate(scripts, 1):
    exists = "✓" if os.path.exists(script['file']) else "✗"
    print(f"{i:<4} {script['file']:<30} {script['auto']:<6} {script['random']:<6} {script['level']:<8} {exists}")
    print(f"     └─ {script['desc']}")
    print()

print("─" * 80)
print("\n📖 Documentation:\n")

docs = [
    ("README_COMBAT.md", "Guide complet de tous les scripts"),
    ("SUMMARY_RANDOM_COMBAT.md", "Résumé du projet et personnalisation"),
]

for doc, desc in docs:
    exists = "✓" if os.path.exists(doc) else "✗"
    size = ""
    if os.path.exists(doc):
        size_bytes = os.path.getsize(doc)
        size = f"({size_bytes/1024:.1f}K)"
    print(f"  {exists} {doc:<30} {size:<10} - {desc}")

print("\n" + "="*80)
print("\n💡 RECOMMANDATIONS:\n")
print("  🎬 Première fois?       → python demo_quick_combat.py")
print("  🧪 Tests automatiques?  → python auto_random_combat.py")
print("  ⚔️  Simulation complète? → python advanced_random_combat.py")
print("\n" + "="*80)
print()

