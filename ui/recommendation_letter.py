"""
Générateur de lettre de recommandation personnalisée
"""

from datetime import datetime
from typing import Dict, List


class RecommendationLetterGenerator:
    """Générateur de lettres de motivation personnalisées"""
    
    def __init__(self, student_name: str = "Étudiant"):
        self.student_name = student_name
        self.date = datetime.now().strftime("%d/%m/%Y")
    
    def generate_letter(self, 
                        best_domain: str, 
                        best_percentage: float,
                        notes: Dict[str, float],
                        preferences: List[str],
                        qualities: List[str],
                        style: str = "professionnel") -> str:
        """
        Génère une lettre de motivation personnalisée
        
        Args:
            best_domain: Meilleur domaine d'orientation
            best_percentage: Pourcentage de compatibilité
            notes: Dictionnaire des notes
            preferences: Liste des préférences
            qualities: Liste des qualités
            style: Style de la lettre (professionnel, enthousiaste, concis)
        
        Returns:
            Lettre de motivation formatée
        """
        
        if style == "professionnel":
            return self._generate_professional_letter(best_domain, best_percentage, notes, preferences, qualities)
        elif style == "enthousiaste":
            return self._generate_enthusiastic_letter(best_domain, best_percentage, notes, preferences, qualities)
        else:
            return self._generate_concise_letter(best_domain, best_percentage, notes, preferences, qualities)
    
    def _generate_professional_letter(self, 
                                      best_domain: str, 
                                      best_percentage: float,
                                      notes: Dict[str, float],
                                      preferences: List[str],
                                      qualities: List[str]) -> str:
        """Génère une lettre au style professionnel"""
        
        # Identifier les points forts académiques
        strong_subjects = [s for s, v in notes.items() if v >= 14]
        strong_subjects_fr = self._translate_subjects(strong_subjects)
        
        # Qualités formatées
        qualities_fr = self._translate_qualities(qualities[:3])
        
        # Préférences formatées
        preferences_fr = self._translate_preferences(preferences[:2])
        
        letter = f"""
{self.date}

**Objet : Candidature pour une formation en {best_domain}**

Madame, Monsieur,

Actuellement étudiant, je me permets de vous adresser ma candidature pour intégrer une formation dans le domaine de {best_domain}. Après une analyse approfondie de mon profil académique et personnel, je suis convaincu que cette voie correspond parfaitement à mes aspirations et à mes compétences.

**📊 Profil académique**
Mes résultats scolaires démontrent une compatibilité de {best_percentage:.1f}% avec les exigences de la filière {best_domain}. Je me distingue particulièrement dans les matières suivantes : {', '.join(strong_subjects_fr) if strong_subjects_fr else 'les matières scientifiques et humaines'}. Ces performances attestent de ma capacité à suivre une formation exigeante dans ce domaine.

**⭐ Qualités personnelles**
Parmi mes principales qualités, je peux citer : {', '.join(qualities_fr)}. Ces atouts, combinés à ma rigueur et ma motivation, me permettront de m'épanouir pleinement dans mes études et de contribuer activement à la vie de l'établissement.

**🎯 Projet professionnel**
Mon intérêt pour {', '.join(preferences_fr) if preferences_fr else 'ce domaine'} ne cesse de grandir, et je souhaite mettre mon énergie au service de cette orientation. Je suis convaincu que votre établissement saura m'offrir les meilleures conditions pour développer mes compétences et concrétiser mon projet professionnel.

Je suis disponible pour un entretien afin de vous exposer plus en détail ma motivation et mon parcours.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{self.student_name}
"""
        return letter
    
    def _generate_enthusiastic_letter(self,
                                      best_domain: str,
                                      best_percentage: float,
                                      notes: Dict[str, float],
                                      preferences: List[str],
                                      qualities: List[str]) -> str:
        """Génère une lettre au style enthousiaste et dynamique"""
        
        qualities_fr = self._translate_qualities(qualities[:3])
        
        letter = f"""
{self.date}

**✨ Lettre de motivation - Formation en {best_domain}**

Bonjour,

Je suis un étudiant passionné et déterminé à réussir dans le domaine de {best_domain} ! Avec un taux de compatibilité de {best_percentage:.1f}% entre mon profil et cette filière, je suis plus que jamais convaincu que c'est la voie qui me correspond.

**Pourquoi moi ?**
- ✅ Des résultats solides dans les matières clés
- ✅ Des qualités comme {', '.join(qualities_fr)} qui font la différence
- ✅ Une motivation sans faille pour réussir

**Mon projet ?**
Intégrer une formation d'excellence en {best_domain} pour développer mes compétences et contribuer à des projets innovants.

Je serais ravi de vous rencontrer pour échanger sur ma candidature et ma passion pour ce domaine.

A très bientôt, j'espère !

{self.student_name}
"""
        return letter
    
    def _generate_concise_letter(self,
                                 best_domain: str,
                                 best_percentage: float,
                                 notes: Dict[str, float],
                                 preferences: List[str],
                                 qualities: List[str]) -> str:
        """Génère une lettre concise et directe"""
        
        qualities_fr = self._translate_qualities(qualities[:2])
        
        letter = f"""
{self.date}

**Objet : Candidature formation {best_domain}**

Madame, Monsieur,

Mon profil académique ({best_percentage:.1f}% de compatibilité) et mes qualités ({', '.join(qualities_fr)}) me destinent naturellement à la filière {best_domain}.

Je souhaite intégrer votre formation pour concrétiser mon projet professionnel dans ce domaine passionnant.

Je me tiens à votre disposition pour un entretien.

Cordialement,

{self.student_name}
"""
        return letter
    
    def _translate_subjects(self, subjects: List[str]) -> List[str]:
        """Traduit les matières en français"""
        translation = {
            "math": "Mathématiques",
            "physics": "Physique",
            "biology": "Biologie",
            "chemistry": "Chimie",
            "french": "Français",
            "philosophy": "Philosophie",
            "economics": "Économie",
            "art": "Arts",
            "english": "Anglais",
            "history": "Histoire",
            "informatics": "Informatique"
        }
        return [translation.get(s, s.capitalize()) for s in subjects]
    
    def _translate_qualities(self, qualities: List[str]) -> List[str]:
        """Traduit les qualités en français"""
        translation = {
            "analytical": "esprit analytique",
            "logical": "logique",
            "creative": "créativité",
            "empathy": "empathie",
            "rigorous": "rigueur",
            "communication": "sens de la communication",
            "leadership": "leadership",
            "patient": "patience",
            "problem-solving": "résolution de problèmes",
            "artistic": "sens artistique",
            "argumentative": "capacité d'argumentation",
            "detail-oriented": "sens du détail"
        }
        return [translation.get(q, q) for q in qualities]
    
    def _translate_preferences(self, preferences: List[str]) -> List[str]:
        """Traduit les préférences en français"""
        translation = {
            "technology": "la technologie",
            "health": "la santé",
            "art": "l'art et la création",
            "justice": "la justice",
            "business": "le monde des affaires",
            "engineering": "l'ingénierie",
            "medicine": "la médecine",
            "design": "le design",
            "law": "le droit",
            "commerce": "le commerce",
            "environment": "l'environnement"
        }
        return [translation.get(p, p) for p in preferences]
    
    def save_letter_to_file(self, letter: str, filepath: str):
        """Sauvegarde la lettre dans un fichier"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(letter)
    
    def get_letter_stats(self, letter: str) -> Dict[str, int]:
        """Retourne des statistiques sur la lettre"""
        return {
            "caracteres": len(letter),
            "mots": len(letter.split()),
            "lignes": len(letter.split('\n'))
        }


# Test du module
if __name__ == "__main__":
    generator = RecommendationLetterGenerator("Marie Dupont")
    
    # Test
    notes = {"math": 16, "physics": 15, "biology": 14}
    preferences = ["technology", "engineering"]
    qualities = ["analytical", "logical", "problem-solving"]
    
    letter = generator.generate_letter(
        best_domain="Ingénierie",
        best_percentage=78.5,
        notes=notes,
        preferences=preferences,
        qualities=qualities,
        style="professionnel"
    )
    
    print(letter)
    print(f"\n📊 Statistiques: {generator.get_letter_stats(letter)}")