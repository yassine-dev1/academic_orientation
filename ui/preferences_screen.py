import customtkinter as ctk
from ui.styles import Colors, Fonts, Sizes


class PreferencesScreen(ctk.CTkFrame):
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
            text="🎯 Étape 2 : Centres d'intérêt",
            font=Fonts.TITLE,
            text_color=Colors.TEXT
        )
        title.pack(side="left")
        
        progress_label = ctk.CTkLabel(
            header_frame,
            text="2/5",
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
        progress_bar.set(0.50)
        
        ctk.CTkLabel(
            self,
            text="Sélectionnez les domaines qui vous intéressent :",
            font=Fonts.SUBTITLE,
            text_color=Colors.TEXT_SECONDARY
        ).pack(pady=(20, 0))
        
        interests_frame = ctk.CTkFrame(self, fg_color="transparent")
        interests_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        interests = [
            ("technology", "💻 Technologie & Innovation"),
            ("health", "🏥 Santé & Médecine"),
            ("art", "🎨 Art & Créativité"),
            ("justice", "⚖️ Droit & Justice"),
            ("business", "📊 Commerce & Gestion"),
        ]
        
        self.pref_vars = {}
        
        for i, (key, label) in enumerate(interests):
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(
                interests_frame,
                text=label,
                variable=var,
                font=Fonts.BODY,
                fg_color=Colors.PRIMARY,
                hover_color=Colors.PRIMARY_DARK,
                border_color=Colors.BORDER
            )
            cb.pack(anchor="w", pady=5)
            self.pref_vars[key] = var
        
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
            text="Suivant →",
            font=Fonts.BUTTON,
            height=45,
            width=150,
            corner_radius=8,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_DARK,
            command=self.save_and_next
        )
        next_btn.pack(side="right")
    
    def save_and_next(self):
        self.student_data["preferences"] = [key for key, var in self.pref_vars.items() if var.get()]
        self.next_callback()