"""
Moteur de règles - Contient toutes les règles d'orientation
Chaque règle est une méthode distincte pour plus de clarté
"""

from typing import Dict, List
from core2.faits.StudentFactBase import StudentFact


class RulesBase:
    """
    Moteur de règles d'orientation
    Chaque règle est encapsulée dans une méthode
    """
    
    def __init__(self):
        self.activated_rules: List[str] = []
        
        # Matrice de scoring RIASEC → Domaines
        # Chaque type RIASEC donne des points aux domaines selon sa pertinence
        self.riasec_matrix = {
            "realistic":      {"Ingenierie": 3, "Medecine": 0, "Design": 1, "Droit": 0, "Commerce": 0},
            "investigative":  {"Ingenierie": 2, "Medecine": 3, "Design": 0, "Droit": 1, "Commerce": 0},
            "artistic":       {"Ingenierie": 0, "Medecine": 0, "Design": 3, "Droit": 0, "Commerce": 0},
            "social":         {"Ingenierie": 0, "Medecine": 2, "Design": 0, "Droit": 2, "Commerce": 1},
            "enterprising":   {"Ingenierie": 0, "Medecine": 0, "Design": 0, "Droit": 1, "Commerce": 3},
            "conventional":   {"Ingenierie": 1, "Medecine": 0, "Design": 0, "Droit": 2, "Commerce": 2},
        }
        
        # Matrice de scoring Valeurs professionnelles → Domaines
        self.values_matrix = {
            "stability":      {"Ingenierie": 1, "Medecine": 2, "Design": 0, "Droit": 2, "Commerce": 1},
            "creativity":     {"Ingenierie": 2, "Medecine": 0, "Design": 3, "Droit": 0, "Commerce": 1},
            "social_impact":  {"Ingenierie": 0, "Medecine": 3, "Design": 0, "Droit": 2, "Commerce": 0},
            "prestige":       {"Ingenierie": 1, "Medecine": 2, "Design": 0, "Droit": 2, "Commerce": 2},
            "autonomy":       {"Ingenierie": 2, "Medecine": 0, "Design": 2, "Droit": 0, "Commerce": 1},
            "leadership":     {"Ingenierie": 0, "Medecine": 0, "Design": 0, "Droit": 2, "Commerce": 3},
        }
    
    def apply_all_rules(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Applique toutes les règles d'orientation
        Retourne les scores mis à jour
        """
        self.activated_rules = []
        
        # Appliquer les règles académiques (notes + qualités)
        scores = self.rule_engineering(facts, scores)
        scores = self.rule_medicine(facts, scores)
        scores = self.rule_design(facts, scores)
        scores = self.rule_law(facts, scores)
        scores = self.rule_business(facts, scores)
        
        # Appliquer les règles RIASEC
        scores = self.apply_riasec_rules(facts, scores)
        
        # Appliquer les règles des valeurs professionnelles
        scores = self.apply_values_rules(facts, scores)
        
        return scores
    
    def get_activated_rules(self) -> List[str]:
        """Retourne la liste des règles qui ont été activées"""
        return self.activated_rules
    
    # ============================================
    # RÈGLES RIASEC (Holland)
    # ============================================
    def apply_riasec_rules(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
    """
    Applique les bonus/malus RIASEC selon la matrice de scoring.
    
    Règles :
    - Score > 7 : bonus élevé (fort intérêt)
    - Score 5-7 : bonus modéré (intérêt moyen)
    - Score 3-5 : pas de changement (neutre)
    - Score < 3 : malus (désintérêt fort)
    
    Formule bonus : (score - 5) * coeff * facteur_normalisation
    Formule malus : (score - 5) * coeff * 0.5 (pour scores < 5)
    """
    if not facts.riasec:
        return scores
    
    riasec_activated = False
    NORMALIZATION_FACTOR = 0.5  # Évite que RIASEC domine trop
    MAX_BONUS_PER_DOMAIN = 15    # Plafond pour un domaine
    
    for trait, score in facts.riasec.items():
        if trait not in self.riasec_matrix:
            continue
            
        coefficients = self.riasec_matrix[trait]
        
        for domain, coeff in coefficients.items():
            if coeff == 0:
                continue
            
            if score > 5:
                # Bonus pour intérêt élevé
                excess = score - 5  # de 1 à 5
                bonus = excess * coeff * NORMALIZATION_FACTOR
                scores[domain] = scores.get(domain, 0) + bonus
                riasec_activated = True
                
            elif score < 3:
                # Malus pour désintérêt marqué
                deficit = 3 - score  # de 1 à 2
                malus = deficit * coeff * NORMALIZATION_FACTOR * 0.7
                scores[domain] = scores.get(domain, 0) - malus
                riasec_activated = True
        
        if riasec_activated:
            self.activated_rules.append("RIASEC")
        
        return scores
    
    # ============================================
    # RÈGLES VALEURS PROFESSIONNELLES
    # ============================================
    def apply_values_rules(self, facts: StudentFact, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Applique les bonus des valeurs professionnelles selon la matrice.
        Pour chaque valeur au-dessus du seuil (5), on ajoute un bonus
        proportionnel au score de l'étudiant.
        Formule: bonus = (score_valeur - 5) * coefficient_matrice
        """
        if not facts.valeurs:
            return scores
        
        values_activated = False
        NORMALIZATION_FACTOR = 0.5  # Évite que RIASEC domine trop
        MAX_BONUS_PER_DOMAIN = 15    # Plafond pour un domaine

    for trait, score in facts.valeurs.items():
        if trait not in self.values_matrix:
            continue
            
        coefficients = self.values_matrix[trait]
        
        for domain, coeff in coefficients.items():
            if coeff == 0:
                continue
            
            if score > 5:
                # Bonus pour intérêt élevé
                excess = score - 5  # de 1 à 5
                bonus = excess * coeff * NORMALIZATION_FACTOR
                scores[domain] = scores.get(domain, 0) + bonus
                values_activated = True
                
            elif score < 3:
                # Malus pour désintérêt marqué
                deficit = 3 - score  # de 1 à 2
                malus = deficit * coeff * NORMALIZATION_FACTOR * 0.7
                scores[domain] = scores.get(domain, 0) - malus
                values_activated = True
                
        
        if values_activated:
            self.activated_rules.append("Valeurs Pro")
        
        return scores
    
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