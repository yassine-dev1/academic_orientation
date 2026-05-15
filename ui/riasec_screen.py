"""
Écran de profil RIASEC (Holland)
Étape 4a/5 de l'évaluation
"""

import customtkinter as ctk
from ui.styles import Colors, Fonts, Sizes


class RiasecScreen(ctk.CTkFrame):
    """Écran d'évaluation RIASEC (Holland) - Types d'intérêts professionnels"""
    
    def __init__(self, parent, student_data, next_callback, back_callback):
        super().__init__(parent, fg_color="transparent")
        self.student_data = student_data
        self.next_callback = next_callback
        self.back_callback = back_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(30, 0))
        
        title = ctk.CTkLabel(
            header_frame,
            text="🎯 Étape 4a : Profil RIASEC",
            font=Fonts.TITLE,
            text_color=Colors.TEXT
        )
        title.pack(side="left")
        
        progress_label = ctk.CTkLabel(
            header_frame,
            text="4/5",
            font=Fonts.BODY_BOLD,
            text_color=Colors.PRIMARY
        )
        progress_label.pack(side="right")
        
        progress_bar = ctk.CTkProgressBar(
            self,
            height=6,
            corner_radius=3,
            progress_color=Colors.SUCCESS,
            fg_color=Colors.SURFACE
        )
        progress_bar.pack(fill="x", padx=30, pady=10)
        progress_bar.set(0.8)  # 4/5 = 80%
        
        # Frame scrollable
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=420
        )
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(10, 0))
        
        # Description
        desc_label = ctk.CTkLabel(
            scroll_frame,
            text="Le modèle RIASEC identifie 6 types d'intérêts professionnels.\n"
                 "Évaluez votre intérêt pour chaque type d'activité (de 1 = Pas du tout à 10 = Tout à fait) :",
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 15))
        
        # Questions RIASEC
        riasec_questions = [
            ("realistic", "🔧 Réaliste", 
             "Aimez-vous construire, réparer ou travailler avec des outils et machines ?"),
            ("investigative", "🔬 Investigateur", 
             "Aimez-vous analyser des données, faire des expériences ou résoudre des problèmes complexes ?"),
            ("artistic", "🎨 Artistique", 
             "Aimez-vous dessiner, écrire, jouer de la musique ou exprimer votre créativité ?"),
            ("social", "🤝 Social", 
             "Aimez-vous aider les autres, enseigner ou travailler en groupe ?"),
            ("enterprising", "📢 Entreprenant", 
             "Aimez-vous diriger des projets, prendre des décisions ou convaincre les gens ?"),
            ("conventional", "📋 Conventionnel", 
             "Aimez-vous organiser des informations, suivre des procédures précises ou gérer des données ?"),
        ]
        
        self.riasec_sliders = {}
        for key, label, question in riasec_questions:
            slider = self._create_slider_card(scroll_frame, label, question)
            self.riasec_sliders[key] = slider
        
        # Navigation
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=30, pady=20)
        
        back_btn = ctk.CTkButton(
            nav_frame,
            text="← Retour",
            font=Fonts.BUTTON,
            height=45,
            width=120,
            corner_radius=8,
            fg_color=Colors.SURFACE,
            hover_color=Colors.BORDER,
            command=self.back_callback
        )
        back_btn.pack(side="left")
        
        next_btn = ctk.CTkButton(
            nav_frame,
            text="Suivant : Mes valeurs →",
            font=Fonts.BUTTON,
            height=50,
            width=220,
            corner_radius=8,
            fg_color=Colors.PRIMARY,
            hover_color="#1A5BBF",
            command=self.save_and_continue
        )
        next_btn.pack(side="right")
    
    def _create_slider_card(self, parent, label_text, question_text):
        """Crée une carte avec slider pour une question"""
        card = ctk.CTkFrame(
            parent,
            fg_color=Colors.SURFACE,
            corner_radius=8
        )
        card.pack(fill="x", pady=4)
        
        # Ligne du haut : icône + label
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 2))
        
        ctk.CTkLabel(
            header,
            text=label_text,
            font=Fonts.BODY_BOLD,
            text_color=Colors.TEXT
        ).pack(side="left")
        
        # Question
        ctk.CTkLabel(
            card,
            text=question_text,
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=500,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        # Slider + valeur
        slider_frame = ctk.CTkFrame(card, fg_color="transparent")
        slider_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(
            slider_frame,
            text="1",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_DISABLED,
            width=20
        ).pack(side="left")
        
        slider = ctk.CTkSlider(
            slider_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            width=300,
            progress_color=Colors.PRIMARY
        )
        slider.pack(side="left", padx=10, expand=True, fill="x")
        slider.set(5)
        
        ctk.CTkLabel(
            slider_frame,
            text="10",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_DISABLED,
            width=20
        ).pack(side="left")
        
        value_label = ctk.CTkLabel(
            slider_frame,
            text="5/10",
            font=Fonts.BODY_BOLD,
            text_color=Colors.PRIMARY,
            width=50
        )
        value_label.pack(side="right", padx=(10, 0))
        
        def make_callback(lbl):
            def callback(value):
                lbl.configure(text=f"{int(value)}/10")
            return callback
        
        slider.configure(command=make_callback(value_label))
        
        return slider
    
    def save_and_continue(self):
        """Sauvegarde les scores RIASEC et passe à l'écran suivant"""
        self.student_data["riasec"] = {
            key: int(slider.get()) for key, slider in self.riasec_sliders.items()
        }
        self.next_callback()