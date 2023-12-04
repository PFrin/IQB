# Auteur: Malo Rihet
# Date: 30 octobre 2023
# Description: Ce script permet de cloner le projet IQB et l'initialiser dans le répertoire actuel.
# Licence: IODA GROUP
# exécution du script : python deploy_script.py

# Importation des modules nécessaires
import os
import subprocess
import platform
import django
from django.conf import settings
from polls.defaults import QUESTION_TYPES


# URL du repo GitHub à cloner
GITHUB_REPO_URL = "https://github.com/votre-utilisateur/votre-projet.git"
# Path des fixtures à charger
FIXTURE_PATH = "chemin/vers/votre/fixtures.json"

#####################################################

# Demander à l'utilisateur s'il souhaite créer le projet ici
def ask_user_for_confirmation():
    while True:
        user_response = input("Voulez-vous créer le projet ici? (O/N): ").strip().lower()
        if user_response in ['o', 'oui']:
            print("Téléchargement du projet en cours...")
            return True
        elif user_response in ['n', 'non']:
            print("Vous avez choisi de ne pas créer le projet ici. Relancez le programme dans le bon emplacement.")
            return False
        else:
            print("Réponse invalide. Veuillez répondre par 'O' ou 'N'.")

# Clonage du projet GitHub
def clone_github_project(destination):
    print("Clonage du projet...")
    try:
        subprocess.run(["git", "clone", GITHUB_REPO_URL, destination], check=True)
        print("Projet cloné avec succès")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erreur Git : {str(e)}. Le clonage du projet a échoué.")

# Install paquets nécessaires du projet GitHub
def install_requirements(directory):
    print("Installation des dépendances...")
    try:
        requirements_file = os.path.join(directory, 'requirements.txt')
        subprocess.run(["pip", "install", "-r", requirements_file], check=True)
        print("Dépendances installées avec succès")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation des dépendances : {str(e)}")

# Initialisation des paramètres Django
def initialize_django_settings(directory):
    # Path fichier de configuration Django
    settings_file = os.path.join(directory, 'votre_projet', 'settings.py')
    with open(settings_file, 'r') as f:
        settings_content = f.read()
        settings_content = settings_content.replace("DATABASES = {", "DATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.sqlite3',\n        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),\n    }\n}")
    with open(settings_file, 'w') as f:
        f.write(settings_content)
        
# Migrer la base de données --> makemigrations et migrate
def migrate_database():
    try:
        subprocess.run(["python", "./manage.py", "makemigrations"])
        subprocess.run(["python", "./manage.py", "migrate"])
        print("Migrations effectuées avec succès")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors des migrations de la base de données : {str(e)}")
        
# Initialisation de la base de données
def initialize_database():
    print("script pas fini")
    #print("Donnée initiales chargées avec succès")
    '''
    from your_app.models import Type
    je récupere les typeQuesstion du fichier defaults.py 
    CreateType(typeQuesstion) en rejoutant la méthode dans le model 
    '''
        
def load_initial_data():
    try:
        subprocess.run(["python", "./manage.py", "loaddata", FIXTURE_PATH])
        print("Données initiales chargées avec succès")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du chargement des données initiales : {str(e)}")

# Créer un superutilisateur
def create_superuser():
    try:
        subprocess.run(["python", "./manage.py", "createsuperuser"])
        print("Superutilisateur créé avec succès")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la création du superutilisateur : {str(e)}")

# Lancer le serveur
def run_server():
    try:
        subprocess.run(["python", "./manage.py", "runserver"])
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du démarrage du serveur : {str(e)}")

def main():
    # Début du programme
    print("Début du programme")
    
    # Variables
    current_directory = os.getcwd()
    operating_system = platform.system()

    # Affichage des informations
    print(f"Système d'exploitation détecté : {operating_system}")
    print(f"Répertoire actuel : {current_directory}")

    if ask_user_for_confirmation():                           # Demander confirmation à l'utilisateur
        if clone_github_project(current_directory):           # Cloner le projet
            if install_requirements(current_directory):       # Installez les dépendances
                initialize_django_settings(current_directory) # Initialiser les paramètres Django
                migrate_database()                            # Migrer la base de données
                load_initial_data()                           # Charger les données initiales    
                create_superuser()                            # Créer un superutilisateur
                run_server()                                  # Lancer le serveur

    if __name__ == "__main__":
        main()
    
    
    

# vérifier initialize_django_settings
# vérifier create_superuser
# vérifier run_server
# INITIAL_DATA_FIXTURES
# FIXTURE_PATH
# vérifier si table de base de données est complète ? 
'''
# Assurez-vous que les paramètres Django sont chargés
django.setup()
    
# Appelez votre fonction d'initialisation
initialize_table()
'''




#####################################################
#   ! executer avant migrate lors du deploiement !  #
#   ! Pour éxécuter le script :                     #
#   ! python manage.py shell < deploy_script.py     #
#   ! Pour éxécution automatique :                  #
#   ! -> étudier signal.py de django                #
#####################################################

# executer la commande "pip -r ./requirement.txt"
# modifier la bdd dans settings.py pour mettre celle par défaut "sqllite3.db" de django 
# executer la commande "python ./manage.py createsuperuser"
# Suivre les commandes pour créer un super admin
# executer la commande "python ./manage.py runserver"
# Se logger au site : 127.0.0.1:8000/admin
# Se loger au site admin avec les identifiants du super user 
# Se rendre sur la table "Type" 
# Ajouter les différents type (donner la liste exacte)
# Enregistrer et se rendre sur le site : 127.0.0.1:8000
# Créer un user et se logger au site avec le bon Login et le bon PWD