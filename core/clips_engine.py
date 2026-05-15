"""
Moteur d'inférence CLIBS (CLIPS) pour l'orientation académique
Compatible avec clipspy 1.0.6
"""

import clips
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple


class CLIPSEngine:
    """Moteur d'inférence basé sur CLIPS (NASA)"""
    
    def __init__(self, knowledge_path: str = "knowledge"):
        self.env = clips.Environment()
        self.knowledge_path = Path(knowledge_path)
        self.scores: Dict[str, float] = {}
        self.debug = False
        
        # Charger la base de connaissances
        self.load_knowledge_base()
    
    def set_debug(self, enabled: bool = True):
        """Active ou désactive le mode debug"""
        self.debug = enabled
    
    def load_knowledge_base(self):
        """Charge tous les fichiers CLIPS du dossier knowledge"""
        # Charger les templates
        templates_file = self.knowledge_path / "templates.clp"
        if templates_file.exists():
            print(f"Chargement: {templates_file}")
            self.env.load(str(templates_file))
        
        # Charger les règles
        rules_file = self.knowledge_path / "rules.clp"
        if rules_file.exists():
            print(f"Chargement: {rules_file}")
            self.env.load(str(rules_file))
        
        self.env.reset()
        print("✅ Base de connaissances CLIPS chargée")
    
    def assert_fact(self, fact_string: str):
        """Ajoute un fait dans la base de faits"""
        try:
            self.env.assert_string(fact_string)
            if self.debug:
                print(f"  + {fact_string}")
            return True
        except Exception as e:
            if self.debug:
                print(f"  ❌ Erreur: {e}")
            return False
    
    def assert_grade(self, subject: str, value: float):
        """Ajoute une note dans la base de faits"""
        int_value = int(value)
        fact = f'(grade (subject {subject}) (value {int_value}))'
        return self.assert_fact(fact)
    
    def assert_quality(self, quality: str, level: int = 3):
        """Ajoute une qualité dans la base de faits"""
        fact = f'(quality (name {quality}) (level {level}))'
        return self.assert_fact(fact)
    
    def assert_preference(self, value: str, category: str = "interest"):
        """Ajoute une préférence dans la base de faits"""
        fact = f'(preference (category {category}) (value "{value}"))'
        return self.assert_fact(fact)
    
    def evaluate_student(self, 
                         notes: Dict[str, float],
                         preferences: List[str],
                         qualites: List[str]) -> Dict[str, Any]:
        """
        Évalue un étudiant et retourne les scores
        """
        if self.debug:
            print("\n" + "="*50)
            print("🔍 Évaluation par le moteur CLIPS")
            print("="*50)
        
        # Réinitialiser
        self.env.reset()
        self.scores = {}
        
        # Ajouter les faits
        if self.debug:
            print("\n📥 Ajout des faits:")
        
        for subject, grade in notes.items():
            self.assert_grade(subject.lower(), grade)
        
        for quality in qualites:
            self.assert_quality(quality.lower())
        
        for pref in preferences:
            self.assert_preference(pref.lower())
        
        # Exécuter les règles
        if self.debug:
            print("\n⚙️ Exécution des règles CLIPS...")
        
        self.env.run()
        
        # Récupérer les scores depuis l'environnement CLIPS
        self.extract_scores_from_facts()
        
        # Calculer les pourcentages
        percentages = self.get_percentages(self.scores)
        
        if self.debug:
            print("\n📊 Scores finaux:")
            for domain, score in self.scores.items():
                print(f"  {domain}: {score}")
        
        return {
            "scores": self.scores,
            "percentages": percentages,
            "total": sum(self.scores.values())
        }
    
    def extract_scores_from_facts(self):
        """Extrait les scores des faits recommendation dans CLIPS"""
        try:
            for fact in self.env.facts():
                fact_str = str(fact)
                # Chercher les faits de type recommendation
                if 'recommendation' in fact_str:
                    # Extraction plus robuste
                    parts = fact_str.split()
                    domain = None
                    score = None
                    
                    for i, part in enumerate(parts):
                        if part == 'domain' and i + 1 < len(parts):
                            domain = parts[i + 1].strip(')')
                        if part == 'score' and i + 1 < len(parts):
                            score_str = parts[i + 1].strip(')')
                            try:
                                score = float(score_str)
                            except:
                                score = 0
                    
                    if domain and score is not None:
                        if domain in self.scores:
                            self.scores[domain] += score
                        else:
                            self.scores[domain] = score
        except Exception as e:
            if self.debug:
                print(f"Erreur extraction: {e}")
    
    def get_percentages(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Convertit les scores en pourcentages"""
        total = sum(scores.values())
        if total == 0:
            return {domain: 0.0 for domain in ["Ingenierie", "Medecine", "Design", "Droit", "Commerce"]}
        
        percentages = {}
        for domain, score in scores.items():
            percentages[domain] = (score / total) * 100
        
        # Ajouter les domaines manquants avec 0
        for domain in ["Ingenierie", "Medecine", "Design", "Droit", "Commerce"]:
            if domain not in percentages:
                percentages[domain] = 0.0
        
        return percentages
    
    def get_top_recommendations(self, percentages: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
        """Retourne les top N recommandations"""
        sorted_items = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:top_n]
    
    def reset(self):
        """Réinitialise complètement le moteur"""
        self.env.reset()
        self.scores = {}
    
    def get_stats(self) -> Dict[str, int]:
        """Retourne des statistiques sur le moteur"""
        return {
            "rules": len(list(self.env.rules())),
            "facts": len(list(self.env.facts())),
            "templates": len(self.env.templates)
        }