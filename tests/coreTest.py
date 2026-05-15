# tests/coreTest.py
import sys
from pathlib import Path

# Ajouter le dossier parent au chemin Python
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Maintenant importer
from core_.clips_engine import CLIPSEngine

def test_core():
    print("=" * 50)
    print("🧪 Test du module CORE avec CLIPS")
    print("=" * 50)
    
    # Créer le moteur
    engine = CLIPSEngine(knowledge_path=str(parent_dir / "knowledge"))
    engine.set_debug(True)
    
    # Profil étudiant - Ingénierie (maths/physique élevées)
    print("\n📋 Profil: Étudiant en Sciences")
    notes = {
        "math": 18,
        "physics": 17,
    }
    preferences = ["technology", "engineering"]
    qualites = ["analytical", "logical"]
    
    result = engine.evaluate_student(notes, preferences, qualites)
    
    print("\n📊 RÉSULTATS:")
    for domain, percentage in result["percentages"].items():
        if percentage > 0:
            bar_length = int(percentage / 5)
            bar = "█" * bar_length
            print(f"  {domain:12} : {bar} {percentage:.1f}%")
    
    top = engine.get_top_recommendations(result["percentages"])
    if top:
        print(f"\n🏆 RECOMMANDATION: {top[0][0]} ({top[0][1]:.1f}%)")
    
    print("\n✅ Test terminé")

if __name__ == "__main__":
    test_core()