"""
Calculateur de bonus basé sur les préférences
"""

from typing import Dict, List
from core2.faits.StudentFactBase import StudentFact


class BonusCalculator:
    """Calcule les bonus liés aux préférences"""
    
    def __init__(self):
        # Mapping des préférences vers les domaines
        self.preference_mapping = {
            # Ingénierie
            "technology": "Ingenierie",
            "engineering": "Ingenierie",
            "computers": "Ingenierie",
            "robotics": "Ingenierie",
            
            # Médecine
            "health": "Medecine",
            "medicine": "Medecine",
            "helping": "Medecine",
            "care": "Medecine",
            
            # Design
            "art": "Design",
            "design": "Design",
            "creativity": "Design",
            "drawing": "Design",
            
            # Droit
            "justice": "Droit",
            "law": "Droit",
            "debate": "Droit",
            "legal": "Droit",
            
            # Commerce
            "business": "Commerce",
            "entrepreneurship": "Commerce",
            "management": "Commerce",
            "marketing": "Commerce"
        }
        
        # Bonus de base (configurable)
        self.bonus_value = 15
        
        # Bonus maximum pour un même domaine (évite l'abus)
        self.max_bonus_per_domain = 30
    
    def apply_preference_bonus(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Applique les bonus en fonction des préférences de l'étudiant
        """
        # Compter combien de préférences pointent vers chaque domaine
        domain_count = {}
        
        for pref in facts.preferences:
            pref_lower = pref.lower()
            
            # Chercher le domaine correspondant
            for key, domain in self.preference_mapping.items():
                if key in pref_lower or pref_lower in key:
                    domain_count[domain] = domain_count.get(domain, 0) + 1

        
        # Appliquer les bonus
        for domain, count in domain_count.items():
            # Bonus = valeur de base × nombre de préférences (avec un maximum)
            bonus = min(self.bonus_value * count, self.max_bonus_per_domain)
            scores[domain] = scores.get(domain, 0) + bonus
        
        return scores