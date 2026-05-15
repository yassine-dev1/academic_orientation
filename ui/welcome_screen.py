import customtkinter as ctk
from ui.styles import Colors, Fonts, Sizes


class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, start_callback, engine):
        super().__init__(parent, fg_color="transparent")
        self.start_callback = start_callback
        
        # Contenu centré
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True)
        
        # Logo
        icon_label = ctk.CTkLabel(
            content_frame,
            text="🎓",
            font=("Segoe UI", 80),
            text_color=Colors.PRIMARY
        )
        icon_label.pack(pady=(0, 20))
        
        # Titre
        title = ctk.CTkLabel(
            content_frame,
            text="Système Expert d'Orientation",
            font=Fonts.TITLE,
            text_color=Colors.TEXT
        )
        title.pack()
        
        # Sous-titre
        subtitle = ctk.CTkLabel(
            content_frame,
            text="Découvrez la voie qui vous correspond le mieux",
            font=Fonts.SUBTITLE,
            text_color=Colors.TEXT_SECONDARY
        )
        subtitle.pack(pady=(10, 40))
        
        # Description
        desc_frame = ctk.CTkFrame(
            content_frame,
            fg_color=Colors.SURFACE,
            corner_radius=Sizes.BORDER_RADIUS
        )
        desc_frame.pack(pady=20, padx=40, fill="x")
        
        desc_text = """
        🔍 Comment ça fonctionne ?
        
        1. Renseignez vos notes dans les matières clés
        2. Indiquez vos centres d'intérêt
        3. Sélectionnez vos qualités personnelles
        4. Obtenez une recommandation personnalisée
        """
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text=desc_text,
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            justify="left"
        )
        desc_label.pack(padx=20, pady=20)
        
        # Bouton démarrer
        start_btn = ctk.CTkButton(
            content_frame,
            text="🚀 Commencer l'évaluation",
            font=Fonts.BUTTON,
            height=50,
            width=250,
            corner_radius=Sizes.BORDER_RADIUS_SMALL,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_DARK,
            command=self.start_callback
        )
        start_btn.pack(pady=40)