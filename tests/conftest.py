import sys
import os

# Ajouter le répertoire racine du projet au PYTHONPATH
# Ce fichier est dans tests/ donc on remonte d'un niveau pour atteindre Projet_info_2A/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
