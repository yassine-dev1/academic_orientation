"""
Test direct sans interface
"""

import sys
sys.path.insert(0, '.')

from core_.expert_engine import ExpertEngine

# Créer le moteur
engine = ExpertEngine()
engine.set_debug(True)

# Données de test
notes = {
    "math": 16,
    "physics": 15,
    "biology": 14,
    "chemistry": 13
}

preferences = ["technology", "engineering"]
qualities = ["analytical", "logical"]

# Évaluation
result = engine.evaluate_student(notes, preferences, qualities)

print("\n" + "="*40)
print("RÉSULTATS:")
print("="*40)
for domain, pct in result["percentages"].items():
    if pct > 0:
        print(f"  {domain}: {pct:.1f}%")