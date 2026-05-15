"""
Moteur expert d'orientation académique - Version refactorisée
Sépare les faits, les règles et le traitement
"""

from typing import Dict, List, Any, Tuple, Optional
from core2.faits.StudentFactBase import StudentFact
from core2.regles import RulesBase
from core2.traitement import ScoreCalculator, BonusCalculator


class ExpertEngine:
    """
    Moteur expert d'orientation académique
    Utilise le chaînage avant (forward chaining)
    """
    
    def __init__(self):
        self.facts = StudentFact()
        self.rules_engine = RulesBase()
        self.score_calculator = ScoreCalculator()
        self.bonus_calculator = BonusCalculator()
        self.scores: Dict[str, float] = {}
        self.debug = False
    
    def set_debug(self, enabled: bool = True):
        """Active le mode debug"""
        self.debug = enabled
    
    def load_facts(self, 
                   notes: Dict[str, float],
                   preferences: List[str],
                   qualites: List[str],
                   riasec: Optional[Dict[str, int]] = None,
                   valeurs: Optional[Dict[str, int]] = None):
        """
        Charge les faits de l'étudiant dans la base de connaissances
        """
        self.facts = StudentFact()
        
        for subject, grade in notes.items():
            self.facts.add_note(subject, grade)
        
        for pref in preferences:
            self.facts.add_preference(pref)
        
        for qualite in qualites:
            self.facts.add_qualite(qualite)
        
        # Charger les scores RIASEC
        if riasec:
            for trait, score in riasec.items():
                self.facts.set_riasec(trait, score)
        
        # Charger les valeurs professionnelles
        if valeurs:
            for valeur, score in valeurs.items():
                self.facts.set_valeur(valeur, score)
    
    def evaluate_student(self, 
                         notes: Dict[str, float],
                         preferences: List[str],
                         qualites: List[str],
                         riasec: Optional[Dict[str, int]] = None,
                         valeurs: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Évalue un étudiant avec le chaînage avant
        """
        # 1. Charger les faits
        self.load_facts(notes, preferences, qualites, riasec, valeurs)
        
        # 2. Initialiser les scores
        self.scores = self.score_calculator.init_scores()
        
        if self.debug:
            self._print_debug_info()
        
        # 3. Appliquer toutes les règles (chaînage avant)
        #    Inclut: règles académiques + RIASEC + valeurs professionnelles
        self.scores = self.rules_engine.apply_all_rules(self.facts, self.scores)
        
        # 4. Appliquer les bonus de préférences
        self.scores = self.bonus_calculator.apply_preference_bonus(self.facts, self.scores)
        
        # 5. Calculer les pourcentages
        percentages = self.score_calculator.calculate_percentages(self.scores)
        total = sum(self.scores.values())
        
        if self.debug:
            self._print_results(percentages)
            self._print_activated_rules()
        
        return {
            "scores": self.scores,
            "percentages": percentages,
            "total": total
        }
    
    def _print_debug_info(self):
        """Affiche les informations de debug"""
        print("\n" + "="*50)
        print("🔍 ÉVALUATION DU PROFIL ÉTUDIANT")
        print("="*50)
        print(f"📚 Notes: {self.facts.notes}")
        print(f"🎯 Préférences: {self.facts.preferences}")
        print(f"⭐ Qualités: {self.facts.qualites}")
        if self.facts.riasec:
            print(f"🧭 RIASEC: {self.facts.riasec}")
        if self.facts.valeurs:
            print(f"💎 Valeurs: {self.facts.valeurs}")
        print("-"*40)
    
    def _print_results(self, percentages: Dict[str, float]):
        """Affiche les résultats finaux"""
        print("\n" + "="*40)
        print("📊 RÉSULTATS FINAUX")
        print("="*40)
        for domain, score in self.scores.items():
            bar = "█" * int(percentages[domain] / 5)
            print(f"  {domain:12} | {bar:20} {percentages[domain]:.1f}% ({score} pts)")
    
    def _print_activated_rules(self):
        """Affiche les règles activées"""
        activated = self.rules_engine.get_activated_rules()
        if activated:
            print("\n📋 Règles activées:", ", ".join(activated))
    
    def get_top_recommendations(self, percentages: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
        """Retourne les top N recommandations"""
        return self.score_calculator.get_top_recommendations(percentages, top_n)
    
    def get_best_domain(self, percentages: Dict[str, float]) -> Tuple[str, float]:
        """Retourne le meilleur domaine"""
        return self.score_calculator.get_best_domain(percentages)
    
    def get_activated_rules(self) -> List[str]:
        """Retourne la liste des règles activées"""
        return self.rules_engine.get_activated_rules()
    
    def reset(self):
        """Réinitialise le moteur"""
        self.facts = StudentFact()
        self.scores = {}


# Test rapide
if __name__ == "__main__":
    engine = ExpertEngine()
    engine.set_debug(True)
    
    notes = {
        "math": 17,
        "physics": 16,
        "biology": 15,
        "chemistry": 14,
        "art": 13,
        "french": 14,
        "philosophy": 12,
        "economics": 15
    }
    
    preferences = ["technology", "engineering"]
    qualities = ["analytical", "logical", "problem-solving"]
    
    # Test avec RIASEC et Valeurs
    riasec = {
        "realistic": 8,
        "investigative": 9,
        "artistic": 4,
        "social": 5,
        "enterprising": 6,
        "conventional": 5
    }
    
    valeurs = {
        "stability": 6,
        "creativity": 8,
        "social_impact": 4,
        "prestige": 5,
        "autonomy": 7,
        "leadership": 5
    }
    
    result = engine.evaluate_student(notes, preferences, qualities, riasec, valeurs)
    
    best = engine.get_best_domain(result["percentages"])
    print(f"\n🏆 MEILLEURE ORIENTATION: {best[0]} ({best[1]:.1f}%)")