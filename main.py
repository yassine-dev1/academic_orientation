#!/usr/bin/env python3
"""
Système Expert d'Orientation Académique
Avec moteur d'inférence CLIPS (NASA) et interface moderne
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import run

if __name__ == "__main__":
    run()