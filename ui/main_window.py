"""
Fenêtre principale du système expert d'orientation
Version stable sans segmentation fault
"""

import customtkinter as ctk
from tkinter import messagebox
from ui.styles import Colors, Fonts, Sizes
from core2.moteur.expert_engine import ExpertEngine


class ModernOrientationApp(ctk.CTk):
    """Application principale"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration
        self.title("🎓 Système Expert d'Orientation Académique")
        self.geometry(f"{Sizes.WINDOW_WIDTH}x{Sizes.WINDOW_HEIGHT}")
        self.minsize(800, 600)
        self.configure(fg_color=Colors.BACKGROUND)
        
        # Moteur expert
        self.engine = ExpertEngine()
        self.engine.set_debug(True)
        
        # Données étudiant (ajout de riasec et valeurs)
        self.student_data = {
            "notes": {},
            "preferences": [],
            "qualities": [],
            "riasec": {},
            "valeurs": {}
        }
        
        # Configuration thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Frame principal qui contiendra tout (on ne le détruit jamais)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Écran actuel
        self.current_screen = None
        
        # Afficher l'écran d'accueil
        self.show_welcome_screen()
        
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (Sizes.WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (Sizes.WINDOW_HEIGHT // 2)
        self.geometry(f"{Sizes.WINDOW_WIDTH}x{Sizes.WINDOW_HEIGHT}+{x}+{y}")
    
    def clear_screen(self):
        """Nettoie l'écran actuel"""
        if self.current_screen:
            self.current_screen.destroy()
    
    def show_welcome_screen(self):
        """Affiche l'écran d'accueil"""
        self.clear_screen()
        
        from ui.welcome_screen import WelcomeScreen
        self.current_screen = WelcomeScreen(
            self.main_container, 
            self.start_evaluation,
            self.engine
        )
        self.current_screen.pack(fill="both", expand=True)
    
    def start_evaluation(self):
        """Démarre l'évaluation"""
        self.clear_screen()
        
        from ui.notes_screen import NotesScreen
        self.current_screen = NotesScreen(
            self.main_container,
            self.student_data,
            self.show_preferences_screen
        )
        self.current_screen.pack(fill="both", expand=True)
    
    def show_preferences_screen(self):
        """Affiche l'écran des préférences"""
        self.clear_screen()
        
        from ui.preferences_screen import PreferencesScreen
        self.current_screen = PreferencesScreen(
            self.main_container,
            self.student_data,
            self.show_qualities_screen,
            self.start_evaluation
        )
        self.current_screen.pack(fill="both", expand=True)
    
    def show_qualities_screen(self):
        """Affiche l'écran des qualités"""
        self.clear_screen()
        
        from ui.qualities_screen import QualitiesScreen
        self.current_screen = QualitiesScreen(
            self.main_container,
            self.student_data,
            self.show_riasec_screen,
            self.show_preferences_screen
        )
        self.current_screen.pack(fill="both", expand=True)
    
    # def show_personality_screen(self):
    #     """Affiche l'écran RIASEC + Valeurs Professionnelles"""
    #     self.clear_screen()
        
    #     from ui.personality_screen import PersonalityScreen
    #     self.current_screen = PersonalityScreen(
    #         self.main_container,
    #         self.student_data,
    #         self.evaluate_and_show_results,
    #         self.show_qualities_screen
    #     )
    #     self.current_screen.pack(fill="both", expand=True)
 

    def show_riasec_screen(self):
        """Affiche l'écran RIASEC"""
        self.clear_screen()
        
        from ui.riasec_screen import RiasecScreen
        self.current_screen = RiasecScreen(
            self.main_container,
            self.student_data,
            self.show_values_screen,
            self.show_qualities_screen
        )
        self.current_screen.pack(fill="both", expand=True)

    def show_values_screen(self):
        """Affiche l'écran des Valeurs Professionnelles"""
        self.clear_screen()
        
        from ui.values_screen import ValuesScreen
        self.current_screen = ValuesScreen(
            self.main_container,
            self.student_data,
            self.evaluate_and_show_results,
            self.show_riasec_screen
        )
        self.current_screen.pack(fill="both", expand=True)
    
    def evaluate_and_show_results(self):
        """Évalue et affiche les résultats"""
        # Afficher un écran de chargement
        self.clear_screen()
        
        from ui.loading_screen import LoadingScreen
        self.current_screen = LoadingScreen(
            self.main_container,
            self.student_data,
            self.engine,
            self.show_results_screen,
            self.start_evaluation
        )
        self.current_screen.pack(fill="both", expand=True)
    
    def show_results_screen(self, result):
        """Affiche les résultats"""
        self.clear_screen()
        
        from ui.results_view import ResultsView
        self.current_screen = ResultsView(
            self.main_container,
            result,
            self.engine,
            self.start_evaluation,
            self.student_data
        )
        self.current_screen.pack(fill="both", expand=True)


def run():
    app = ModernOrientationApp()
    app.mainloop()


if __name__ == "__main__":
    run()