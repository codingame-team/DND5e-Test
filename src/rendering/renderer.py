"""
Renderers for game output - Adapter Pattern
Permet de changer facilement le mode d'affichage (console, ncurses, etc.)
"""

from abc import ABC, abstractmethod
from typing import List
import time


class Renderer(ABC):
    """Interface abstraite pour renderers"""

    @abstractmethod
    def print_header(self, title: str):
        """Afficher un en-tête"""
        pass

    @abstractmethod
    def print_slow(self, text: str, delay: float = 0.02):
        """Afficher texte avec effet"""
        pass

    @abstractmethod
    def wait_for_input(self, prompt: str = "\n[Appuyez sur ENTRÉE pour continuer]"):
        """Attendre entrée utilisateur"""
        pass

    @abstractmethod
    def get_choice(self, options: List[str]) -> int:
        """Obtenir choix utilisateur"""
        pass

    @abstractmethod
    def display_map(self, map_ascii: str, player_pos: tuple = None):
        """Afficher une map"""
        pass


class ConsoleRenderer(Renderer):
    """
    Renderer console simple
    Compatible avec le jeu actuel
    """

    def print_header(self, title: str):
        """En-tête stylisé"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")

    def print_slow(self, text: str, delay: float = 0.02):
        """Effet machine à écrire"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def wait_for_input(self, prompt: str = "\n[Appuyez sur ENTRÉE pour continuer]"):
        """Pause"""
        input(prompt)

    def get_choice(self, options: List[str]) -> int:
        """Choix utilisateur"""
        print("\nQue voulez-vous faire ?")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")

        while True:
            try:
                choice = int(input("\nVotre choix: "))
                if 1 <= choice <= len(options):
                    return choice - 1
                print(f"Veuillez entrer un nombre entre 1 et {len(options)}")
            except ValueError:
                print("Veuillez entrer un nombre valide")

    def display_map(self, map_ascii: str, player_pos: tuple = None):
        """Afficher map ASCII"""
        print("\n" + "─" * 70)
        print("  🗺️  CARTE")
        print("─" * 70)
        print(map_ascii)
        if player_pos:
            print(f"\n📍 Position: {player_pos}")
        print("─" * 70 + "\n")


def create_renderer(use_ncurses: bool = False) -> Renderer:
    """
    Factory pour créer renderer
    Pour l'instant, retourne toujours ConsoleRenderer
    NCurses peut être ajouté plus tard
    """
    # NCurses désactivé pour l'instant (nécessite configuration spéciale)
    return ConsoleRenderer()

