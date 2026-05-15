"""
Système expert d'orientation académique - Version finale
100% Python, compatible avec Python 3.14
Aucune dépendance externe requise
"""

from typing import Dict, List, Any, Tuple


class ExpertEngine:
    """Moteur expert d'orientation académique"""
    
    def __init__(self):
        self.scores: Dict[str, float] = {}
        self.debug = False
    
    def set_debug(self, enabled: bool = True):
        """Active le mode debug pour voir les règles activées"""
        self.debug = enabled
    
    def evaluate_student(self, 
                         notes: Dict[str, float],
                         preferences: List[str],
                         qualites: List[str]) -> Dict[str, Any]:
        """
        Évalue un étudiant et retourne les scores
        
        Args:
            notes: Dictionnaire des notes par matière (ex: {"math": 16, "physics": 15})
            preferences: Liste des centres d'intérêt (ex: ["technology", "health"])
            qualites: Liste des qualités personnelles (ex: ["analytical", "logical"])
        
        Returns:
            Dictionnaire avec scores et pourcentages
        """
        
        # Initialisation des scores
        self.scores = {
            "Ingenierie": 0,
            "Medecine": 0,
            "Design": 0,
            "Droit": 0,
            "Commerce": 0
        }
        
        if self.debug:
            print("\n" + "="*50)
            print("🔍 ÉVALUATION DU PROFIL ÉTUDIANT")
            print("="*50)
            print(f"📚 Notes: {notes}")
            print(f"🎯 Préférences: {preferences}")
            print(f"⭐ Qualités: {qualites}")
            print("-"*40)
        
        # ============================================
        # RÈGLE 1: INGÉNIERIE
        # ============================================
        math = notes.get("math", 0)
        physics = notes.get("physics", 0)
        
        if math >= 14 and physics >= 14:
            score = (math * 2) + (physics * 2)
            self.scores["Ingenierie"] += score
            if self.debug:
                print(f"✅ Ingénierie: maths={math}, physique={physics} → +{score} pts")
        elif math >= 12 or physics >= 12:
            score = (math + physics) * 1.5
            self.scores["Ingenierie"] += score
            if self.debug:
                print(f"📌 Ingénierie (niveau moyen): +{score} pts")
        
        # Bonus pour qualités techniques
        if "analytical" in qualites or "logical" in qualites or "problem-solving" in qualites:
            self.scores["Ingenierie"] += 15
            if self.debug:
                print(f"🎁 Bonus Ingénierie (qualités techniques): +15 pts")
        
        # ============================================
        # RÈGLE 2: MÉDECINE
        # ============================================
        bio = notes.get("biology", 0)
        chem = notes.get("chemistry", 0)
        
        if bio >= 15 and chem >= 14:
            score = (bio * 2.5) + (chem * 1.5)
            self.scores["Medecine"] += score
            if self.debug:
                print(f"✅ Médecine: biologie={bio}, chimie={chem} → +{score} pts")
        elif bio >= 13 or chem >= 12:
            score = (bio + chem) * 1.8
            self.scores["Medecine"] += score
            if self.debug:
                print(f"📌 Médecine (niveau moyen): +{score} pts")
        
        # Bonus pour qualités humaines
        if "empathy" in qualites or "patient" in qualites or "rigor" in qualites:
            self.scores["Medecine"] += 20
            if self.debug:
                print(f"🎁 Bonus Médecine (qualités humaines): +20 pts")
        
        # ============================================
        # RÈGLE 3: DESIGN
        # ============================================
        art = notes.get("art", 0)
        
        if art >= 14:
            score = art * 3
            self.scores["Design"] += score
            if self.debug:
                print(f"✅ Design: arts={art} → +{score} pts")
        elif art >= 11:
            score = art * 2
            self.scores["Design"] += score
            if self.debug:
                print(f"📌 Design (niveau moyen): +{score} pts")
        
        # Bonus créativité
        if "creative" in qualites or "artistic" in qualites or "imaginative" in qualites:
            self.scores["Design"] += 15
            if self.debug:
                print(f"🎁 Bonus Design (créativité): +15 pts")
        
        # ============================================
        # RÈGLE 4: DROIT
        # ============================================
        french = notes.get("french", 0)
        philo = notes.get("philosophy", 0)
        
        if french >= 14 and philo >= 13:
            score = (french * 1.8) + (philo * 1.5)
            self.scores["Droit"] += score
            if self.debug:
                print(f"✅ Droit: français={french}, philosophie={philo} → +{score} pts")
        elif french >= 12 or philo >= 11:
            score = (french + philo) * 1.3
            self.scores["Droit"] += score
            if self.debug:
                print(f"📌 Droit (niveau moyen): +{score} pts")
        
        # Bonus argumentation
        if "argumentative" in qualites or "rigorous" in qualites or "analytical" in qualites:
            self.scores["Droit"] += 15
            if self.debug:
                print(f"🎁 Bonus Droit (argumentation): +15 pts")
        
        # ============================================
        # RÈGLE 5: COMMERCE
        # ============================================
        eco = notes.get("economics", 0)
        
        if eco >= 14:
            score = eco * 2.5
            self.scores["Commerce"] += score
            if self.debug:
                print(f"✅ Commerce: économie={eco} → +{score} pts")
        elif eco >= 11:
            score = eco * 1.8
            self.scores["Commerce"] += score
            if self.debug:
                print(f"📌 Commerce (niveau moyen): +{score} pts")
        
        # Bonus leadership
        if "leadership" in qualites or "communication" in qualites or "negotiation" in qualites:
            self.scores["Commerce"] += 15
            if self.debug:
                print(f"🎁 Bonus Commerce (leadership): +15 pts")
        
        # ============================================
        # PRISE EN COMPTE DES PRÉFÉRENCES
        # ============================================
        preference_mapping = {
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
        
        for pref in preferences:
            pref_lower = pref.lower()
            if pref_lower in preference_mapping:
                domain = preference_mapping[pref_lower]
                self.scores[domain] += 15
                if self.debug:
                    print(f"🎯 Préférence '{pref}' → +15 pts pour {domain}")
        
        # ============================================
        # CALCUL DES POURCENTAGES
        # ============================================
        total = sum(self.scores.values())
        
        if total == 0:
            percentages = {d: 0.0 for d in self.scores.keys()}
        else:
            percentages = {d: (s / total) * 100 for d, s in self.scores.items()}
        
        # Arrondir les pourcentages
        percentages = {k: round(v, 1) for k, v in percentages.items()}
        
        if self.debug:
            print("\n" + "="*40)
            print("📊 RÉSULTATS FINAUX")
            print("="*40)
            for domain, score in self.scores.items():
                bar = "█" * int(percentages[domain] / 5)
                print(f"  {domain:12} | {bar:20} {percentages[domain]:.1f}% ({score} pts)")
        
        return {
            "scores": self.scores,
            "percentages": percentages,
            "total": total
        }
    
    def get_top_recommendations(self, percentages: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
        """Retourne les top N recommandations"""
        sorted_items = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:top_n]
    
    def get_best_domain(self, percentages: Dict[str, float]) -> Tuple[str, float]:
        """Retourne le meilleur domaine et son score"""
        sorted_items = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        if sorted_items:
            return sorted_items[0]
        return ("Aucun", 0.0)
    
    def reset(self):
        """Réinitialise le moteur"""
        self.scores = {}


# Test rapide
if __name__ == "__main__":
    engine = ExpertEngine()
    engine.set_debug(True)
    
    # Profil de test
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
    
    result = engine.evaluate_student(notes, preferences, qualities)
    
    best = engine.get_best_domain(result["percentages"])
    print(f"\n🏆 MEILLEURE ORIENTATION: {best[0]} ({best[1]:.1f}%)")