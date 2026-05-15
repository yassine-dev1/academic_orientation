# """
# Core package - Cœur métier du système expert
# Contient les modèles de données, constantes et moteur d'inférence CLIPS
# """

# from core.constants import Colors, CareerFields, Config
# from core.models import Question, CareerResult, StudentProfile
# from core.clips_engine import CLIPSEngine

# __all__ = [
#     'Colors',
#     'CareerFields', 
#     'Config',
#     'Question',
#     'CareerResult',
#     'StudentProfile',
#     'CLIPSEngine'
# ]

"""
Core package - Cœur métier du système expert
"""

from core_.clips_engine import CLIPSEngine

__all__ = ['CLIPSEngine']