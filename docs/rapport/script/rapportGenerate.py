from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

def create_report():
    doc = Document()

    # Style titre
    title_style = doc.styles.add_style('MyTitle', WD_STYLE_TYPE.PARAGRAPH)
    title_style.font.size = Pt(24)
    title_style.font.bold = True
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ========== PAGE DE GARDE ==========
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

    # ========== 1. INTRODUCTION ==========
    doc.add_heading("1. Introduction et objectif", level=1)
    doc.add_paragraph("Le présent projet consiste en la conception et la réalisation d’un système expert d’aide à l’orientation académique. L’objectif principal est d’assister un élève de lycée dans le choix d’un domaine d’études supérieures en se basant non seulement sur ses notes scolaires, mais aussi sur ses préférences déclarées, ses qualités personnelles, ses intérêts profonds (modèle RIASEC) et ses valeurs professionnelles. Le système calcule un score par domaine (Ingénierie, Médecine, Design, Droit, Commerce), puis convertit ces scores en pourcentages de compatibilité. L’élève reçoit une recommandation personnalisée ainsi qu’un graphique de synthèse.")

    # ========== DIAGRAMME DE COMMUNICATION (avant workflow) ==========
    doc.add_heading("2. Diagramme de communication (flux des données)", level=1)
    try:
        doc.add_picture("C:/Users/dell/Desktop/Projects_ILISI2/SystemeExpert_Python/orientation_expert/docs/diagrammes/Communication2.png", width=Inches(6))
    except:
        doc.add_paragraph("[Image : Communication2.png à insérer manuellement]")
    doc.add_paragraph("Ce diagramme illustre la circulation des informations entre les composants : les entrées (Notes, Préférences, Qualités, RIASEC, Valeurs) sont agrégées dans StudentFact, puis traitées par les règles et le calculateur de bonus, avant d'être converties en pourcentages et d'alimenter les sorties (graphique, recommandation, lettre).")

    # ========== WORKFLOW ET CHAÎNAGE AVANT ==========
    doc.add_heading("3. Workflow du moteur d’inférence – Chaînage avant", level=1)
    doc.add_paragraph("Le moteur utilise un chaînage avant (forward chaining) : à partir des faits initiaux, il applique des règles pour construire progressivement les scores.")
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

    # ========== DÉTAIL DES RÈGLES ==========
    doc.add_heading("4. Détail des règles d’évaluation", level=1)
    
    # Règles académiques
    doc.add_heading("4.1 Règles académiques", level=2)
    doc.add_paragraph("Chaque domaine possède une règle spécifique basée sur les notes et certaines qualités :")
    rules_desc = [
        ("Ingénierie", "maths ≥14 ET physique ≥14 (excellent) ou ≥12 (moyen) ; bonus pour qualités analytiques, logiques, résolution de problèmes."),
        ("Médecine", "biologie ≥15 ET chimie ≥14 (excellent) ou ≥13/12 (moyen) ; bonus pour empathie, patience, rigueur."),
        ("Design", "arts ≥14 (excellent) ou ≥11 (moyen) ; bonus pour créativité, sens artistique, imagination."),
        ("Droit", "français ≥14 ET philosophie ≥13 (excellent) ou ≥12/11 (moyen) ; bonus pour argumentation, rigueur, analyse."),
        ("Commerce", "économie ≥14 (excellent) ou ≥11 (moyen) ; bonus pour leadership, communication, négociation.")
    ]
    for domaine, desc in rules_desc:
        doc.add_paragraph(f"• {domaine} : {desc}", style='List Bullet')
    
    # Règles RIASEC
    doc.add_heading("4.2 Règles RIASEC", level=2)
    doc.add_paragraph("L'étudiant note chaque type RIASEC de 1 à 10. Une matrice de correspondance attribue des coefficients aux domaines. Le moteur applique :")
    doc.add_paragraph("- Si score > 5 : bonus = (score-5) × coeff × 0.5 (normalisation)", style='List Bullet')
    doc.add_paragraph("- Si score < 3 : malus = (3-score) × coeff × 0.5 × 0.7 (pénalité renforcée)", style='List Bullet')
    doc.add_paragraph("- Un plafond de 15 points par domaine évite une surpondération.", style='List Bullet')
    
    # Règles Valeurs
    doc.add_heading("4.3 Règles Valeurs professionnelles", level=2)
    doc.add_paragraph("Même logique que RIASEC avec 6 valeurs : Stabilité, Créativité, Impact social, Prestige, Autonomie, Leadership. Une matrice de correspondance lie chaque valeur aux domaines.")

    # ========== MODÈLE RIASEC ==========
    doc.add_heading("5. Modèle RIASEC (Holland)", level=1)
    doc.add_paragraph("Développé par John Holland, ce modèle classe les personnalités professionnelles en 6 types : Réaliste (R), Investigateur (I), Artistique (A), Social (S), Entreprenant (E), Conventionnel (C).")
    doc.add_heading("Pourquoi l’ajouter ?", level=2)
    doc.add_paragraph("- Les notes seules ne suffisent pas : un élève peut avoir de bonnes notes mais détester le travail en laboratoire.\n- Le RIASEC affine la compatibilité entre la personnalité et la culture du domaine.\n- Dans notre système, une matrice de correspondance applique bonus/malus avec normalisation.")

    # ========== VALEURS PROFESSIONNELLES ==========
    doc.add_heading("6. Valeurs professionnelles", level=1)
    doc.add_paragraph("Les valeurs professionnelles sont les motivations profondes qui guident une personne dans sa carrière (Super, Schein). 6 valeurs retenues : Stabilité, Créativité, Impact social, Prestige, Autonomie, Leadership.")
    doc.add_heading("Pourquoi les ajouter ?", level=2)
    doc.add_paragraph("- Un métier peut être académiquement accessible mais psychologiquement insatisfaisant si les valeurs ne sont pas alignées.\n- Exemple : un élève très créatif sera malheureux en comptabilité.\n- Le système applique bonus/malus avec la même logique que RIASEC.")

    # ========== DIAGRAMME DE CLASSES ==========
    doc.add_heading("7. Diagramme de classes", level=1)
    try:
        doc.add_picture("C:/Users/dell/Desktop/Projects_ILISI2/SystemeExpert_Python/orientation_expert/docs/diagrammes/DiagClassSysExpert.png", width=Inches(6))
    except:
        doc.add_paragraph("[Image : DiagClassSysExpert.png à insérer manuellement]")
    doc.add_paragraph("Description : MainWindow (interface), ExpertEngine (cœur), StudentFactBase (données), RulesBase (règles académiques, RIASEC, valeurs), ScoreCalculator (scores et pourcentages), BonusCalculator (bonus préférences), ResultsView (affichage, lettre). Relations : ExpertEngine utilise RulesBase, ScoreCalculator, BonusCalculator, StudentFactBase.")

    # ========== GÉNÉRATION DE LETTRE PAR LLM (GEMINI) ==========
    doc.add_heading("8. Génération automatique de lettre de motivation et conseils", level=1)
    doc.add_paragraph("Le système intègre une API Google Gemini (modèle génératif) pour produire une lettre de motivation personnalisée ainsi que des conseils d'orientation. Après l'évaluation, le LLM reçoit :")
    doc.add_paragraph("- Le meilleur domaine et son pourcentage de compatibilité.", style='List Bullet')
    doc.add_paragraph("- Les notes, préférences, qualités, scores RIASEC et valeurs de l'étudiant.", style='List Bullet')
    doc.add_paragraph("- Un style d'écriture choisi (ex: formel, motivant, court).", style='List Bullet')
    doc.add_paragraph("La lettre générée est présentée dans l'interface et peut être copiée ou sauvegardée. Cela permet d'obtenir un retour à la fois technique et humain, renforçant l'aspect personnalisé du conseil d'orientation.")

    # ========== CONCLUSION ==========
    doc.add_heading("9. Conclusion", level=1)
    doc.add_paragraph("L'intégration des modèles RIASEC et des valeurs professionnelles améliore significativement la précision et la pertinence des recommandations. Le système ne se limite plus aux performances scolaires ; il prend en compte la personnalité et les motivations profondes de l’élève. L’architecture orientée objet, couplée à un moteur à chaînage avant, rend le code modulaire, maintenable et extensible à d’autres domaines d’orientation. L'utilisation d'un LLM (Gemini) pour générer une lettre de motivation apporte une valeur ajoutée qualitative, transformant le résultat chiffré en un conseil personnalisé et engageant. Ce travail constitue une base solide pour un outil d'aide à l'orientation réellement adapté aux besoins des élèves.")

    # Sauvegarde
    doc.save("Rapport_Orientation.docx")
    print("Fichier 'Rapport_Orientation.docx' généré avec succès.")

if __name__ == "__main__":
    create_report()