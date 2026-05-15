"""
Moteur de règles - Contient toutes les règles d'orientation
Chaque règle est une méthode distincte pour plus de clarté
"""

from typing import Dict, List
from orientation_expert.core2.faits.StudentFactBase import StudentFact


class RulesBase:
    """
    Moteur de règles d'orientation
    Chaque règle est encapsulée dans une méthode
    """
    
    def __init__(self):
        self.activated_rules: List[str] = []
    
    def apply_all_rules(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Applique toutes les règles d'orientation
        Retourne les scores mis à jour
        """
        self.activated_rules = []
        
        # Appliquer chaque règle
        scores = self.rule_engineering(facts, scores)
        scores = self.rule_medicine(facts, scores)
        scores = self.rule_design(facts, scores)
        scores = self.rule_law(facts, scores)
        scores = self.rule_business(facts, scores)
        
        return scores
    
    def get_activated_rules(self) -> List[str]:
        """Retourne la liste des règles qui ont été activées"""
        return self.activated_rules
    
    # ============================================
    # RÈGLE 1: INGÉNIERIE
    # ============================================
    def rule_engineering(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Règle d'orientation vers l'Ingénierie
        Conditions: maths >= 14 ET physique >= 14 (ou niveau moyen)
        Actions: Ajoute des points et bonus
        """
        math = facts.get_note("math")
        physics = facts.get_note("physics")
        rule_activated = False
        
        # Niveau excellent
        if math >= 14 and physics >= 14:
            score = (math * 2) + (physics * 2)
            scores["Ingenierie"] = scores.get("Ingenierie", 0) + score
            rule_activated = True
        # Niveau moyen
        elif math >= 12 or physics >= 12:
            score = (math + physics) * 1.5
            scores["Ingenierie"] = scores.get("Ingenierie", 0) + score
            rule_activated = True
        
        # Bonus pour qualités techniques
        technical_qualities = ["analytical", "logical", "problem-solving"]
        if any(q in facts.qualites for q in technical_qualities):
            scores["Ingenierie"] += 15
            rule_activated = True
        
        if rule_activated:
            self.activated_rules.append("Ingénierie")
        
        return scores
    
    # ============================================
    # RÈGLE 2: MÉDECINE
    # ============================================
    def rule_medicine(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Règle d'orientation vers la Médecine
        Conditions: biologie >= 15 ET chimie >= 14 (ou niveau moyen)
        Actions: Ajoute des points et bonus
        """
        bio = facts.get_note("biology")
        chem = facts.get_note("chemistry")
        rule_activated = False
        
        # Niveau excellent
        if bio >= 15 and chem >= 14:
            score = (bio * 2.5) + (chem * 1.5)
            scores["Medecine"] = scores.get("Medecine", 0) + score
            rule_activated = True
        # Niveau moyen
        elif bio >= 13 or chem >= 12:
            score = (bio + chem) * 1.8
            scores["Medecine"] = scores.get("Medecine", 0) + score
            rule_activated = True
        
        # Bonus pour qualités humaines
        human_qualities = ["empathy", "patient", "rigor"]
        if any(q in facts.qualites for q in human_qualities):
            scores["Medecine"] += 20
            rule_activated = True
        
        if rule_activated:
            self.activated_rules.append("Médecine")
        
        return scores
    
    # ============================================
    # RÈGLE 3: DESIGN
    # ============================================
    def rule_design(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Règle d'orientation vers le Design
        Conditions: arts >= 14 (ou niveau moyen)
        Actions: Ajoute des points et bonus
        """
        art = facts.get_note("art")
        rule_activated = False
        
        # Niveau excellent
        if art >= 14:
            score = art * 3
            scores["Design"] = scores.get("Design", 0) + score
            rule_activated = True
        # Niveau moyen
        elif art >= 11:
            score = art * 2
            scores["Design"] = scores.get("Design", 0) + score
            rule_activated = True
        
        # Bonus pour créativité
        creative_qualities = ["creative", "artistic", "imaginative"]
        if any(q in facts.qualites for q in creative_qualities):
            scores["Design"] += 15
            rule_activated = True
        
        if rule_activated:
            self.activated_rules.append("Design")
        
        return scores
    
    # ============================================
    # RÈGLE 4: DROIT
    # ============================================
    def rule_law(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Règle d'orientation vers le Droit
        Conditions: français >= 14 ET philosophie >= 13 (ou niveau moyen)
        Actions: Ajoute des points et bonus
        """
        french = facts.get_note("french")
        philo = facts.get_note("philosophy")
        rule_activated = False
        
        # Niveau excellent
        if french >= 14 and philo >= 13:
            score = (french * 1.8) + (philo * 1.5)
            scores["Droit"] = scores.get("Droit", 0) + score
            rule_activated = True
        # Niveau moyen
        elif french >= 12 or philo >= 11:
            score = (french + philo) * 1.3
            scores["Droit"] = scores.get("Droit", 0) + score
            rule_activated = True
        
        # Bonus pour argumentation
        argument_qualities = ["argumentative", "rigorous", "analytical"]
        if any(q in facts.qualites for q in argument_qualities):
            scores["Droit"] += 15
            rule_activated = True
        
        if rule_activated:
            self.activated_rules.append("Droit")
        
        return scores
    
    # ============================================
    # RÈGLE 5: COMMERCE
    # ============================================
    def rule_business(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Règle d'orientation vers le Commerce
        Conditions: économie >= 14 (ou niveau moyen)
        Actions: Ajoute des points et bonus
        """
        eco = facts.get_note("economics")
        rule_activated = False
        
        # Niveau excellent
        if eco >= 14:
            score = eco * 2.5
            scores["Commerce"] = scores.get("Commerce", 0) + score
            rule_activated = True
        # Niveau moyen
        elif eco >= 11:
            score = eco * 1.8
            scores["Commerce"] = scores.get("Commerce", 0) + score
            rule_activated = True
        
        # Bonus pour leadership
        leadership_qualities = ["leadership", "communication", "negotiation"]
        if any(q in facts.qualites for q in leadership_qualities):
            scores["Commerce"] += 15
            rule_activated = True
        
        if rule_activated:
            self.activated_rules.append("Commerce")
        
        return scores