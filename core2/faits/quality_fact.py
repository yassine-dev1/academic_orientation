"""
Classe représentant un fait de type "qualité"
"""

from dataclasses import dataclass


@dataclass
class QualityFact:
    """
    Fait représentant une qualité personnelle
    """
    name: str
    level: int = 3  # Niveau de 1 à 5
    
    def matches(self, *qualities: str) -> bool:
        """Vérifie si la qualité correspond à l'une des qualités données"""
        return self.name.lower() in [q.lower() for q in qualities]
    
    def __str__(self) -> str:
        return f"Quality(name={self.name}, level={self.level})"