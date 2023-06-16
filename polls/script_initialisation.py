# script_initialisation.py

import os
import django
from django.conf import settings

def initialize_table():
    # Initialisez ici la table de votre base de données selon vos besoins
    pass

if __name__ == '__main__':
    # Définissez le chemin vers le fichier de configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nom_de_votre_projet.settings')
    
    # Assurez-vous que les paramètres Django sont chargés
    django.setup()
    
    # Appelez votre fonction d'initialisation
    initialize_table()
