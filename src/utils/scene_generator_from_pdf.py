"""
Générateur de scènes depuis sections PDF
"""
from typing import List, Dict, Optional
from src.scenes.scene_system import (
    NarrativeScene, ChoiceScene, CombatScene, RestScene
)


class SceneGeneratorFromPDF:
    """Génère des scènes depuis sections PDF"""

    def __init__(self, scene_data: List[Dict], monster_factory=None):
        """
        Args:
            scene_data: Sections extraites du PDF
            monster_factory: Factory pour créer monstres
        """
        self.scene_data = scene_data
        self.monster_factory = monster_factory
        self.generated_scenes = []

    def generate_all_scenes(self) -> List:
        """Générer toutes les scènes depuis les données"""
        scenes = []

        for idx, scene_data in enumerate(self.scene_data):
            scene = self.generate_scene(scene_data, idx)
            if scene:
                scenes.append(scene)

        self.generated_scenes = scenes
        return scenes

    def generate_scene(self, data: Dict, index: int) -> Optional[object]:
        """
        Générer une scène depuis données

        Args:
            data: Données de la scène (extraites du PDF)
            index: Index de la scène

        Returns:
            Scene object ou None
        """
        scene_type = data.get('type', 'narrative')
        scene_id = data.get('id', f'scene_{index}')
        title = data.get('title', f'Scene {index + 1}')
        description = data.get('description', '')

        # Déterminer scène suivante
        next_scene = self._determine_next_scene(index)

        if scene_type == 'combat':
            return self._create_combat_scene(scene_id, title, description, next_scene)

        elif scene_type == 'choice':
            return self._create_choice_scene(scene_id, title, description, data.get('choices', []))

        elif scene_type == 'rest':
            return self._create_rest_scene(scene_id, title, next_scene)

        else:  # narrative
            return self._create_narrative_scene(scene_id, title, description, next_scene)

    def _create_narrative_scene(self, scene_id: str, title: str, text: str, next_scene: str):
        """Créer scène narrative"""
        return NarrativeScene(
            scene_id=scene_id,
            title=title,
            text=text,
            next_scene_id=next_scene
        )

    def _create_choice_scene(self, scene_id: str, title: str, description: str, choices_data: List[Dict]):
        """Créer scène de choix"""
        # Convertir choix du PDF en format attendu
        choices = []
        for choice_data in choices_data:
            choice = {
                'text': choice_data.get('text', 'Continuer'),
                'next_scene': choice_data.get('next_scene'),
                'effects': choice_data.get('effects', {})
            }
            choices.append(choice)

        # Si pas de choix définis, créer un choix par défaut
        if not choices:
            choices = [{'text': 'Continuer', 'next_scene': None}]

        return ChoiceScene(
            scene_id=scene_id,
            title=title,
            description=description,
            choices=choices
        )

    def _create_combat_scene(self, scene_id: str, title: str, description: str, next_scene: str):
        """Créer scène de combat"""
        # Factory par défaut: créer un gobelin
        def default_enemies(ctx):
            if self.monster_factory:
                return self.monster_factory.create_monsters(['goblin'])
            return []

        return CombatScene(
            scene_id=scene_id,
            title=title,
            description=description,
            enemies_factory=default_enemies,
            on_victory_scene=next_scene,
            on_defeat_scene='game_over'
        )

    def _create_rest_scene(self, scene_id: str, title: str, next_scene: str):
        """Créer scène de repos"""
        return RestScene(
            scene_id=scene_id,
            title=title,
            rest_type='short',
            next_scene_id=next_scene
        )

    def _determine_next_scene(self, current_index: int) -> Optional[str]:
        """Déterminer l'ID de la scène suivante"""
        if current_index + 1 < len(self.scene_data):
            return self.scene_data[current_index + 1].get('id', f'scene_{current_index + 1}')
        return None

    def connect_scenes(self, scene_graph: Dict[str, str]):
        """
        Connecter les scènes selon un graphe

        Args:
            scene_graph: Dict {scene_id: next_scene_id}
        """
        for scene in self.generated_scenes:
            if hasattr(scene, 'next_scene_id') and scene.scene_id in scene_graph:
                scene.next_scene_id = scene_graph[scene.scene_id]

    def export_to_json(self) -> List[Dict]:
        """Exporter les scènes générées en JSON"""
        exported = []

        for scene in self.generated_scenes:
            scene_dict = {
                'id': scene.scene_id,
                'title': scene.title,
                'type': scene.__class__.__name__.replace('Scene', '').lower()
            }

            if hasattr(scene, 'text'):
                scene_dict['text'] = scene.text

            if hasattr(scene, 'description'):
                scene_dict['description'] = scene.description

            if hasattr(scene, 'next_scene_id'):
                scene_dict['next_scene'] = scene.next_scene_id

            if hasattr(scene, 'choices'):
                scene_dict['choices'] = scene.choices

            exported.append(scene_dict)

        return exported


