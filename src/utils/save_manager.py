"""
Système de sauvegarde et chargement de partie
"""
import json
import pickle
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class SaveGameManager:
    """Gestionnaire de sauvegardes de parties"""

    def __init__(self, save_dir: str = "savegames"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.current_save_dir.mkdir(exist_ok=True)

    @property
    def current_save_dir(self) -> Path:
        """Répertoire des sauvegardes actives"""
        return self.save_dir / "current"

    def save_game(self, scenario_name: str, party: List, game_state: Dict,
                  scene_id: str, slot_name: str = "autosave") -> bool:
        """
        Sauvegarder une partie

        Args:
            scenario_name: Nom du scénario
            party: Liste des personnages
            game_state: État du jeu
            scene_id: ID de la scène actuelle
            slot_name: Nom du slot de sauvegarde

        Returns:
            True si succès
        """
        try:
            save_data = {
                'scenario': scenario_name,
                'scene_id': scene_id,
                'game_state': game_state,
                'timestamp': datetime.now().isoformat(),
                'version': '3.1.0'
            }

            # Sauvegarder metadata JSON
            save_file = self.current_save_dir / f"{slot_name}.json"
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            # Sauvegarder party en pickle (objets complexes)
            party_file = self.current_save_dir / f"{slot_name}_party.pkl"
            with open(party_file, 'wb') as f:
                pickle.dump(party, f)

            print(f"✅ Partie sauvegardée: {slot_name}")
            return True

        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False

    def load_game(self, slot_name: str = "autosave") -> Optional[Dict]:
        """
        Charger une partie

        Returns:
            Dict avec 'party', 'game_state', 'scene_id', 'scenario' ou None
        """
        try:
            save_file = self.current_save_dir / f"{slot_name}.json"
            party_file = self.current_save_dir / f"{slot_name}_party.pkl"

            if not save_file.exists() or not party_file.exists():
                return None

            # Charger metadata
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Charger party
            with open(party_file, 'rb') as f:
                party = pickle.load(f)

            save_data['party'] = party

            print(f"✅ Partie chargée: {slot_name}")
            print(f"   Scénario: {save_data['scenario']}")
            print(f"   Date: {save_data['timestamp']}")

            return save_data

        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            return None

    def list_saves(self) -> List[Dict]:
        """Lister toutes les sauvegardes disponibles"""
        saves = []

        for save_file in self.current_save_dir.glob("*.json"):
            if not save_file.stem.endswith("_party"):
                try:
                    with open(save_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data['slot_name'] = save_file.stem
                        saves.append(data)
                except:
                    pass

        return sorted(saves, key=lambda x: x.get('timestamp', ''), reverse=True)

    def delete_save(self, slot_name: str) -> bool:
        """Supprimer une sauvegarde"""
        try:
            save_file = self.current_save_dir / f"{slot_name}.json"
            party_file = self.current_save_dir / f"{slot_name}_party.pkl"

            if save_file.exists():
                save_file.unlink()
            if party_file.exists():
                party_file.unlink()

            print(f"✅ Sauvegarde supprimée: {slot_name}")
            return True

        except Exception as e:
            print(f"❌ Erreur suppression: {e}")
            return False

    def autosave(self, scenario_name: str, party: List, game_state: Dict, scene_id: str):
        """Sauvegarde automatique"""
        return self.save_game(scenario_name, party, game_state, scene_id, "autosave")


class JSONLoader:
    """Chargeur de données JSON"""

    @staticmethod
    def load_scenes(scenario_id: str) -> Optional[Dict]:
        """Charger les scènes d'un scénario"""
        try:
            file_path = Path(f"data/scenes/{scenario_id}.json")
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"⚠️ Erreur chargement scènes: {e}")
            return None

    @staticmethod
    def load_monsters() -> Dict:
        """Charger tous les monstres"""
        try:
            file_path = Path("data/monsters/all_monsters.json")
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('monsters', {})
            return {}
        except Exception as e:
            print(f"⚠️ Erreur chargement monstres: {e}")
            return {}

    @staticmethod
    def load_parties() -> Dict:
        """Charger les configurations de groupes"""
        try:
            file_path = Path("data/parties/scenario_parties.json")
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('parties', {})
            return {}
        except Exception as e:
            print(f"⚠️ Erreur chargement parties: {e}")
            return {}

