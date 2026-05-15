"""
Vue des résultats - Version stable avec conseils IA
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from ui.styles import Colors, Fonts, Sizes
from datetime import datetime
from utils.letter_generator import AILetterGenerator
from utils.advice_generator import AdviceGenerator, format_advice_for_display


class ResultsView(ctk.CTkFrame):
    """Vue des résultats avec graphiques, lettre et conseils IA"""
    
    def __init__(self, parent, result, engine, restart_callback, student_data=None):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.result = result
        self.engine = engine
        self.restart_callback = restart_callback
        
        # Récupérer les données
        if student_data:
            self.student_data = student_data
        elif hasattr(parent, 'student_data'):
            self.student_data = parent.student_data
        else:
            self.student_data = {"notes": {}, "preferences": [], "qualities": []}
        
        self.letter_generated = False
        self.current_letter = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface"""
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ========== TITRE ==========
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="✨ Résultats de l'Évaluation",
            font=("Segoe UI", 28, "bold"),
            text_color=Colors.SUCCESS
        )
        title.pack(side="left")
        
        # Bouton retour
        restart_btn = ctk.CTkButton(
            title_frame,
            text="🔄 Nouvelle évaluation",
            font=("Segoe UI", 12, "bold"),
            height=38,
            width=160,
            corner_radius=8,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_DARK,
            command=self.restart_callback
        )
        restart_btn.pack(side="right")
        
        # ========== CRÉATION DES ONGLETS ==========
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=Colors.SURFACE,
            segmented_button_fg_color=Colors.BACKGROUND,
            segmented_button_selected_color=Colors.PRIMARY,
            segmented_button_unselected_color=Colors.SURFACE,
            text_color=Colors.TEXT
        )
        self.tabview.pack(fill="both", expand=True, pady=(10, 0))
        
        # Onglets
        self.tabview.add("📊 Résultats")
        self.tabview.add("📝 Lettre de motivation")
        self.tabview.add("💡 Conseils IA")
        
        # Remplir les onglets
        self.create_results_tab()
        self.create_letter_tab()
        self.create_advice_tab()
    
    def create_results_tab(self):
        """Crée l'onglet des résultats avec graphiques"""
        tab = self.tabview.tab("📊 Résultats")
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        # ========== GRAPHIQUE À BARRES ==========
        chart_frame = ctk.CTkFrame(scroll_frame, fg_color=Colors.SURFACE, corner_radius=12)
        chart_frame.pack(fill="x", pady=(0, 20))
        
        chart_title = ctk.CTkLabel(
            chart_frame,
            text="📊 Compatibilité par domaine",
            font=("Segoe UI", 16, "bold"),
            text_color=Colors.PRIMARY
        )
        chart_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Barres
        percentages = self.result.get("percentages", {})
        sorted_domains = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        
        colors = [Colors.PRIMARY, Colors.SECONDARY, Colors.SUCCESS, Colors.WARNING, Colors.ERROR]
        
        bars_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        bars_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for i, (domain, percentage) in enumerate(sorted_domains):
            if percentage > 0:
                row_frame = ctk.CTkFrame(bars_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)
                
                # Nom
                icons = {"Ingenierie": "🔧", "Medecine": "🏥", "Design": "🎨", "Droit": "⚖️", "Commerce": "📊"}
                icon = icons.get(domain, "📌")
                
                name_label = ctk.CTkLabel(
                    row_frame, 
                    text=f"{icon} {domain}", 
                    font=("Segoe UI", 12, "bold"),
                    width=100,
                    anchor="w"
                )
                name_label.pack(side="left", padx=(0, 10))
                
                # Barre
                bar_container = ctk.CTkFrame(row_frame, fg_color=Colors.BACKGROUND, corner_radius=6, height=28)
                bar_container.pack(side="left", fill="x", expand=True)
                
                bar_width = percentage * 3.5
                bar = ctk.CTkFrame(
                    bar_container,
                    fg_color=colors[i % len(colors)],
                    corner_radius=6,
                    height=28,
                    width=bar_width
                )
                bar.pack(side="left", fill="y")
                
                # Pourcentage
                pct_label = ctk.CTkLabel(
                    row_frame,
                    text=f"{percentage:.1f}%",
                    font=("Segoe UI", 12, "bold"),
                    width=60,
                    anchor="e"
                )
                pct_label.pack(side="right", padx=(10, 0))
        
        # ========== MEILLEURE ORIENTATION ==========
        best_domain = max(percentages.items(), key=lambda x: x[1])
        
        best_frame = ctk.CTkFrame(scroll_frame, fg_color=Colors.SUCCESS, corner_radius=12)
        best_frame.pack(fill="x", pady=(0, 20))
        
        best_text = f"🏆 Votre meilleure orientation : {best_domain[0]} avec {best_domain[1]:.1f}% de compatibilité"
        best_label = ctk.CTkLabel(
            best_frame,
            text=best_text,
            font=("Segoe UI", 16, "bold"),
            text_color=Colors.BACKGROUND,
            padx=15,
            pady=15
        )
        best_label.pack()
        
        # ========== CARTES DÉTAILLÉES ==========
        details_title = ctk.CTkLabel(
            scroll_frame,
            text="📋 Analyse détaillée",
            font=("Segoe UI", 16, "bold"),
            text_color=Colors.PRIMARY
        )
        details_title.pack(anchor="w", pady=(0, 10))
        
        for domain, percentage in sorted_domains[:3]:
            if percentage > 0:
                self.create_detail_card(scroll_frame, domain, percentage)
        
        # ========== RÉSUMÉ ==========
        self.create_summary(scroll_frame)
    
    def create_detail_card(self, parent, domain, percentage):
        """Crée une carte de détail"""
        card = ctk.CTkFrame(parent, fg_color=Colors.SURFACE, corner_radius=10)
        card.pack(fill="x", pady=5)
        
        # Niveau
        if percentage >= 70:
            level = "Excellent"
            level_color = Colors.SUCCESS
        elif percentage >= 50:
            level = "Bon"
            level_color = Colors.PRIMARY
        elif percentage >= 30:
            level = "Moyen"
            level_color = Colors.WARNING
        else:
            level = "À explorer"
            level_color = Colors.ERROR
        
        # En-tête
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))
        
        icons = {"Ingenierie": "🔧", "Medecine": "🏥", "Design": "🎨", "Droit": "⚖️", "Commerce": "📊"}
        icon = icons.get(domain, "📌")
        
        domain_label = ctk.CTkLabel(
            header, 
            text=f"{icon} {domain}", 
            font=("Segoe UI", 14, "bold"),
            text_color=Colors.PRIMARY
        )
        domain_label.pack(side="left")
        
        level_label = ctk.CTkLabel(
            header, 
            text=level, 
            font=("Segoe UI", 11, "bold"),
            text_color=level_color
        )
        level_label.pack(side="right")
        
        # Description
        descriptions = {
            "Ingenierie": "Conception et résolution de problèmes techniques. Métiers d'avenir dans la tech.",
            "Medecine": "Soins et santé des patients. Une carrière humaine et exigeante.",
            "Design": "Création de solutions esthétiques et fonctionnelles.",
            "Droit": "Application et interprétation des lois. Défendez les droits.",
            "Commerce": "Gestion, stratégie et développement d'activités commerciales."
        }
        desc = descriptions.get(domain, "Explorez ce domaine passionnant !")
        
        desc_label = ctk.CTkLabel(
            card,
            text=desc,
            font=("Segoe UI", 11),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=600,
            justify="left"
        )
        desc_label.pack(anchor="w", padx=15, pady=(0, 10))
    
    def create_summary(self, parent):
        """Crée un résumé des points forts"""
        percentages = self.result.get("percentages", {})
        if not percentages:
            return
            
        best_domain = max(percentages.items(), key=lambda x: x[1])
        
        summary_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.BACKGROUND,
            corner_radius=12
        )
        summary_frame.pack(fill="x", pady=20)
        
        notes = self.student_data.get("notes", {})
        strong_subjects = [s for s, v in notes.items() if v >= 14]
        subjects_fr = {
            "math": "Mathématiques", "physics": "Physique", "biology": "Biologie",
            "chemistry": "Chimie", "french": "Français", "philosophy": "Philosophie",
            "economics": "Économie", "art": "Arts"
        }
        strong_names = [subjects_fr.get(s, s) for s in strong_subjects]
        
        qualities = self.student_data.get("qualities", [])
        
        summary_text = f"""
📌 **RÉSUMÉ DE VOTRE PROFIL**

🎯 Meilleure orientation : {best_domain[0]} ({best_domain[1]:.1f}%)

📚 Points forts académiques : {', '.join(strong_names) if strong_names else 'Matières variées'}

⭐ Qualités identifiées : {', '.join(qualities[:3]) if qualities else 'Motivation et sérieux'}

🔍 Analyse : Votre profil montre une bonne compatibilité avec le domaine {best_domain[0]}.
"""
        
        summary_label = ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=("Segoe UI", 12),
            text_color=Colors.TEXT_SECONDARY,
            justify="left",
            wraplength=700
        )
        summary_label.pack(padx=15, pady=15)
    
    def create_letter_tab(self):
        """Crée l'onglet de la lettre de motivation"""
        tab = self.tabview.tab("📝 Lettre de motivation")
        
        # Frame principal
        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Bouton générer
        generate_btn = ctk.CTkButton(
            main_frame,
            text="✍️ Générer une lettre personnalisée",
            font=("Segoe UI", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color=Colors.PRIMARY,
            command=self.generate_letter
        )
        generate_btn.pack(pady=10)
        
        # Zone de texte
        self.letter_text = ctk.CTkTextbox(
            main_frame,
            font=("Segoe UI", 11),
            wrap="word",
            fg_color=Colors.BACKGROUND,
            text_color=Colors.TEXT
        )
        self.letter_text.pack(fill="both", expand=True, pady=10)
        self.letter_text.insert("1.0", "Cliquez sur 'Générer' pour créer votre lettre de motivation...")
        self.letter_text.configure(state="disabled")
        
        # Boutons copier/sauvegarder
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=5)
        
        copy_btn = ctk.CTkButton(
            btn_frame,
            text="📋 Copier",
            font=("Segoe UI", 11),
            height=32,
            width=100,
            corner_radius=8,
            fg_color=Colors.SURFACE,
            hover_color=Colors.BORDER,
            command=self.copy_letter
        )
        copy_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Sauvegarder",
            font=("Segoe UI", 11),
            height=32,
            width=100,
            corner_radius=8,
            fg_color=Colors.SURFACE,
            hover_color=Colors.BORDER,
            command=self.save_letter
        )
        save_btn.pack(side="left", padx=5)
    
    def generate_letter(self):
        """Génère une lettre de motivation unique avec l'IA"""
        
        # Fenêtre de choix du style
        style_window = ctk.CTkToplevel(self)
        style_window.title("Style de lettre")
        style_window.geometry("400x300")
        style_window.transient(self)
        style_window.grab_set()
        
        ctk.CTkLabel(
            style_window,
            text="Choisissez le style de votre lettre :",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)
        
        style_var = ctk.StringVar(value="professionnel")
        
        styles_frame = ctk.CTkFrame(style_window, fg_color="transparent")
        styles_frame.pack(pady=10)
        
        styles = [
            ("📝 Professionnel et formel", "professionnel"),
            ("🎨 Créatif et original", "creatif"),
            ("⚡ Concis et percutant", "concis")
        ]
        
        for text, value in styles:
            ctk.CTkRadioButton(
                styles_frame,
                text=text,
                variable=style_var,
                value=value,
                font=("Segoe UI", 12)
            ).pack(anchor="w", pady=5)
        
        def generate():
            style = style_var.get()
            style_window.destroy()
            
            # Afficher un chargement
            self.letter_text.configure(state="normal")
            self.letter_text.delete("1.0", "end")
            self.letter_text.insert("1.0", "🤖 Génération de votre lettre personnalisée...\n\nVeuillez patienter quelques secondes.")
            self.letter_text.configure(state="disabled")
            
            try:
                generator = AILetterGenerator()
                
                percentages = self.result.get("percentages", {})
                best_domain = max(percentages.items(), key=lambda x: x[1])
                
                letter = generator.generate_letter(
                    best_domain=best_domain[0],
                    best_percentage=best_domain[1],
                    notes=self.student_data.get("notes", {}),
                    preferences=self.student_data.get("preferences", []),
                    qualities=self.student_data.get("qualities", []),
                    style=style
                )
                
                self.current_letter = letter
                self.letter_generated = True
                
                self.letter_text.configure(state="normal")
                self.letter_text.delete("1.0", "end")
                self.letter_text.insert("1.0", letter)
                self.letter_text.configure(state="disabled")
                
                messagebox.showinfo("Succès", "Lettre générée avec succès !")
            except Exception as e:
                self.letter_text.configure(state="normal")
                self.letter_text.delete("1.0", "end")
                self.letter_text.insert("1.0", f"Erreur : {str(e)}")
                self.letter_text.configure(state="disabled")
                messagebox.showerror("Erreur", str(e))
        
        ctk.CTkButton(
            style_window,
            text="Générer ma lettre",
            font=("Segoe UI", 13, "bold"),
            height=40,
            corner_radius=8,
            fg_color=Colors.SUCCESS,
            command=generate
        ).pack(pady=20)
    
    def copy_letter(self):
        if self.letter_generated:
            self.clipboard_clear()
            self.clipboard_append(self.current_letter)
            messagebox.showinfo("Succès", "Lettre copiée dans le presse-papier !")
        else:
            messagebox.showwarning("Attention", "Générez d'abord une lettre.")
    
    def save_letter(self):
        if not self.letter_generated:
            messagebox.showwarning("Attention", "Générez d'abord la lettre.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
            initialfile="lettre_motivation.txt"
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.current_letter)
            messagebox.showinfo("Succès", f"Lettre sauvegardée : {file_path}")
    
    def create_advice_tab(self):
        """Crée l'onglet des conseils personnalisés avec IA"""
        tab = self.tabview.tab("💡 Conseils IA")
        
        # Frame pour le contenu
        content_frame = ctk.CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Bouton générer
        generate_btn = ctk.CTkButton(
            content_frame,
            text="🤖 Générer des conseils personnalisés avec IA",
            font=("Segoe UI", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color=Colors.PRIMARY,
            command=self.generate_advice
        )
        generate_btn.pack(pady=10)
        
        # Zone de texte pour les conseils
        self.advice_text = ctk.CTkTextbox(
            content_frame,
            font=("Segoe UI", 12),
            wrap="word",
            fg_color=Colors.BACKGROUND,
            text_color=Colors.TEXT
        )
        self.advice_text.pack(fill="both", expand=True, pady=10)
        self.advice_text.insert("1.0", "Cliquez sur 'Générer' pour obtenir des conseils personnalisés par IA...")
        self.advice_text.configure(state="disabled")
    
    def generate_advice(self):
        """Génère et affiche les conseils"""
        self.advice_text.configure(state="normal")
        self.advice_text.delete("1.0", "end")
        self.advice_text.insert("1.0", "🤖 Génération de conseils personnalisés...\n\nVeuillez patienter quelques secondes.")
        self.advice_text.configure(state="disabled")
        
        # Récupérer les données
        percentages = self.result.get("percentages", {})
        best_domain = max(percentages.items(), key=lambda x: x[1])
        
        # Générer les conseils
        generator = AdviceGenerator()
        advice_dict = generator.generate_advice(
            best_domain=best_domain[0],
            best_percentage=best_domain[1],
            all_scores=self.result.get("scores", {}),
            notes=self.student_data.get("notes", {}),
            preferences=self.student_data.get("preferences", []),
            qualities=self.student_data.get("qualities", [])
        )
        
        # Afficher
        advice_text = format_advice_for_display(advice_dict)
        
        self.advice_text.configure(state="normal")
        self.advice_text.delete("1.0", "end")
        self.advice_text.insert("1.0", advice_text)
        self.advice_text.configure(state="disabled")
        messagebox.showinfo("Succès", "Conseils générés avec succès !")