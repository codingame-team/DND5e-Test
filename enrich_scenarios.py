#!/usr/bin/env python3
"""
Script d'enrichissement automatique de scénarios
Extrait le contenu des PDFs et génère des scénarios enrichis
"""

from pathlib import Path
from src.utils.pdf_reader import PDFScenarioReader
import json
from typing import Dict, List

class ScenarioEnricher:
    """Enrichir automatiquement un scénario depuis son PDF"""

    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.scenario_name = pdf_path.stem
        self.reader = None

    def extract_pdf_content(self) -> Dict:
        """Extraire tout le contenu du PDF"""
        print(f"📖 Extraction de {self.scenario_name}...")

        with PDFScenarioReader(self.pdf_path) as reader:
            full_text = reader.get_full_text()
            sections = reader.extract_sections()
            npcs = reader.extract_npcs()
            locations = reader.extract_locations()
            encounters = reader.extract_encounters()

            return {
                'full_text': full_text,
                'sections': sections,
                'npcs': npcs,
                'locations': locations,
                'encounters': encounters,
                'text_length': len(full_text)
            }

    def analyze_content(self, content: Dict) -> Dict:
        """Analyser le contenu pour identifier les éléments clés"""
        sections = content['sections']

        # Identifier l'introduction
        intro_section = None
        for key in ['introduction', 'intro', 'contexte', 'présentation']:
            if key in sections:
                intro_section = sections[key]
                break

        if not intro_section and sections:
            # Prendre la première section
            intro_section = list(sections.values())[0]

        return {
            'intro_text': intro_section[:500] if intro_section else "Scénario D&D 5e",
            'num_sections': len(sections),
            'num_npcs': len(content['npcs']),
            'num_locations': len(content['locations']),
            'num_encounters': len(content['encounters'])
        }

    def generate_basic_scenes(self, content: Dict, analysis: Dict) -> List[Dict]:
        """Générer des scènes basiques depuis le contenu extrait"""
        scenes = []

        # Scène 1: Introduction
        intro_text = analysis['intro_text']
        if len(intro_text) > 400:
            intro_text = intro_text[:400] + "..."

        scenes.append({
            "id": "intro",
            "type": "narrative",
            "title": f"📖 {self.scenario_name.upper().replace('-', ' ')}",
            "text": intro_text,
            "next_scene": "main_choice"
        })

        # Scène 2: Choix principal
        choices = []

        # Ajouter des choix basés sur les lieux
        for i, loc in enumerate(content['locations'][:3]):
            choices.append({
                "text": f"Explorer {loc}",
                "next_scene": f"location_{i+1}",
                "effects": {}
            })

        if not choices:
            choices.append({
                "text": "Commencer l'aventure",
                "next_scene": "adventure_start",
                "effects": {}
            })

        scenes.append({
            "id": "main_choice",
            "type": "choice",
            "title": "🗺️ CHOIX",
            "description": "Que faites-vous?",
            "choices": choices
        })

        # Scènes de lieux
        for i, loc in enumerate(content['locations'][:3], 1):
            scenes.append({
                "id": f"location_{i}",
                "type": "narrative",
                "title": f"🏛️ {loc.upper()}",
                "text": f"Vous arrivez à {loc}.\n\nVous explorez les lieux...",
                "next_scene": "encounter_1" if i == 1 else "main_choice"
            })

        # Scène de démarrage si pas de lieux
        scenes.append({
            "id": "adventure_start",
            "type": "narrative",
            "title": "⚔️ L'AVENTURE COMMENCE",
            "text": "Votre aventure commence...",
            "next_scene": "encounter_1"
        })

        # Rencontres basées sur les encounters extraits
        if content['encounters']:
            encounter = content['encounters'][0]
            scenes.append({
                "id": "encounter_1",
                "type": "combat",
                "title": f"⚔️ RENCONTRE: {encounter['creature'].upper()}",
                "description": f"Vous affrontez {encounter['count']} {encounter['creature']}!",
                "monsters": ["goblin"] * min(encounter['count'], 4),
                "on_victory": "victory",
                "on_defeat": "game_over"
            })
        else:
            scenes.append({
                "id": "encounter_1",
                "type": "combat",
                "title": "⚔️ COMBAT",
                "description": "Des ennemis vous attaquent!",
                "monsters": ["goblin", "goblin"],
                "on_victory": "victory",
                "on_defeat": "game_over"
            })

        # Victoire
        scenes.append({
            "id": "victory",
            "type": "narrative",
            "title": "🎉 VICTOIRE!",
            "text": f"Vous avez accompli votre mission dans {self.scenario_name.replace('-', ' ')}!\n\nVous êtes récompensés pour vos exploits.",
            "next_scene": None,
            "rewards": {
                "gold": 200,
                "xp": 500,
                "items": []
            }
        })

        # Défaite
        scenes.append({
            "id": "game_over",
            "type": "narrative",
            "title": "💀 DÉFAITE",
            "text": "Vous avez été vaincus...",
            "next_scene": None
        })

        return scenes

    def create_enriched_scenario(self) -> Dict:
        """Créer un scénario enrichi complet"""
        print(f"\n{'='*70}")
        print(f"📖 ENRICHISSEMENT: {self.scenario_name}")
        print(f"{'='*70}")

        # Extraire le contenu
        content = self.extract_pdf_content()
        print(f"✅ Texte extrait: {content['text_length']} caractères")
        print(f"✅ Sections: {len(content['sections'])}")
        print(f"✅ NPCs: {len(content['npcs'])}")
        print(f"✅ Lieux: {len(content['locations'])}")
        print(f"✅ Rencontres: {len(content['encounters'])}")

        # Analyser
        analysis = self.analyze_content(content)

        # Générer les scènes
        scenes = self.generate_basic_scenes(content, analysis)
        print(f"✅ Scènes générées: {len(scenes)}")

        # Créer le JSON du scénario
        scenario = {
            "scenario_id": self.scenario_name.lower().replace('-', '_'),
            "name": self.scenario_name.replace('-', ' ').title(),
            "level": 2,
            "difficulty": "medium",
            "duration_hours": "2-3",
            "recommended_party_size": 4,
            "description": f"Scénario enrichi automatiquement depuis le PDF. {analysis['num_sections']} sections, {analysis['num_locations']} lieux.",
            "scenes": scenes
        }

        return scenario

    def save_enriched_scenario(self, output_dir: Path):
        """Sauvegarder le scénario enrichi"""
        scenario = self.create_enriched_scenario()

        output_file = output_dir / f"{self.scenario_name.lower().replace('-', '_')}_enrichi.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scenario, f, indent=2, ensure_ascii=False)

        print(f"✅ Scénario sauvegardé: {output_file}")
        return output_file


