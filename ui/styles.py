"""
Styles modernes pour l'interface du système expert
Theme: Dark Modern Elegant
"""

class Colors:
    """Palette de couleurs professionnelle"""
    # Couleurs principales
    PRIMARY = "#6C63FF"          # Violet moderne
    PRIMARY_DARK = "#5A52D5"     # Violet foncé
    PRIMARY_LIGHT = "#8B84FF"    # Violet clair
    
    SECONDARY = "#FF6584"         # Rose accent
    SECONDARY_DARK = "#E55574"    # Rose foncé
    
    # Couleurs de statut
    SUCCESS = "#00D26A"           # Vert
    WARNING = "#FFB86C"           # Orange
    ERROR = "#FF5555"             # Rouge
    INFO = "#6C63FF"              # Violet info
    
    # Niveaux de gris (dark theme)
    BACKGROUND = "#1A1A2E"        # Fond principal
    SURFACE = "#16213E"           # Surface/cartes
    SURFACE_LIGHT = "#1F2A4A"     # Surface plus claire
    BORDER = "#2D3A5A"            # Bordures
    
    # Texte
    TEXT = "#F8F8F2"              # Texte principal
    TEXT_SECONDARY = "#A9B7C6"    # Texte secondaire
    TEXT_DISABLED = "#5A6B7A"     # Texte désactivé
    
    # Graphiques
    CHART_COLORS = ["#6C63FF", "#FF6584", "#00D26A", "#FFB86C", "#FF5555"]

class Fonts:
    """Polices modernes"""
    TITLE = ("Segoe UI", 28, "bold")
    SUBTITLE = ("Segoe UI", 16, "normal")
    BODY = ("Segoe UI", 12, "normal")
    BODY_BOLD = ("Segoe UI", 12, "bold")
    BUTTON = ("Segoe UI", 13, "bold")
    SMALL = ("Segoe UI", 10, "normal")
    CHART_LABEL = ("Segoe UI", 11, "bold")

class Sizes:
    """Dimensions et espacements"""
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 750
    PADDING_LARGE = 30
    PADDING_MEDIUM = 20
    PADDING_SMALL = 10
    BORDER_RADIUS = 15
    BORDER_RADIUS_SMALL = 8
    ANIMATION_DURATION = 200

class Shadows:
    """Ombres pour les cartes (simulées avec bordures)"""
    CARD = {"border_width": 1, "border_color": Colors.BORDER}
    CARD_HOVER = {"border_width": 1, "border_color": Colors.PRIMARY}