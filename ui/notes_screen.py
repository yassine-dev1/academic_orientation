import customtkinter as ctk
from ui.styles import Colors, Fonts, Sizes


class NotesScreen(ctk.CTkFrame):
    def __init__(self, parent, student_data, next_callback):
        super().__init__(parent, fg_color="transparent")
        self.student_data = student_data
        self.next_callback = next_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(30, 0))
        
        title = ctk.CTkLabel(
            header_frame,
            text="📊 Étape 1 : Vos Notes",
            font=Fonts.TITLE,
            text_color=Colors.TEXT
        )
        title.pack(side="left")
        
        progress_label = ctk.CTkLabel(
            header_frame,
            text="1/5",
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
        progress_bar.set(0.25)
        
        # Frame scrollable pour les notes
        notes_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=450
        )
        notes_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        subjects = [
            ("math", "Mathématiques", "📐"),
            ("physics", "Physique", "⚡"),
            ("biology", "Biologie", "🧬"),
            ("chemistry", "Chimie", "🧪"),
            ("french", "Français", "📖"),
            ("philosophy", "Philosophie", "💭"),
            ("economics", "Économie", "📈"),
            ("art", "Arts", "🎨")
        ]
        
        self.note_entries = {}
        
        for subject, name, icon in subjects:
            card = ctk.CTkFrame(
                notes_frame,
                fg_color=Colors.SURFACE,
                corner_radius=8
            )
            card.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                card,
                text=icon,
                font=("Segoe UI", 20),
                width=40
            ).pack(side="left", padx=15, pady=10)
            
            ctk.CTkLabel(
                card,
                text=name,
                font=Fonts.BODY_BOLD,
                text_color=Colors.TEXT,
                width=120
            ).pack(side="left", padx=10)
            
            slider = ctk.CTkSlider(
                card,
                from_=0,
                to=20,
                number_of_steps=20,
                width=300,
                progress_color=Colors.PRIMARY
            )
            slider.pack(side="left", padx=20)
            slider.set(12)
            
            value_label = ctk.CTkLabel(
                card,
                text="12/20",
                font=Fonts.BODY_BOLD,
                text_color=Colors.PRIMARY,
                width=50
            )
            value_label.pack(side="right", padx=15)
            
            def make_callback(slider, label):
                def callback(value):
                    label.configure(text=f"{int(value)}/20")
                return callback
            
            slider.configure(command=make_callback(slider, value_label))
            self.note_entries[subject] = slider
        
        # Navigation
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=30, pady=20)
        
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
        for subject, slider in self.note_entries.items():
            self.student_data["notes"][subject] = int(slider.get())
        self.next_callback()