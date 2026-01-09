"""
Parser PDF avancé pour extraire tables de monstres et rencontres
"""
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import fitz  # PyMuPDF


class AdvancedPDFParser:
    """Parser avancé pour PDFs de scénarios D&D"""

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.doc = None
        self.text_pages = []

    def __enter__(self):
        self.doc = fitz.open(self.pdf_path)
        self._extract_all_text()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.doc:
            self.doc.close()

    def _extract_all_text(self):
        """Extraire tout le texte du PDF"""
        self.text_pages = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            self.text_pages.append({
                'page_num': page_num + 1,
                'text': text
            })

    def extract_monster_tables(self) -> List[Dict]:
        """
        Extraire les tables de monstres

        Format typique:
        MONSTER NAME
        CR X | HP XX | AC XX
        """
        monsters = []

        # Patterns pour identifier les monstres
        monster_patterns = [
            # Pattern 1: "Goblin" suivi de stats sur ligne suivante
            r'(?P<name>[A-Z][a-zA-Z\s]+)\n.*?CR\s*(?P<cr>[\d/]+).*?HP\s*(?P<hp>\d+).*?AC\s*(?P<ac>\d+)',
            # Pattern 2: Stats inline
            r'(?P<name>[A-Z][a-zA-Z\s]+).*?CR\s*(?P<cr>[\d/]+).*?HP\s*(?P<hp>\d+).*?AC\s*(?P<ac>\d+)',
            # Pattern 3: Format tabulaire
            r'(?P<name>[A-Z][a-zA-Z\s]+)\s+\|\s+CR\s*(?P<cr>[\d/]+)\s+\|\s+HP\s*(?P<hp>\d+)\s+\|\s+AC\s*(?P<ac>\d+)',
        ]

        for page_data in self.text_pages:
            text = page_data['text']

            for pattern in monster_patterns:
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    monster = {
                        'name': match.group('name').strip(),
                        'cr': match.group('cr'),
                        'hp': int(match.group('hp')),
                        'ac': int(match.group('ac')),
                        'page': page_data['page_num'],
                        'source': 'pdf_table'
                    }
                    monsters.append(monster)

        return self._deduplicate_monsters(monsters)

    def extract_random_encounters(self) -> List[Dict]:
        """
        Extraire les tables de rencontres aléatoires

        Format typique:
        RANDOM ENCOUNTERS
        1d6 | Encounter
        1-2 | 2d4 Goblins
        3-4 | 1d6 Wolves
        """
        encounters = []

        for page_data in self.text_pages:
            text = page_data['text']

            # Chercher sections de rencontres
            encounter_sections = re.finditer(
                r'(RANDOM\s+ENCOUNTERS?|WANDERING\s+MONSTERS?)(.*?)(?=\n\n[A-Z]|\Z)',
                text,
                re.DOTALL | re.IGNORECASE
            )

            for section in encounter_sections:
                section_text = section.group(2)

                # Parser les lignes de table
                # Format: "1-2 | 2d4 Goblins"
                encounter_lines = re.finditer(
                    r'(?P<roll>[\d\-d]+)\s*[|\:]\s*(?P<description>.*?)(?=\n|$)',
                    section_text,
                    re.MULTILINE
                )

                for line in encounter_lines:
                    roll = line.group('roll').strip()
                    description = line.group('description').strip()

                    if description and len(description) > 3:
                        encounter = {
                            'roll': roll,
                            'description': description,
                            'page': page_data['page_num'],
                            'type': 'random_encounter'
                        }

                        # Extraire nombre et type de monstre
                        parsed = self._parse_encounter_description(description)
                        encounter.update(parsed)

                        encounters.append(encounter)

        return encounters

    def _parse_encounter_description(self, description: str) -> Dict:
        """
        Parser description de rencontre
        Ex: "2d4 Goblins" -> {count: "2d4", monster: "Goblins"}
        """
        # Pattern: "XdY Monster" ou "X Monster"
        match = re.match(r'(\d+d\d+|\d+)\s+(.+)', description)

        if match:
            return {
                'count': match.group(1),
                'monster_type': match.group(2).strip()
            }

        return {
            'count': '1',
            'monster_type': description
        }

    def extract_sections_as_scenes(self) -> List[Dict]:
        """
        Extraire les sections du PDF et les convertir en scènes

        Identifie:
        - Titres de sections (CAPS ou numérotés)
        - Descriptions
        - Choix possibles
        """
        scenes = []

        for page_data in self.text_pages:
            text = page_data['text']

            # Chercher sections avec titres
            # Pattern: Ligne en CAPS suivie de texte
            sections = re.finditer(
                r'^([A-Z][A-Z\s]{3,})\n(.*?)(?=\n[A-Z][A-Z\s]{3,}|\Z)',
                text,
                re.MULTILINE | re.DOTALL
            )

            for section in sections:
                title = section.group(1).strip()
                content = section.group(2).strip()

                # Ignorer si trop court
                if len(content) < 50:
                    continue

                # Identifier le type de scène
                scene_type = self._identify_scene_type(title, content)

                # Extraire choix si présent
                choices = self._extract_choices(content)

                scene = {
                    'id': self._generate_scene_id(title),
                    'title': title,
                    'type': scene_type,
                    'description': self._clean_text(content),
                    'page': page_data['page_num'],
                    'choices': choices
                }

                scenes.append(scene)

        return scenes

    def _identify_scene_type(self, title: str, content: str) -> str:
        """Identifier le type de scène"""
        title_lower = title.lower()
        content_lower = content.lower()

        # Combat
        if any(word in title_lower for word in ['combat', 'battle', 'encounter', 'fight']):
            return 'combat'

        if any(word in content_lower for word in ['attack', 'initiative', 'hp', 'damage']):
            return 'combat'

        # Choix
        if 'if' in content_lower and 'then' in content_lower:
            return 'choice'

        if len(self._extract_choices(content)) > 0:
            return 'choice'

        # Repos
        if any(word in title_lower for word in ['rest', 'camp', 'sleep']):
            return 'rest'

        # Par défaut: narrative
        return 'narrative'

    def _extract_choices(self, text: str) -> List[Dict]:
        """Extraire les choix possibles du texte"""
        choices = []

        # Pattern: lignes commençant par - ou •
        bullet_points = re.finditer(r'^[\-\•]\s*(.+?)(?=\n|$)', text, re.MULTILINE)

        for bullet in bullet_points:
            choice_text = bullet.group(1).strip()
            if len(choice_text) > 5:
                choices.append({
                    'text': choice_text,
                    'next_scene': None  # À définir manuellement
                })

        # Pattern: "If ... then ..."
        if_then = re.finditer(
            r'If\s+(.+?)\s+then\s+(.+?)(?=\.|If|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        for condition in if_then:
            choices.append({
                'text': condition.group(1).strip(),
                'consequence': condition.group(2).strip(),
                'next_scene': None
            })

        return choices

    def _generate_scene_id(self, title: str) -> str:
        """Générer un ID de scène depuis le titre"""
        # Convertir en snake_case
        scene_id = title.lower()
        scene_id = re.sub(r'[^\w\s]', '', scene_id)
        scene_id = re.sub(r'\s+', '_', scene_id)
        return scene_id

    def _clean_text(self, text: str) -> str:
        """Nettoyer le texte extrait"""
        # Supprimer numéros de page
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)

        # Normaliser espaces
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        return text.strip()

    def _deduplicate_monsters(self, monsters: List[Dict]) -> List[Dict]:
        """Supprimer les monstres en double"""
        seen = set()
        unique = []

        for monster in monsters:
            key = (monster['name'], monster['cr'], monster['hp'])
            if key not in seen:
                seen.add(key)
                unique.append(monster)

        return unique

    def extract_treasure_tables(self) -> List[Dict]:
        """Extraire les tables de trésors"""
        treasures = []

        for page_data in self.text_pages:
            text = page_data['text']

            # Chercher sections de trésor
            treasure_sections = re.finditer(
                r'(TREASURE|LOOT|REWARDS?)(.*?)(?=\n\n[A-Z]|\Z)',
                text,
                re.DOTALL | re.IGNORECASE
            )

            for section in treasure_sections:
                section_text = section.group(2)

                # Extraire valeurs en or
                gold = re.findall(r'(\d+)\s*(?:gp|gold|po)', section_text, re.IGNORECASE)

                # Extraire items
                items = re.findall(r'[-•]\s*(.+?)(?=\n|$)', section_text, re.MULTILINE)

                if gold or items:
                    treasures.append({
                        'page': page_data['page_num'],
                        'gold': sum(int(g) for g in gold),
                        'items': [item.strip() for item in items if item.strip()],
                        'raw_text': section_text[:200]
                    })

        return treasures

    def generate_full_analysis(self) -> Dict:
        """Générer une analyse complète du PDF"""
        return {
            'monsters': self.extract_monster_tables(),
            'random_encounters': self.extract_random_encounters(),
            'scenes': self.extract_sections_as_scenes(),
            'treasures': self.extract_treasure_tables(),
            'total_pages': len(self.text_pages),
            'source_file': str(self.pdf_path)
        }

