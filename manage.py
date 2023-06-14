#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from django.conf import settings
#from polls.models import Type

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IQB.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def initialize_table():
    # Vérifiez d'abord si des enregistrements existent déjà dans la table
    if Type.objects.exists():
        print("La table 'Type' existe déjà. Aucune initialisation nécessaire.")
        return
    
    # Créez les objets Type avec les valeurs spécifiées
    type_1 = Type.objects.create(typeQuestion="Question à échelle")
    type_2 = Type.objects.create(typeQuestion="question ouverte")
    type_3 = Type.objects.create(typeQuestion="choix multiple")
    type_4 = Type.objects.create(typeQuestion="Choix unique")

    print("Initialisation de la table 'Type' terminée.")

if __name__ == '__main__':
    main()

    #initialize_table()

    #execute_from_command_line(sys.argv)