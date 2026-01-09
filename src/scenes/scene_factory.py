"""
Scene Factory - Construit des scènes à partir de données JSON
"""

from typing import Dict, List, Optional, Callable
from .scene_system import (
    BaseScene, NarrativeScene, ChoiceScene, CombatScene,
    MerchantScene, RestScene, SceneManager
)


class SceneFactory:
    """
    Factory pour créer des scènes depuis JSON
    """

    @staticmethod
    def create_scene_from_dict(scene_data: Dict, monster_factory=None) -> Optional[BaseScene]:
        """
        Créer une scène à partir d'un dictionnaire

        Args:
            scene_data: Données de la scène
            monster_factory: Factory pour créer les monstres

        Returns:
            Une instance de BaseScene ou None
        """
        scene_type = scene_data.get('type')
        scene_id = scene_data.get('id')
        title = scene_data.get('title', '')

        if scene_type == 'narrative':
            return NarrativeScene(
                scene_id=scene_id,
                title=title,
                text=scene_data.get('text', ''),
                next_scene_id=scene_data.get('next_scene'),
                delay=scene_data.get('delay', 0.02)
            )

        elif scene_type == 'choice':
            choices = []
            for choice_data in scene_data.get('choices', []):
                choices.append({
                    'text': choice_data.get('text'),
                    'next_scene': choice_data.get('next_scene'),
                    'effects': choice_data.get('effects', {})
                })

            return ChoiceScene(
                scene_id=scene_id,
                title=title,
                description=scene_data.get('description', ''),
                choices=choices
            )

        elif scene_type == 'combat':
            # Créer une factory pour les monstres
            monster_names = scene_data.get('monsters', [])

            def enemies_factory(game_context):
                monsters = []
                factory = game_context.get('monster_factory') or monster_factory
                if factory:
                    for monster_name in monster_names:
                        monster = factory.create_monster(monster_name)
                        if monster:
                            monsters.append(monster)
                return monsters

            return CombatScene(
                scene_id=scene_id,
                title=title,
                description=scene_data.get('description', ''),
                enemies_factory=enemies_factory,
                on_victory_scene=scene_data.get('on_victory'),
                on_defeat_scene=scene_data.get('on_defeat')
            )

        elif scene_type == 'merchant':
            return MerchantScene(
                scene_id=scene_id,
                title=title,
                merchant_id=scene_data.get('merchant_id', 'default'),
                next_scene_id=scene_data.get('next_scene')
            )

        elif scene_type == 'rest':
            return RestScene(
                scene_id=scene_id,
                title=title,
                rest_type=scene_data.get('rest_type', 'long'),
                next_scene_id=scene_data.get('next_scene')
            )

        else:
            print(f"⚠️ Type de scène inconnu: {scene_type}")
            return None

    @staticmethod
    def build_scene_manager_from_json(scenario_data: Dict, monster_factory=None) -> SceneManager:
        """
        Construire un SceneManager complet depuis les données JSON

        Args:
            scenario_data: Données complètes du scénario
            monster_factory: Factory pour créer les monstres

        Returns:
            Un SceneManager configuré avec toutes les scènes
        """
        manager = SceneManager()

        scenes_data = scenario_data.get('scenes', [])

        # Créer toutes les scènes
        for scene_data in scenes_data:
            scene = SceneFactory.create_scene_from_dict(scene_data, monster_factory)
            if scene:
                manager.add_scene(scene)

        # Définir la scène de départ (première scène par défaut)
        if scenes_data:
            start_scene_id = scenes_data[0].get('id')
            manager.set_start_scene(start_scene_id)

        return manager

    @staticmethod
    def load_scenario_from_json_file(json_file_path: str, monster_factory=None) -> Optional[SceneManager]:
        """
        Charger un scénario complet depuis un fichier JSON

        Args:
            json_file_path: Chemin vers le fichier JSON
            monster_factory: Factory pour créer les monstres

        Returns:
            Un SceneManager ou None en cas d'erreur
        """
        import json
        from pathlib import Path

        try:
            path = Path(json_file_path)
            if not path.exists():
                print(f"❌ Fichier non trouvé: {json_file_path}")
                return None

            with open(path, 'r', encoding='utf-8') as f:
                scenario_data = json.load(f)

            return SceneFactory.build_scene_manager_from_json(scenario_data, monster_factory)

        except Exception as e:
            print(f"❌ Erreur lors du chargement du scénario: {e}")
            import traceback
            traceback.print_exc()
            return None

