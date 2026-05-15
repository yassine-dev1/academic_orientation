"""
Classe représentant un fait de type "note"
"""

from dataclasses import dataclass


@dataclass
class GradeFact:
    """
    Fait représentant une note dans une matière
    """
    subject: str
    value: float
    
    def is_excellent(self, threshold: float = 16) -> bool:
        """Vérifie si la note est excellente"""
        return self.value >= threshold
    
    def is_good(self, threshold: float = 14) -> bool:
        """Vérifie si la note est bonne"""
        return self.value >= threshold
    
    def is_average(self, threshold: float = 12) -> bool:
        """Vérifie si la note est moyenne"""
        return self.value >= threshold
    
    def __str__(self) -> str:
        return f"Grade(subject={self.subject}, value={self.value})"