"""
Modèles de données pour le système expert
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class QuestionType(Enum):
    """Types de questions"""
    PERSONALITY = "personality"
    ACADEMIC = "academic"
    CAREER = "career"
    CONDITIONAL = "conditional"


@dataclass
class Question:
    """Modèle de question"""
    id: int
    text: str
    options: List[str]
    points: Dict[str, Dict[str, int]]
    question_type: QuestionType = QuestionType.PERSONALITY
    condition: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire"""
        return {
            "id": self.id,
            "text": self.text,
            "options": self.options,
            "points": self.points,
            "type": self.question_type.value,
            "condition": self.condition
        }


@dataclass
class CareerResult:
    """Résultat d'orientation pour un domaine"""
    name: str
    score: float
    percentage: float
    description: str
    required_skills: List[str]
    job_examples: List[str]
    
    def get_grade(self) -> str:
        """Retourne la mention selon le pourcentage"""
        if self.percentage >= 75:
            return "Excellent"
        elif self.percentage >= 60:
            return "Très bon"
        elif self.percentage >= 45:
            return "Bon"
        elif self.percentage >= 30:
            return "Moyen"
        else:
            return "À explorer"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire"""
        return {
            "name": self.name,
            "score": self.score,
            "percentage": self.percentage,
            "grade": self.get_grade(),
            "description": self.description,
            "skills": self.required_skills,
            "jobs": self.job_examples
        }


@dataclass
class StudentProfile:
    """Profil de l'étudiant"""
    domain: Optional[int] = None
    answers: List[int] = field(default_factory=list)
    scores: Dict[str, int] = field(default_factory=dict)
    notes: Dict[str, float] = field(default_factory=dict)
    preferences: List[str] = field(default_factory=list)
    qualities: List[str] = field(default_factory=list)
    
    def add_note(self, subject: str, value: float):
        """Ajoute une note"""
        self.notes[subject.lower()] = value
    
    def add_preference(self, preference: str):
        """Ajoute une préférence"""
        self.preferences.append(preference.lower())
    
    def add_quality(self, quality: str):
        """Ajoute une qualité"""
        self.qualities.append(quality.lower())
    
    def reset(self):
        """Réinitialise le profil"""
        self.domain = None
        self.answers = []
        self.scores = {}
        self.notes = {}
        self.preferences = []
        self.qualities = []
    
    def to_clips_facts(self) -> List[str]:
        """Convertit le profil en faits CLIPS"""
        facts = []
        
        # Notes
        for subject, value in self.notes.items():
            facts.append(f'(grade (subject {subject}) (value {value}))')
        
        # Préférences
        for pref in self.preferences:
            facts.append(f'(preference (category "interest") (value "{pref}"))')
        
        # Qualités
        for quality in self.qualities:
            facts.append(f'(quality (name {quality}) (level 3))')
        
        return facts


@dataclass
class EvaluationResult:
    """Résultat complet de l'évaluation"""
    student: StudentProfile
    scores: Dict[str, float]
    percentages: Dict[str, float]
    recommendations: List[CareerResult]
    explanation: str = ""
    
    def get_best_match(self) -> Optional[CareerResult]:
        """Retourne la meilleure recommandation"""
        if self.recommendations:
            return self.recommendations[0]
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire"""
        return {
            "student": {
                "notes": self.student.notes,
                "preferences": self.student.preferences,
                "qualities": self.student.qualities
            },
            "scores": self.scores,
            "percentages": self.percentages,
            "recommendations": [r.to_dict() for r in self.recommendations],
            "explanation": self.explanation
        }