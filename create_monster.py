from dnd_5e_core.entities import get_extended_monster_loader

# Load the monster loader
loader = get_extended_monster_loader()

# Search for monsters
goblins = loader.search_monsters(name_contains="dragon", min_cr=1, max_cr=3)
for g in goblins:
	print(g)
print(f"Found {len(goblins)} goblin variants")

# Get a specific monster with full data
orc_eye = loader.get_monster_by_name("Orc Eye of Gruumsh")
print(f"{orc_eye['name']} - CR {orc_eye['cr']}")
print(f"HP: {orc_eye['hp']['average']}, Source: {orc_eye['source']}")

# Get statistics
stats = loader.get_stats()
print(f"Total extended monsters: {stats['total']}")
print(f"Sources: {list(stats['by_source'].keys())}")

# Download monster tokens
from dnd_5e_core.utils import download_monster_token

download_monster_token("Orc Eye of Gruumsh", source="MM", save_folder="tokens")