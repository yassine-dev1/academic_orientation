"""
Classe représentant l'ensemble des faits concernant un étudiant
"""

from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class StudentFact:
    """
    Base de faits de l'étudiant
    Contient toutes les informations brutes sur l'étudiant
    """
    notes: Dict[str, float] = field(default_factory=dict)
    preferences: List[str] = field(default_factory=list)
    qualites: List[str] = field(default_factory=list)
    riasec: Dict[str, int] = field(default_factory=dict)
    valeurs: Dict[str, int] = field(default_factory=dict)
    
    def add_note(self, matiere: str, valeur: float) -> None:
        """Ajoute ou met à jour une note"""
        self.notes[matiere.lower()] = valeur
    
    def add_preference(self, preference: str) -> None:
        """Ajoute une préférence"""
        if preference.lower() not in self.preferences:
            self.preferences.append(preference.lower())
    
    def add_qualite(self, qualite: str) -> None:
        """Ajoute une qualité"""
        if qualite.lower() not in self.qualites:
            self.qualites.append(qualite.lower())
    
    def get_note(self, matiere: str) -> float:
        """Récupère une note, retourne 0 si non trouvée"""
        return self.notes.get(matiere.lower(), 0)
    
    def set_riasec(self, trait: str, value: int) -> None:
        """Définit un score RIASEC (R, I, A, S, E, C) entre 1 et 10"""
        self.riasec[trait.lower()] = max(1, min(10, value))
    
    def get_riasec(self, trait: str) -> int:
        """Récupère un score RIASEC, retourne 5 par défaut"""
        return self.riasec.get(trait.lower(), 5)
    
    def set_valeur(self, valeur_name: str, value: int) -> None:
        """Définit un score de valeur professionnelle entre 1 et 10"""
        self.valeurs[valeur_name.lower()] = max(1, min(10, value))
    
    def get_valeur(self, valeur_name: str) -> int:
        """Récupère un score de valeur professionnelle, retourne 5 par défaut"""
        return self.valeurs.get(valeur_name.lower(), 5)
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire pour le débogage"""
        return {
            "notes": self.notes,
            "preferences": self.preferences,
            "qualites": self.qualites,
            "riasec": self.riasec,
            "valeurs": self.valeurs
        }