def main():
    """Enrichir plusieurs scénarios"""
    scenarios_dir = Path("scenarios")
    output_dir = Path("data/scenes")

    # Liste des PDFs à enrichir (25 scénarios)
    priority_pdfs = [
        # Déjà enrichis manuellement
        # "Masque-utruz.pdf",

        # Batch 1 (5)
        "Cryptes-de-Kelemvor.pdf",
        "Defis-a-Phlan.pdf",
        "Fort-Roanoke.pdf",
        "Harceles-a-Monteloy.pdf",
        "Chasse-sanglante.pdf",

        # Batch 2 (5)
        "Armee-verte.pdf",
        "Basse-tour.pdf",
        "Douze-fontaines.pdf",
        "Duel-au-pinceau.pdf",
        "Fuir-Elturgard.pdf",

        # Batch 3 (5)
        "Malediction-Autretant.pdf",
        "Mariage-empereur-demon.pdf",
        "Menaces-sur-Port-Nyanzaru.pdf",
        "Message.pdf",
        "Naufrages.pdf",

        # Batch 4 (5)
        "Nom-de-la-foi.pdf",
        "Nuit-empereur-demon.pdf",
        "Pour-un-diamant.pdf",
        "Quelque-chose-de-perdu.pdf",
        "Quitte-ou-double.pdf",

        # Batch 5 (5)
        "Rachat.pdf",
        "Retour-empereur-demon.pdf",
        "Ruffians-d-Olizya.pdf",
        "Sceptre-de-Baine.pdf",
        "Oeil-de-Gruumsh.pdf"
    ]

    print("🚀 ENRICHISSEMENT AUTOMATIQUE DE SCÉNARIOS")
    print("="*70)

    enriched_count = 0

    for pdf_name in priority_pdfs:
        pdf_path = scenarios_dir / pdf_name

        if not pdf_path.exists():
            print(f"⚠️  PDF non trouvé: {pdf_name}")
            continue

        try:
            enricher = ScenarioEnricher(pdf_path)
            enricher.save_enriched_scenario(output_dir)
            enriched_count += 1
            print()
        except Exception as e:
            print(f"❌ Erreur pour {pdf_name}: {e}")
            import traceback
            traceback.print_exc()
            print()

    print("="*70)
    print(f"✅ {enriched_count}/{len(priority_pdfs)} scénarios enrichis avec succès!")


if __name__ == "__main__":
    main()

