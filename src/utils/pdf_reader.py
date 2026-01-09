"""
PDF Reader for D&D Scenarios
Extracts text, images, and maps from scenario PDFs
"""

import fitz  # PyMuPDF
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import re


class PDFScenarioReader:
    """
    Lecteur de scénarios PDF D&D
    Extrait texte, structure, et images/maps
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.doc = None
        self.pages_text = []
        self.structure = {}

        if self.pdf_path.exists():
            self.doc = fitz.open(str(self.pdf_path))
            self._extract_all()

    def _extract_all(self):
        """Extraire tout le contenu du PDF"""
        if not self.doc:
            return

        # Extraire texte de chaque page
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            self.pages_text.append({
                'page': page_num + 1,
                'text': text,
                'blocks': self._extract_text_blocks(page)
            })

    def _extract_text_blocks(self, page) -> List[Dict]:
        """Extraire blocs de texte structurés"""
        blocks = []
        text_blocks = page.get_text("dict")["blocks"]

        for block in text_blocks:
            if block.get("type") == 0:  # Text block
                block_text = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        block_text += span.get("text", "") + " "

                blocks.append({
                    'text': block_text.strip(),
                    'bbox': block.get("bbox"),
                    'font_size': block.get("lines", [{}])[0].get("spans", [{}])[0].get("size", 12)
                })

        return blocks

    def extract_sections(self) -> Dict[str, str]:
        """
        Extraire les sections du scénario
        Détecte les titres et organise le contenu
        """
        sections = {}
        current_section = "introduction"
        current_text = []

        for page_data in self.pages_text:
            for block in page_data['blocks']:
                text = block['text']
                font_size = block.get('font_size', 12)

                # Détecter titre (font plus grande)
                if font_size > 14 and len(text) < 100:
                    # Sauver section précédente
                    if current_text:
                        sections[current_section] = "\n".join(current_text)

                    # Nouvelle section
                    current_section = text.strip().lower().replace(" ", "_")
                    current_text = []
                else:
                    current_text.append(text)

        # Dernière section
        if current_text:
            sections[current_section] = "\n".join(current_text)

        return sections

    def extract_npcs(self) -> List[Dict]:
        """
        Extraire les PNJs mentionnés
        Recherche patterns comme "NOM (Race, Classe)"
        """
        npcs = []
        full_text = self.get_full_text()

        # Pattern: Nom en gras ou majuscules suivi de description
        npc_pattern = r'([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ][a-zàâäéèêëïîôùûüÿç]+(?:\s+[A-ZÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ][a-zàâäéèêëïîôùûüÿç]+)*)\s*\(([^)]+)\)'

        matches = re.finditer(npc_pattern, full_text)
        for match in matches:
            name = match.group(1)
            description = match.group(2)

            npcs.append({
                'name': name,
                'description': description,
                'context': full_text[max(0, match.start()-100):min(len(full_text), match.end()+100)]
            })

        return npcs

    def extract_locations(self) -> List[str]:
        """
        Extraire les lieux mentionnés
        Recherche patterns de lieux
        """
        locations = []
        full_text = self.get_full_text()

        # Patterns communs pour lieux
        location_keywords = [
            r'(?:le|la|l\')\s+([A-Z][a-zàâäéèêëïîôùûüÿç]+(?:\s+(?:de|des|du)\s+[A-Z][a-zàâäéèêëïîôùûüÿç]+)?)',
            r'(?:Village|Ville|Château|Grotte|Forêt|Montagne|Caverne|Donjon|Taverne)\s+(?:de\s+|des\s+|du\s+)?([A-Z][a-zàâäéèêëïîôùûüÿç]+)'
        ]

        for pattern in location_keywords:
            matches = re.finditer(pattern, full_text)
            for match in matches:
                location = match.group(1) if match.lastindex == 1 else match.group(0)
                if location and location not in locations:
                    locations.append(location.strip())

        return locations[:20]  # Limiter à 20 pour éviter trop de résultats

    def extract_encounters(self) -> List[Dict]:
        """
        Extraire les rencontres de combat
        Recherche mentions de créatures et CR
        """
        encounters = []
        full_text = self.get_full_text()

        # Pattern: créature avec potentiel CR/niveau
        creature_pattern = r'(\d+)\s*([gG]obelin|[oO]rc|[dD]ragon|[lL]oup|[zZ]ombie|[sS]quelette|[hH]obgobelin)'

        matches = re.finditer(creature_pattern, full_text, re.IGNORECASE)
        for match in matches:
            count = int(match.group(1))
            creature = match.group(2)

            encounters.append({
                'count': count,
                'creature': creature.capitalize(),
                'context': full_text[max(0, match.start()-50):min(len(full_text), match.end()+50)]
            })

        return encounters

    def extract_images(self, output_dir: str = "data/maps") -> List[str]:
        """
        Extraire toutes les images du PDF
        Sauvegarde dans output_dir et retourne chemins
        """
        if not self.doc:
            return []

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        extracted_images = []

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            image_list = page.get_images()

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Sauvegarder image
                image_filename = f"{self.pdf_path.stem}_page{page_num+1}_img{img_index+1}.{image_ext}"
                image_path = output_path / image_filename

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                extracted_images.append(str(image_path))

        return extracted_images

    def extract_maps_as_ascii(self) -> List[Dict]:
        """
        Tenter de détecter et convertir maps en ASCII
        Analyse les images pour détecter grilles/maps
        """
        maps = []

        # Pour l'instant, créer map ASCII générique basée sur le scénario
        sections = self.extract_sections()
        locations = self.extract_locations()

        # Créer une map simple basée sur les lieux trouvés
        if locations:
            ascii_map = self._generate_simple_ascii_map(locations[:5])
            maps.append({
                'type': 'generated',
                'locations': locations[:5],
                'ascii': ascii_map
            })

        return maps

    def _generate_simple_ascii_map(self, locations: List[str]) -> str:
        """Générer une map ASCII simple avec les lieux"""
        width = 40
        height = 15

        # Créer grille vide
        grid = [['.' for _ in range(width)] for _ in range(height)]

        # Bordures
        for x in range(width):
            grid[0][x] = '#'
            grid[height-1][x] = '#'
        for y in range(height):
            grid[y][0] = '#'
            grid[y][width-1] = '#'

        # Placer lieux (positions fixes valides)
        # Format: (row/y, col/x) dans les limites de la grille
        positions = [
            (3, 5),   # A - en haut à gauche
            (3, 20),  # B - en haut à droite
            (7, 12),  # C - au centre
            (11, 8),  # D - en bas à gauche
            (11, 25)  # E - en bas à droite
        ]

        for i, loc in enumerate(locations[:5]):
            if i < len(positions):
                row, col = positions[i]
                # Vérifier que les positions sont valides
                if 0 <= row < height and 0 <= col < width:
                    letter = chr(65 + i)  # A, B, C, D, E
                    grid[row][col] = letter

        # Convertir en string
        map_str = "\n".join("".join(row) for row in grid)

        # Ajouter légende
        legend = "\n\nLégende:\n"
        for i, loc in enumerate(locations[:5]):
            legend += f"  {chr(65+i)} = {loc}\n"

        return map_str + legend

    def get_full_text(self) -> str:
        """Obtenir tout le texte du PDF"""
        return "\n\n".join(page['text'] for page in self.pages_text)

    def get_page_count(self) -> int:
        """Obtenir nombre de pages"""
        return len(self.doc) if self.doc else 0

    def generate_scenario_summary(self) -> Dict:
        """
        Générer un résumé complet du scénario
        """
        return {
            'title': self.pdf_path.stem,
            'pages': self.get_page_count(),
            'sections': list(self.extract_sections().keys()),
            'npcs': self.extract_npcs(),
            'locations': self.extract_locations(),
            'encounters': self.extract_encounters(),
            'full_text_length': len(self.get_full_text())
        }

    def close(self):
        """Fermer le document PDF"""
        if self.doc:
            self.doc.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def quick_read_scenario(pdf_path: str) -> Dict:
    """
    Lecture rapide d'un scénario
    Retourne résumé structuré
    """
    with PDFScenarioReader(pdf_path) as reader:
        return reader.generate_scenario_summary()

