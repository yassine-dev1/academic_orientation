"""
Calculateur de scores et pourcentages
"""

from typing import Dict, List, Tuple


class ScoreCalculator:
    """Calcule les scores et pourcentages à partir des résultats des règles"""
    
    def __init__(self):
        self.scores: Dict[str, float] = {}
        self.domains = ["Ingenierie", "Medecine", "Design", "Droit", "Commerce"]
    
    def init_scores(self) -> Dict[str, float]:
        """Initialise tous les scores à zéro"""
        return {domain: 0.0 for domain in self.domains}
    
    def calculate_percentages(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Convertit les scores en pourcentages
        """
        total = sum(scores.values())
        
        if total == 0:
            return {domain: 0.0 for domain in self.domains}
        
        percentages = {}
        for domain in self.domains:
            score = scores.get(domain, 0)
            percentages[domain] = round((score / total) * 100, 1)
        
        return percentages
    
    def get_top_recommendations(self, percentages: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
        """Retourne les top N recommandations"""
        sorted_items = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:top_n]
    
    def get_best_domain(self, percentages: Dict[str, float]) -> Tuple[str, float]:
        """Retourne le meilleur domaine"""
        sorted_items = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[0] if sorted_items else ("Aucun", 0.0)