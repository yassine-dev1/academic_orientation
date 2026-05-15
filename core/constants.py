"""
Constantes et configuration du système
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Colors:
    """Thème de couleurs moderne et sombre"""
    PRIMARY = "#6C63FF"      # Violet moderne
    SECONDARY = "#FF6584"     # Rose
    SUCCESS = "#00D26A"       # Vert
    WARNING = "#FFB86C"       # Orange
    ERROR = "#FF5555"         # Rouge
    BACKGROUND = "#1E1E2E"    # Gris foncé
    SURFACE = "#2D2D3D"       # Surface
    TEXT = "#F8F8F2"          # Texte clair
    TEXT_SECONDARY = "#A9A9B8" # Texte secondaire
    BORDER = "#44445A"        # Bordure


@dataclass(frozen=True)
class CareerFields:
    """Domaines de carrière disponibles"""
    ENGINEERING = "Ingénierie"
    MEDICINE = "Médecine"
    DESIGN = "Design"
    LAW = "Droit"
    BUSINESS = "Commerce"
    
    ALL = [ENGINEERING, MEDICINE, DESIGN, LAW, BUSINESS]
    
    # Mapping des noms anglais vers français
    ENGLISH_NAMES = {
        ENGINEERING: "Engineering",
        MEDICINE: "Medicine", 
        DESIGN: "Design",
        LAW: "Law",
        BUSINESS: "Business"
    }


@dataclass(frozen=True)
class Config:
    """Configuration générale"""
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    ANIMATION_DURATION = 300
    AI_MODEL = "gemini-2.0-flash-exp"
    
    # Seuils pour les recommandations
    THRESHOLD_EXCELLENT = 75.0
    THRESHOLD_GOOD = 60.0
    THRESHOLD_AVERAGE = 45.0


@dataclass(frozen=True)
class SubjectMapping:
    """Mapping des matières scolaires"""
    SUBJECTS = {
        "math": "Mathématiques",
        "physics": "Physique",
        "biology": "Biologie",
        "chemistry": "Chimie",
        "informatics": "Informatique",
        "french": "Français",
        "philosophy": "Philosophie",
        "history": "Histoire",
        "economics": "Économie",
        "english": "Anglais",
        "art": "Arts"
    }
    
    @classmethod
    def get_french_name(cls, english_name: str) -> str:
        return cls.SUBJECTS.get(english_name, english_name)