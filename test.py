import sys
from pathlib import Path

# Add the dnd-5e-core package to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "dnd-5e-core"))

from dnd_5e_core.data import load_monster, list_monsters, load_spell

# List all available monsters
monsters = list_monsters()
print(f"Total monsters: {len(monsters)}")  # 332

# Load a specific monster
goblin = load_monster('goblin')
if goblin:
    print(f"Name: {goblin['name']}")
    print(f"HP: {goblin['hit_points']}")
    print(f"CR: {goblin['challenge_rating']}")
else:
    print("Goblin not found!")

# Load a spell
fireball = load_spell('fireball')
if fireball:
    print(f"Spell: {fireball['name']}, Level: {fireball['level']}")
else:
    print("Fireball not found!")
