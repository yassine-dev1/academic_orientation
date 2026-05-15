"""
Calculateur de bonus basé sur les préférences
"""

from typing import Dict, List
from orientation_expert.core2.faits.StudentFactBase import StudentFact


class BonusCalculator:
    """Calcule les bonus liés aux préférences"""
    
    def __init__(self):
        self.preference_mapping = {
            "technology": "Ingenierie",
            "engineering": "Ingenierie",
            "computers": "Ingenierie",
            "health": "Medecine",
            "medicine": "Medecine",
            "helping": "Medecine",
            "art": "Design",
            "design": "Design",
            "creativity": "Design",
            "justice": "Droit",
            "law": "Droit",
            "debate": "Droit",
            "business": "Commerce",
            "entrepreneurship": "Commerce",
            "management": "Commerce"
        }
        self.bonus_value = 15
    
    def apply_preference_bonus(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Applique les bonus en fonction des préférences de l'étudiant
        """
        for pref in facts.preferences:
            pref_lower = pref.lower()
            if pref_lower in self.preference_mapping:
                domain = self.preference_mapping[pref_lower]
                scores[domain] = scores.get(domain, 0) + self.bonus_value
        
        return scores