class PDFScenarioBuilder:
    """Construit un scénario complet depuis analyse PDF"""

    def __init__(self, pdf_analysis: Dict, monster_factory=None):
        """
        Args:
            pdf_analysis: Résultat de AdvancedPDFParser.generate_full_analysis()
            monster_factory: Factory pour créer monstres
        """
        self.analysis = pdf_analysis
        self.monster_factory = monster_factory
        self.scene_generator = SceneGeneratorFromPDF(
            pdf_analysis.get('scenes', []),
            monster_factory
        )

    def build_scenario_structure(self) -> Dict:
        """
        Construire la structure complète du scénario

        Returns:
            Dict avec toutes les informations du scénario
        """
        return {
            'name': self._extract_scenario_name(),
            'scenes': self.scene_generator.export_to_json(),
            'monsters': self.analysis.get('monsters', []),
            'encounters': self.analysis.get('random_encounters', []),
            'treasures': self.analysis.get('treasures', []),
            'total_pages': self.analysis.get('total_pages', 0),
            'source': self.analysis.get('source_file', '')
        }

    def _extract_scenario_name(self) -> str:
        """Extraire le nom du scénario"""
        source = self.analysis.get('source_file', '')
        if source:
            from pathlib import Path
            return Path(source).stem
        return "Generated Scenario"

    def generate_scenes(self) -> List:
        """Générer les objets Scene"""
        return self.scene_generator.generate_all_scenes()

    def get_summary(self) -> str:
        """Obtenir un résumé du scénario généré"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"  📖 SCÉNARIO GÉNÉRÉ DEPUIS PDF")
        lines.append("=" * 60)
        lines.append(f"Nom: {self._extract_scenario_name()}")
        lines.append(f"Pages: {self.analysis.get('total_pages', 0)}")
        lines.append(f"Scènes: {len(self.analysis.get('scenes', []))}")
        lines.append(f"Monstres: {len(self.analysis.get('monsters', []))}")
        lines.append(f"Rencontres aléatoires: {len(self.analysis.get('random_encounters', []))}")
        lines.append(f"Tables de trésor: {len(self.analysis.get('treasures', []))}")
        lines.append("=" * 60)

        # Détail des monstres
        if self.analysis.get('monsters'):
            lines.append("\n🐉 MONSTRES TROUVÉS:")
            for monster in self.analysis['monsters'][:5]:  # Top 5
                lines.append(f"  - {monster['name']} (CR {monster['cr']}, HP {monster['hp']}, AC {monster['ac']})")

        # Détail des rencontres
        if self.analysis.get('random_encounters'):
            lines.append("\n⚔️ RENCONTRES ALÉATOIRES:")
            for enc in self.analysis['random_encounters'][:3]:  # Top 3
                lines.append(f"  - [{enc['roll']}] {enc['description']}")

        return '\n'.join(lines)

