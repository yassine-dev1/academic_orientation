import customtkinter as ctk
from ui.styles import Colors, Fonts, Sizes


class LoadingScreen(ctk.CTkFrame):
    def __init__(self, parent, student_data, engine, show_results, restart_callback):
        super().__init__(parent, fg_color="transparent")
        
        self.student_data = student_data
        self.engine = engine
        self.show_results = show_results
        self.restart_callback = restart_callback
        
        # Centre de chargement
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(expand=True)
        
        loading_label = ctk.CTkLabel(
            center_frame,
            text="🤖 Analyse de votre profil...\n\nVeuillez patienter",
            font=Fonts.BODY,
            text_color=Colors.TEXT
        )
        loading_label.pack()
        
        self.progress = ctk.CTkProgressBar(
            center_frame,
            width=300,
            height=10,
            corner_radius=5,
            progress_color=Colors.PRIMARY
        )
        self.progress.pack(pady=20)
        self.progress.start()
        
        # Lancer l'évaluation après un court délai
        self.after(500, self.evaluate)
    
    def evaluate(self):
        try:
            result = self.engine.evaluate_student(
                notes=self.student_data["notes"],
                preferences=self.student_data["preferences"],
                qualites=self.student_data["qualities"]
            )
            self.progress.stop()
            self.show_results(result)
        except Exception as e:
            self.progress.stop()
            print(f"Erreur: {e}")
            self.restart_callback()