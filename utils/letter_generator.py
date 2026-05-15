"""
Générateur de lettres de motivation avec Gemini AI
Gère les quotas et les erreurs de façon élégante
"""

from google import genai
from typing import Dict, List
from datetime import datetime
import time
import random

# Configuration de l'API Gemini
GEMINI_API_KEY = "AIzaSyAJ6jUbmOepJAPJqMu8lySVKmaARmmCNDo"

class AILetterGenerator:
    """Générateur de lettres de motivation avec IA"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.client = genai.Client(api_key=api_key)
        self.last_letter = ""
        self.model_name = "gemini-3-flash-preview" #"gemini-2.0-flash"
        self.request_count = 0
        self.last_request_time = 0
    
    def _respect_rate_limit(self):
        """Respecte la limite de 15 requêtes par minute"""
        current_time = time.time()
        if self.request_count >= 14:  # Laisser une marge
            elapsed = current_time - self.last_request_time
            if elapsed < 60:  # Si moins d'une minute
                wait_time = 60 - elapsed
                time.sleep(wait_time)
            self.request_count = 0
            self.last_request_time = time.time()
        else:
            self.request_count += 1
            if self.request_count == 1:
                self.last_request_time = current_time
    
    def generate_letter(self, 
                        best_domain: str,
                        best_percentage: float,
                        notes: Dict[str, float],
                        preferences: List[str],
                        qualities: List[str],
                        style: str = "professionnel") -> str:
        """
        Génère une lettre de motivation unique avec l'IA
        """
        
        # Préparer les données pour le prompt
        strong_subjects = [s for s, v in notes.items() if v >= 14]
        subjects_fr = {
            "math": "Mathématiques", "physics": "Physique", "biology": "Biologie",
            "chemistry": "Chimie", "french": "Français", "philosophy": "Philosophie",
            "economics": "Économie", "art": "Arts"
        }
        strong_names = [subjects_fr.get(s, s) for s in strong_subjects]
        
        qualities_fr = {
            "analytical": "esprit analytique", "logical": "logique", "creative": "créativité",
            "empathy": "empathie", "rigorous": "rigueur", "communication": "sens de la communication",
            "leadership": "leadership", "patient": "patience", "problem-solving": "résolution de problèmes",
            "artistic": "sens artistique", "argumentative": "capacité d'argumentation"
        }
        qualities_text = ", ".join([qualities_fr.get(q, q) for q in qualities[:4]]) if qualities else "motivation et sérieux"
        
        preferences_fr = {
            "technology": "la technologie et l'innovation",
            "health": "la santé et le bien-être",
            "art": "l'art et la créativité",
            "justice": "la justice et le droit",
            "business": "le commerce et la gestion",
            "engineering": "l'ingénierie",
            "medicine": "la médecine",
            "design": "le design"
        }
        preferences_text = ", ".join([preferences_fr.get(p, p) for p in preferences[:3]]) if preferences else "l'apprentissage et la découverte"
        
        # Styles d'écriture
        style_prompts = {
            "professionnel": """
                Rédige une lettre de motivation professionnelle, formelle et structurée.
                Utilise un ton respectueux et convaincant.
                Structure: Introduction, parcours académique, qualités personnelles, projet professionnel, conclusion.
            """,
            "creatif": """
                Rédige une lettre de motivation créative, originale et inspirante.
                Utilise des métaphores et un ton enthousiaste.
                Montre de la passion et de l'énergie.
            """,
            "concis": """
                Rédige une lettre de motivation courte et percutante (maximum 150 mots).
                Va droit au but, montre confiance et détermination.
            """
        }
        
        style_text = style_prompts.get(style, style_prompts["professionnel"])
        
        prompt = f"""
        Tu es un conseiller en orientation. Rédige une lettre de motivation UNIQUE et PERSONNALISÉE pour un étudiant.
        
        INFORMATIONS SUR L'ÉTUDIANT :
        - Domaine visé : {best_domain}
        - Compatibilité : {best_percentage:.1f}%
        - Matières fortes : {', '.join(strong_names) if strong_names else 'aucune en particulier mais bonne moyenne générale'}
        - Centres d'intérêt : {preferences_text}
        - Qualités personnelles : {qualities_text}
        
        STYLE DEMANDÉ : {style_text}
        
        CONSIGNES IMPORTANTES :
        - La lettre doit être DIFFÉRENTE à chaque génération
        - Utilise un vocabulaire VARIÉ
        - Adopte le point de vue de l'étudiant ("Je", "Mon", "Mes")
        - Sois CONVAINCANT et AUTHENTIQUE
        - La lettre doit faire environ 200-250 mots
        
        GÉNÈRE UNE LETTRE DE MOTIVATION COMPLÈTE :
        """
        
        # Respecter les limites de taux
        self._respect_rate_limit()
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            self.last_letter = response.text
            return self.last_letter
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print("⚠️ Quota API dépassé, utilisation d'une lettre template...")
                return self._generate_fallback_letter(best_domain, best_percentage, qualities_text)
            elif "404" in error_msg:
                print("⚠️ Modèle non disponible, tentative avec gemini-1.5-flash...")
                try:
                    response = self.client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=prompt
                    )
                    self.last_letter = response.text
                    return self.last_letter
                except:
                    return self._generate_fallback_letter(best_domain, best_percentage, qualities_text)
            else:
                print(f"Erreur API Gemini: {e}")
                return self._generate_fallback_letter(best_domain, best_percentage, qualities_text)
    
    def regenerate_letter(self, style: str = "professionnel") -> str:
        """Régénère une lettre avec des modifications spécifiques"""
        if not self.last_letter:
            return "Générez d'abord une lettre."
        
        prompt = f"""
        Voici une lettre de motivation existante :
        {self.last_letter}
        
        Génère une version complètement différente de cette lettre, avec le même style ({style}) mais des formulations entièrement nouvelles.
        
        Rédige une NOUVELLE VERSION de cette lettre, complètement DIFFÉRENTE.
        """
        
        try:
            self._respect_rate_limit()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            self.last_letter = response.text
            return self.last_letter
        except Exception as e:
            print(f"Erreur régénération: {e}")
            return self.last_letter
    
    def _generate_fallback_letter(self, domain: str, percentage: float, qualities: str) -> str:
        """Lettre de secours en cas d'erreur API - avec variations aléatoires"""
        date = datetime.now().strftime("%d/%m/%Y")
        
        # Variations pour que la lettre ne soit pas toujours identique
        intros = [
            f"Passionné par le domaine de {domain}",
            f"Fort d'un profil compatible à {percentage:.1f}% avec la filière {domain}",
            f"Convaincu que {domain} est la voie qui me correspond",
            f"Animé par une réelle passion pour {domain}"
        ]
        
        qualities_phrases = [
            f"Mes qualités principales sont : {qualities}.",
            f"Doté de {qualities}, je suis prêt à relever les défis.",
            f"Je possède des atouts tels que {qualities}.",
            f"Mes points forts incluent {qualities}."
        ]
        
        intro = random.choice(intros)
        quality_phrase = random.choice(qualities_phrases)
        
        return f"""
{date}

**Objet : Candidature pour une formation en {domain}**

Madame, Monsieur,

{intro}, je souhaite aujourd'hui intégrer votre formation pour concrétiser mon projet professionnel.

{quality_phrase} Ces atouts, combinés à ma motivation sans faille, me permettront de réussir pleinement dans cette voie.

Je serais ravi de pouvoir échanger avec vous lors d'un entretien pour vous exposer plus en détail ma motivation.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

[Votre signature]
"""


# Test rapide
if __name__ == "__main__":
    print("🧪 Test du générateur de lettres IA")
    print("=" * 40)
    
    generator = AILetterGenerator()
    
    test_notes = {"math": 16, "physics": 15, "french": 14}
    test_prefs = ["technology", "engineering"]
    test_quals = ["analytical", "logical", "problem-solving"]
    
    for style in ["professionnel", "creatif", "concis"]:
        print(f"\n📝 Style: {style}")
        print("-" * 40)
        letter = generator.generate_letter(
            best_domain="Ingénierie",
            best_percentage=78.5,
            notes=test_notes,
            preferences=test_prefs,
            qualities=test_quals,
            style=style
        )
        print(letter[:500] + "...\n")