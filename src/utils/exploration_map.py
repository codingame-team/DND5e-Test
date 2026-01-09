"""
Système de carte et suivi d'exploration
"""
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class MapLocation:
    """Représente un lieu sur la carte"""
    id: str
    name: str
    x: int
    y: int
    type: str  # "village", "forest", "dungeon", "chamber", etc.
    description: str = ""
    discovered: bool = False
    visited: bool = False
    connections: List[str] = field(default_factory=list)


class ExplorationMap:
    """Gestionnaire de carte d'exploration"""

    def __init__(self, scenario_id: str):
        self.scenario_id = scenario_id
        self.locations: Dict[str, MapLocation] = {}
        self.current_location: Optional[str] = None
        self.discovered_locations: Set[str] = set()
        self.visited_locations: Set[str] = set()

        # Créer la carte selon le scénario
        self._build_map()

    def _build_map(self):
        """Construire la carte selon le scénario"""
        if self.scenario_id == "chasse_gobelins":
            self._build_goblin_hunt_map()
        elif self.scenario_id == "sunless_citadel":
            self._build_sunless_citadel_map()
        elif self.scenario_id == "tombe_rois_serpents":
            self._build_tomb_map()

    def _build_goblin_hunt_map(self):
        """Carte: La Chasse aux Gobelins"""
        locations = [
            MapLocation("village", "Village de Brume", 0, 0, "village",
                       "Village paisible terrorisé par les gobelins"),
            MapLocation("forest_entrance", "Entrée de la Forêt", 0, 1, "forest",
                       "Lisière de la forêt sombre"),
            MapLocation("forest_path", "Sentier Forestier", 0, 2, "forest",
                       "Sentier sinueux entre les arbres"),
            MapLocation("goblin_camp", "Camp Gobelin", 0, 3, "camp",
                       "Camp fortifié des gobelins"),
        ]

        # Connexions
        locations[0].connections = ["forest_entrance"]
        locations[1].connections = ["village", "forest_path"]
        locations[2].connections = ["forest_entrance", "goblin_camp"]
        locations[3].connections = ["forest_path"]

        for loc in locations:
            self.locations[loc.id] = loc

        # Village découvert au départ
        self.discover_location("village")
        self.current_location = "village"

    def _build_sunless_citadel_map(self):
        """Carte: The Sunless Citadel"""
        locations = [
            MapLocation("entrance", "Entrée Citadelle", 0, 0, "dungeon",
                       "Entrée béante de la citadelle engloutie"),
            MapLocation("main_hall", "Grand Hall", 0, 1, "chamber",
                       "Hall principal avec fresques anciennes"),
            MapLocation("side_entrance", "Entrée Latérale", -1, 0, "secret",
                       "Fissure dans la pierre"),
            MapLocation("goblin_quarters", "Quartiers Gobelins", -1, 1, "chamber",
                       "Zone infestée de gobelins"),
            MapLocation("goblin_lair", "Repaire Gobelin", -1, 2, "chamber",
                       "Repaire du chef gobelin"),
            MapLocation("gardens", "Jardins Souterrains", 1, 1, "chamber",
                       "Jardins phosphorescents inquiétants"),
            MapLocation("tree_chamber", "Chambre de l'Arbre", 1, 2, "boss",
                       "Salle contenant le Gulthias Tree"),
        ]

        # Connexions
        locations[0].connections = ["main_hall", "side_entrance"]
        locations[1].connections = ["entrance", "goblin_quarters", "gardens"]
        locations[2].connections = ["entrance", "goblin_quarters"]
        locations[3].connections = ["main_hall", "side_entrance", "goblin_lair"]
        locations[4].connections = ["goblin_quarters"]
        locations[5].connections = ["main_hall", "tree_chamber"]
        locations[6].connections = ["gardens"]

        for loc in locations:
            self.locations[loc.id] = loc

        self.discover_location("entrance")
        self.current_location = "entrance"

    def _build_tomb_map(self):
        """Carte: La Tombe des Rois Serpents"""
        locations = [
            MapLocation("entrance", "Entrée Pyramide", 0, 0, "dungeon",
                       "Entrée de la pyramide avec hiéroglyphes"),
            MapLocation("offering_chamber", "Chambre Offrandes", -1, 1, "chamber",
                       "Chambre avec autel et statue serpent"),
            MapLocation("secret_passage", "Passage Secret", -1, 2, "secret",
                       "Passage révélé par l'offrande"),
            MapLocation("guardian_hall", "Salle Gardiens", 1, 1, "chamber",
                       "Salle avec statues de guerriers serpents"),
            MapLocation("throne_approach", "Approche Trône", 0, 2, "chamber",
                       "Antichambre avant la salle du trône"),
            MapLocation("throne_room", "Salle du Trône", 0, 3, "boss",
                       "Salle du Roi Serpent Sesshathep"),
        ]

        # Connexions
        locations[0].connections = ["offering_chamber", "guardian_hall"]
        locations[1].connections = ["entrance", "secret_passage"]
        locations[2].connections = ["offering_chamber", "throne_approach"]
        locations[3].connections = ["entrance", "throne_approach"]
        locations[4].connections = ["guardian_hall", "secret_passage", "throne_room"]
        locations[5].connections = ["throne_approach"]

        for loc in locations:
            self.locations[loc.id] = loc

        self.discover_location("entrance")
        self.current_location = "entrance"

    def discover_location(self, location_id: str):
        """Découvrir un lieu (devient visible)"""
        if location_id in self.locations:
            self.locations[location_id].discovered = True
            self.discovered_locations.add(location_id)

            # Auto-découvrir les lieux connectés
            for conn_id in self.locations[location_id].connections:
                if conn_id in self.locations and not self.locations[conn_id].discovered:
                    self.locations[conn_id].discovered = True
                    self.discovered_locations.add(conn_id)

    def visit_location(self, location_id: str):
        """Visiter un lieu (marqué comme exploré)"""
        if location_id in self.locations:
            self.locations[location_id].visited = True
            self.visited_locations.add(location_id)
            self.current_location = location_id
            self.discover_location(location_id)

    def get_ascii_map(self) -> str:
        """Générer carte ASCII"""
        # Trouver les dimensions
        if not self.locations:
            return "Aucune carte disponible"

        min_x = min(loc.x for loc in self.locations.values())
        max_x = max(loc.x for loc in self.locations.values())
        min_y = min(loc.y for loc in self.locations.values())
        max_y = max(loc.y for loc in self.locations.values())

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        # Créer grille
        grid = [[' ' * 3 for _ in range(width * 4)] for _ in range(height * 2)]

        # Placer les lieux
        for loc in self.locations.values():
            if not loc.discovered:
                continue  # Ne pas montrer les lieux non découverts

            x = (loc.x - min_x) * 4
            y = (loc.y - min_y) * 2

            # Symbole selon type et état
            if loc.id == self.current_location:
                symbol = '[@]'  # Position actuelle
            elif loc.visited:
                symbol = '[✓]'  # Visité
            elif loc.discovered:
                symbol = '[?]'  # Découvert mais pas visité
            else:
                symbol = '[ ]'  # Inconnu

            grid[y][x] = symbol

            # Nom du lieu en dessous
            name_short = loc.name[:12]
            for i, char in enumerate(name_short):
                if x + i < len(grid[y + 1]):
                    grid[y + 1][x + i] = char

        # Convertir en string
        lines = []
        lines.append("=" * 60)
        lines.append(f"  🗺️  CARTE - {self.scenario_id.upper()}")
        lines.append("=" * 60)
        lines.append("")

        for row in grid:
            lines.append(''.join(row))

        lines.append("")
        lines.append("Légende:")
        lines.append("  [@] = Vous êtes ici")
        lines.append("  [✓] = Exploré")
        lines.append("  [?] = Découvert")
        lines.append("=" * 60)

        return '\n'.join(lines)

    def get_location_info(self, location_id: str = None) -> str:
        """Obtenir info sur un lieu"""
        if location_id is None:
            location_id = self.current_location

        if location_id not in self.locations:
            return "Lieu inconnu"

        loc = self.locations[location_id]

        info = []
        info.append(f"📍 {loc.name}")
        info.append(f"   Type: {loc.type}")
        info.append(f"   {loc.description}")

        if loc.connections:
            info.append(f"   Connexions: {', '.join(loc.connections)}")

        return '\n'.join(info)

    def get_exploration_progress(self) -> Tuple[int, int, float]:
        """
        Retourner progression exploration

        Returns:
            (visités, total, pourcentage)
        """
        total = len(self.locations)
        visited = len(self.visited_locations)
        percentage = (visited / total * 100) if total > 0 else 0

        return visited, total, percentage

