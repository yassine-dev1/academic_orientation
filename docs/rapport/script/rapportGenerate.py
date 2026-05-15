from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import base64
from io import BytesIO

def create_report():
    doc = Document()

    # Style titre
    title_style = doc.styles.add_style('MyTitle', WD_STYLE_TYPE.PARAGRAPH)
    title_style.font.size = Pt(24)
    title_style.font.bold = True
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Page de garde
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("République du Maroc\nMinistère de l'Éducation Nationale\nUniversité … – Faculté …")
    run.font.size = Pt(12)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Système Expert d'Orientation Académique\nIntégration des modèles RIASEC et valeurs professionnelles")
    run.font.size = Pt(20)
    run.bold = True
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Encadré par : Mohamed RAMDANI\nRéalisé par : EL JARJINI Yassine")
    run.font.size = Pt(12)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Année universitaire : 2025/2026")
    doc.add_page_break()

    # 2. Présentation
    doc.add_heading("1. Introduction et objectif", level=1)
    doc.add_paragraph("Le présent projet consiste en la conception et la réalisation d’un système expert d’aide à l’orientation académique. L’objectif principal est d’assister un élève de lycée dans le choix d’un domaine d’études supérieures en se basant non seulement sur ses notes scolaires, mais aussi sur ses préférences déclarées, ses qualités personnelles, ses intérêts profonds (modèle RIASEC) et ses valeurs professionnelles. Le système calcule un score par domaine (Ingénierie, Médecine, Design, Droit, Commerce), puis convertit ces scores en pourcentages de compatibilité. L’élève reçoit une recommandation personnalisée ainsi qu’un graphique de synthèse.")

    doc.add_heading("2. Workflow du moteur d’inférence – Chaînage avant", level=1)
    doc.add_paragraph("Le moteur utilise un chaînage avant (forward chaining) : à partir des faits initiaux (notes, préférences, qualités, RIASEC, valeurs), il applique des règles pour construire progressivement les scores.")
    steps = [
        "Saisie des données (notes, préférences, qualités, RIASEC 1-10, valeurs 1-10)",
        "Agrégation dans StudentFact",
        "Application des règles : académiques (5 domaines), RIASEC, valeurs",
        "Calcul des scores bruts via ScoreCalculator",
        "Conversion en pourcentages (normalisation)",
        "Affichage des résultats : pourcentages, graphique, recommandation, lettre d’orientation"
    ]
    for s in steps:
        doc.add_paragraph(s, style='List Bullet')
    doc.add_paragraph("Le chaînage avant part des faits et déclenche toutes les règles dont les conditions sont satisfaites, accumulant les scores jusqu’à obtenir une conclusion (les pourcentages). Aucune hypothèse de départ n’est posée.")

    # 3. RIASEC
    doc.add_heading("3. Modèle RIASEC (Holland)", level=1)
    doc.add_paragraph("Développé par John Holland, ce modèle classe les personnalités professionnelles en 6 types : Réaliste (R), Investigateur (I), Artistique (A), Social (S), Entreprenant (E), Conventionnel (C).")
    doc.add_heading("Pourquoi l’ajouter ?", level=2)
    doc.add_paragraph("- Les notes seules ne suffisent pas : un élève peut avoir de bonnes notes mais détester le travail en laboratoire.\n- Le RIASEC affine la compatibilité entre la personnalité et la culture du domaine.\n- Dans notre système, l’élève note chaque dimension de 1 à 10 ; une matrice de correspondance applique bonus/malus (score >5 bonus, <3 malus) avec normalisation.")

    # 4. Valeurs
    doc.add_heading("4. Valeurs professionnelles", level=1)
    doc.add_paragraph("Les valeurs professionnelles sont les motivations profondes qui guident une personne dans sa carrière (Super, Schein). 6 valeurs retenues : Stabilité, Créativité, Impact social, Prestige, Autonomie, Leadership.")
    doc.add_heading("Pourquoi les ajouter ?", level=2)
    doc.add_paragraph("- Un métier peut être académiquement accessible mais psychologiquement insatisfaisant si les valeurs ne sont pas alignées.\n- Exemple : un élève très créatif sera malheureux en comptabilité.\n- Le système applique bonus/malus avec la même logique que RIASEC.")

    # 5. Diagramme de classes
    doc.add_heading("5. Diagramme de classes", level=1)
    doc.add_paragraph("Ci-dessous l’architecture orientée objet du système.")
    # Insérer l'image DiagClassSysExpert.png (à placer dans le même dossier)
    try:
        doc.add_picture("C:/Users/dell/Desktop/Projects_ILISI2/SystemeExpert_Python/orientation_expert/docs/diagrammes/DiagClassSysExpert.png", width=Inches(6))
    except:
        doc.add_paragraph("[Image : DiagClassSysExpert.png à insérer manuellement]")
    doc.add_paragraph("Description : MainWindow (interface), ExpertEngine (cœur), StudentFactBase (données), RulesBase (règles académiques, RIASEC, valeurs), ScoreCalculator (scores et pourcentages), BonusCalculator (bonus préférences), ResultsView (affichage, lettre). Relations : ExpertEngine utilise RulesBase, ScoreCalculator, BonusCalculator, StudentFactBase.")

    # 6. Diagramme de communication
    doc.add_heading("6. Diagramme de communication (flux des données)", level=1)
    try:
        doc.add_picture("C:/Users/dell/Desktop/Projects_ILISI2/SystemeExpert_Python/orientation_expert/docs/diagrammes/Communication2.png", width=Inches(6))
    except:
        doc.add_paragraph("[Image : Communication.png à insérer manuellement]")
    doc.add_paragraph("Flux : Entrées (Notes, Préférences, Qualités, RIASEC, Valeurs) → Agrégation StudentFact → Règles (académiques + RIASEC/valeurs) + BonusCalculator (préférences) → ScoreCalculator total → Conversion % → Sorties (pourcentages, graphique, recommandation, lettre). Le flux est séquentiel, correspondant à un chaînage avant pur.")

    # Sauvegarde
    doc.save("Rapport_Orientation.docx")
    print("Fichier 'Rapport_Orientation.docx' généré avec succès.")

if __name__ == "__main__":
    create_report()