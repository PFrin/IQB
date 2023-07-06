# deploy_script.py

import os
import django
from django.core.management import call_command
from polls.defaults import QUESTION_TYPES

# Définir le chemin vers votre fichier de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
# Assurez-vous d'appeler django.setup() avant d'importer des modèles
django.setup()

def create_question_types():
    """
    Crée les types de questions dans la base de données à partir du fichier default.py.
    """
    for question_type in QUESTION_TYPES:
        call_command('shell', '-c', f"from myapp.models import Type; Type.objects.get_or_create(typeQuestion='{question_type}')")

if __name__ == '__main__':
    create_question_types()


#####################################################
#   ! executer avant migrate lors du deploiement !  #
#   ! Pour éxécuter le script :                     #
#   ! python manage.py shell < deploy_script.py     #
#   ! Pour éxécution automatique :                  #
#   ! -> étudier signal.py de django                #
#####################################################