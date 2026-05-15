"""
Générateur de conseils personnalisés avec Gemini AI
Utilise l'API Gemini pour des conseils intelligents et uniques
"""

from google import genai
from typing import Dict, List
from datetime import datetime
import random
import time

# Configuration de l'API Gemini
GEMINI_API_KEY = "AIzaSyAJ6jUbmOepJAPJqMu8lySVKmaARmmCNDo"

class AdviceGenerator:
    """Générateur de conseils personnalisés avec IA"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3-flash-preview" #"gemini-2.0-flash"
        self.last_advice = ""
        self.request_count = 0
        self.last_request_time = 0
    
    def _respect_rate_limit(self):
        """Respecte la limite de requêtes"""
        current_time = time.time()
        if self.request_count >= 14:
            elapsed = current_time - self.last_request_time
            if elapsed < 60:
                wait_time = 60 - elapsed
                time.sleep(wait_time)
            self.request_count = 0
            self.last_request_time = time.time()
        else:
            self.request_count += 1
            if self.request_count == 1:
                self.last_request_time = current_time
    
    def generate_advice(self, 
                        best_domain: str,
                        best_percentage: float,
                        all_scores: Dict[str, float],
                        notes: Dict[str, float],
                        preferences: List[str],
                        qualities: List[str]) -> Dict[str, any]:
        """
        Génère des conseils personnalisés avec l'IA
        """
        
        # Préparer les données pour le prompt
        subjects_fr = {
            "math": "Mathématiques", "physics": "Physique", "biology": "Biologie",
            "chemistry": "Chimie", "french": "Français", "philosophy": "Philosophie",
            "economics": "Économie", "art": "Arts"
        }
        
        # Notes formatées
        notes_text = "\n".join([f"- {subjects_fr.get(s, s)} : {v}/20" for s, v in notes.items()])
        
        # Scores des autres domaines
        other_scores = {d: s for d, s in all_scores.items() if d != best_domain}
        other_scores_text = "\n".join([f"- {d} : {s:.1f}%" for d, s in sorted(other_scores.items(), key=lambda x: x[1], reverse=True)[:3]])
        
        # Qualités
        qualities_text = ", ".join(qualities) if qualities else "À déterminer"
        
        # Préférences
        preferences_text = ", ".join(preferences) if preferences else "À explorer"
        
        prompt = f"""
        Tu es un conseiller d'orientation professionnel expérimenté. Analyse le profil de l'étudiant suivant et fournis des conseils personnalisés et détaillés.

        ## PROFIL DE L'ÉTUDIANT

        **Domaine d'orientation principal :** {best_domain}
        **Compatibilité :** {best_percentage:.1f}%

        **Scores dans les autres domaines :**
        {other_scores_text}

        **Notes scolaires :**
        {notes_text}

        **Centres d'intérêt :** {preferences_text}

        **Qualités personnelles :** {qualities_text}

        ## TON RÔLE

        Tu dois fournir une analyse complète et professionnelle avec les sections suivantes :

        1. **ANALYSE GLOBALE** : Évalue la cohérence du profil, points forts principaux
        2. **CONSEILS ACADÉMIQUES** : Matières à renforcer, ressources recommandées
        3. **DÉVELOPPEMENT PERSONNEL** : Compétences transversales à développer
        4. **PLAN D'ACTION** : Étapes concrètes sur 6 mois
        5. **FORMATIONS RECOMMANDÉES** : Parcours spécifiques adaptés au profil
        6. **MÉTIERS CIBLES** : 5 métiers correspondant au profil
        7. **CONCLUSION MOTIVANTE** : Message personnalisé encourageant

        ## CONSIGNES

        - Sois précis et personnalisé (ne donne pas de conseils génériques)
        - Propose des ressources concrètes (livres, MOOCs, sites web)
        - Adapte les conseils au niveau scolaire de l'étudiant
        - Utilise un ton professionnel mais encourageant
        - La réponse doit faire environ 800-1000 mots
        - Structure la réponse avec des titres et puces

        GÉNÈRE UN RAPPORT D'ORIENTATION COMPLET ET PERSONNALISÉ :
        """
        
        self._respect_rate_limit()
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            self.last_advice = response.text
            return self._parse_advice_response(self.last_advice, best_domain, best_percentage)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print("⚠️ Quota API dépassé, utilisation de conseils templates...")
                return self._generate_fallback_advice(best_domain, best_percentage, notes, qualities, preferences)
            else:
                print(f"⚠️ Erreur API: {e}")
                return self._generate_fallback_advice(best_domain, best_percentage, notes, qualities, preferences)
    
    def _parse_advice_response(self, response_text: str, domain: str, percentage: float) -> Dict:
        """Parse la réponse de l'API en dictionnaire structuré"""
        
        # Si l'API a bien répondu, on retourne un dict structuré
        # avec le texte brut et des métadonnées
        return {
            "full_text": response_text,
            "domain": domain,
            "percentage": percentage,
            "generated_by_ai": True
        }
    
    def _generate_fallback_advice(self, domain: str, percentage: float, 
                                   notes: Dict, qualities: List, preferences: List) -> Dict:
        """Conseils de secours (quand API indisponible)"""
        
        subjects_fr = {
            "math": "Mathématiques", "physics": "Physique", "biology": "Biologie",
            "chemistry": "Chimie", "french": "Français", "philosophy": "Philosophie",
            "economics": "Économie", "art": "Arts"
        }
        
        # Analyse des forces
        strong_subjects = [subjects_fr.get(s, s) for s, v in notes.items() if v >= 14]
        weak_subjects = [subjects_fr.get(s, s) for s, v in notes.items() if v < 11]
        
        # Conseils spécifiques par domaine
        domain_advice = {
            "Ingenierie": {
                "academic": "Renforcez vos bases en mathématiques et physique. Suivez des cours en ligne sur la programmation (Python, C++).",
                "resources": "Coursera : 'Introduction to Engineering', OpenClassrooms : 'Préparez-vous pour une école d'ingénieur'",
                "studies": "Classes Préparatoires MPSI/PCSI, BUT GEII/GMP, Licence Sciences pour l'ingénieur"
            },
            "Medecine": {
                "academic": "Consolidez vos connaissances en biologie et chimie. Commencez à vous familiariser avec la terminologie médicale.",
                "resources": "Khan Academy : 'Biology', Coursera : 'Introduction to Human Physiology'",
                "studies": "PASS (Parcours Spécifique Accès Santé), L.AS (Licence avec option santé)"
            },
            "Design": {
                "academic": "Développez votre créativité au quotidien. Apprenez les bases des logiciels de design (Figma, Photoshop, Illustrator).",
                "resources": "Behance, Dribbble pour l'inspiration, Coursera : 'Graphic Design Specialization'",
                "studies": "MANAA, BTS Design Graphique, DNA (Diplôme National d'Arts)"
            },
            "Droit": {
                "academic": "Travaillez votre expression écrite et votre logique. Suivez l'actualité juridique.",
                "resources": "Légifrance, Dalloz, Coursera : 'Introduction to Law'",
                "studies": "Licence Droit, Double Licence Droit-Économie, IPAG"
            },
            "Commerce": {
                "academic": "Développez votre culture économique et votre anglais. Entraînez-vous à la prise de parole.",
                "resources": "Les Echos, Harvard Business Review, LinkedIn Learning",
                "studies": "Prépa ECG, BUT TC (Techniques de Commercialisation), Licence Économie-Gestion"
            }
        }
        
        default = domain_advice.get(domain, {
            "academic": "Continuez à travailler l'ensemble des matières. Identifiez vos véritables passions.",
            "resources": "ONISEP, CIDJ, Parcoursup",
            "studies": "Licence générale dans le domaine, BUT adapté"
        })
        
        # Construction du texte complet
        full_text = f"""
{'='*60}
🎓 RAPPORT D'ORIENTATION PERSONNALISÉ
{'='*60}

## 📊 ANALYSE GLOBALE

**Domaine recommandé :** {domain}
**Taux de compatibilité :** {percentage:.1f}%

Votre profil présente une adéquation intéressante avec le domaine {domain}.

**Points forts académiques :** {', '.join(strong_subjects) if strong_subjects else 'Matières variées'}
**Qualités identifiées :** {', '.join(qualities[:3]) if qualities else 'Motivation et sérieux'}

{'⚠️ Axes de progression : ' + ', '.join(weak_subjects) if weak_subjects else ''}

---

## 📚 CONSEILS ACADÉMIQUES

{default['academic']}

**Ressources recommandées :**
{default['resources']}

---

## 🌟 DÉVELOPPEMENT PERSONNEL

Compétences à développer :
• Autonomie et organisation
• Esprit critique et capacité d'analyse
• Communication et travail en équipe
• Veille technologique et culture générale

---

## 📋 PLAN D'ACTION (6 mois)

**Mois 1-2 :** Documentation et exploration
- Renseignez-vous sur les formations disponibles
- Contactez des étudiants et professionnels du secteur
- Suivez des MOOCs d'introduction

**Mois 3-4 :** Préparation active
- Renforcez vos compétences dans les matières clés
- Participez à des ateliers ou stages
- Préparez vos dossiers de candidature

**Mois 5-6 :** Candidatures
- Finalisez vos dossiers Parcoursup
- Préparez-vous aux entretiens de sélection
- Envisagez des formations complémentaires

---

## 🎓 FORMATIONS RECOMMANDÉES

{default['studies']}

---

## 💼 MÉTIERS CIBLES

{self._get_careers_text(domain)}

---

## 💡 CONCLUSION

Vous êtes sur la bonne voie pour réussir dans le domaine {domain} ! 
Avec de la détermination et un travail ciblé, vous avez toutes les chances 
de concrétiser votre projet professionnel.

N'hésitez pas à multiplier les expériences (stages, bénévolat, projets personnels) 
pour affiner votre projet et enrichir votre candidature.

{'='*60}
✨ Conseil personnalisé généré - Bonne continuation dans votre parcours !
{'='*60}
"""
        
        return {
            "full_text": full_text,
            "domain": domain,
            "percentage": percentage,
            "generated_by_ai": False
        }
    
    def _get_careers_text(self, domain: str) -> str:
        """Retourne les métiers pour un domaine"""
        careers = {
            "Ingenierie": "• Ingénieur logiciel\n• Ingénieur civil\n• Data scientist\n• Chef de projet technique\n• Consultant en innovation",
            "Medecine": "• Médecin généraliste\n• Chirurgien\n• Pédiatre\n• Chercheur médical\n• Médecin du travail",
            "Design": "• Designer UX/UI\n• Designer produit\n• Directeur artistique\n• Architecte d'intérieur\n• Motion designer",
            "Droit": "• Avocat\n• Juriste d'entreprise\n• Magistrat\n• Notaire\n• Conseiller juridique",
            "Commerce": "• Chef d'entreprise\n• Consultant\n• Responsable marketing\n• Contrôleur de gestion\n• Business developer"
        }
        return careers.get(domain, "• À explorer selon votre spécialisation")
    
    def regenerate_advice(self) -> Dict:
        """Régénère des conseils avec l'IA"""
        if not self.last_advice:
            return {"full_text": "Générez d'abord des conseils.", "generated_by_ai": False}
        
        prompt = f"""
        Voici un rapport d'orientation existant :
        {self.last_advice}
        
        Génère une version complètement différente de ce rapport, avec des conseils encore plus personnalisés et des recommandations nouvelles.
        Garde la même structure mais change les formulations et ajoute des conseils originaux.
        """
        
        try:
            self._respect_rate_limit()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            self.last_advice = response.text
            return self._parse_advice_response(self.last_advice, "", 0)
        except Exception as e:
            print(f"Erreur régénération: {e}")
            return self._parse_advice_response(self.last_advice, "", 0)


# Fonction pour formater l'affichage
def format_advice_for_display(advice_dict: Dict) -> str:
    """Formate le rapport pour affichage"""
    return advice_dict.get("full_text", "Aucun conseil disponible.")


# Test
if __name__ == "__main__":
    print("🧪 Test du générateur de conseils IA")
    print("=" * 40)
    
    generator = AdviceGenerator()
    
    test_notes = {
        "math": 16, "physics": 15, "biology": 12, "chemistry": 11,
        "french": 14, "philosophy": 13, "economics": 15, "art": 10
    }
    test_prefs = ["technology", "engineering"]
    test_quals = ["analytical", "logical", "problem-solving", "rigorous"]
    
    advice = generator.generate_advice(
        best_domain="Ingénierie",
        best_percentage=78.5,
        all_scores={"Ingenierie": 78.5, "Medecine": 45.2, "Design": 52.3, "Droit": 48.1, "Commerce": 62.0},
        notes=test_notes,
        preferences=test_prefs,
        qualities=test_quals
    )
    
    print(format_advice_for_display(advice))