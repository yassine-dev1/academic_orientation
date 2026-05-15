# tests/coreTest.py
import sys
from pathlib import Path

# Ajouter le dossier parent
sys.path.insert(0, str(Path(__file__).parent.parent))

from core_.clips_engine import CLIPSEngine

def test_core():
    print("=" * 50)
    print("🧪 Test du module CORE avec CLIPS")
    print("=" * 50)
    
    # Créer le moteur
    engine = CLIPSEngine(knowledge_path="knowledge")
    engine.set_debug(True)
    
    # Profil étudiant - Ingénierie (maths/physique élevées)
    print("\n📋 Profil 1: Étudiant en Sciences")
    notes1 = {
        "math": 18,
        "physics": 17,
        "biology": 12,
        "chemistry": 11,
    }
    preferences1 = ["technology", "engineering", "computers"]
    qualites1 = ["analytical", "logical", "problem-solving"]
    
    result1 = engine.evaluate_student(notes1, preferences1, qualites1)
    
    print("\n📊 RÉSULTATS:")
    for domain, percentage in result1["percentages"].items():
        if percentage > 0:
            bar_length = int(percentage / 5)
            bar = "█" * bar_length
            print(f"  {domain:12} : {bar} {percentage:.1f}%")
    
    top = engine.get_top_recommendations(result1["percentages"])
    if top:
        print(f"\n🏆 RECOMMANDATION: {top[0][0]} ({top[0][1]:.1f}%)")
    
    print("\n" + "=" * 50)
    print("✅ Test terminé")

if __name__ == "__main__":
    test_core()