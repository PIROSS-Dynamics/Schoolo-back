

[![Build Status](https://github.com/PIROSS-Dynamics/Schoolo-back/actions/workflows/backend_build.yml/badge.svg)](https://github.com/PIROSS-Dynamics/Schoolo-back/actions)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=PIROSS-Dynamics_Schoolo-back&metric=code_smells&branch=develop)](https://sonarcloud.io/summary/new_code?id=PIROSS-Dynamics_Schoolo-back&branch=develop)
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=PIROSS-Dynamics_Schoolo-back)](https://sonarcloud.io/summary/new_code?id=PIROSS-Dynamics_Schoolo-back)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=PIROSS-Dynamics_Schoolo-back&metric=alert_status&branch=develop)](https://sonarcloud.io/dashboard?id=PIROSS-Dynamics_Schoolo-back&branch=develop)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=PIROSS-Dynamics_Schoolo-back&metric=bugs)](https://sonarcloud.io/summary/new_code?id=PIROSS-Dynamics_Schoolo-back)


[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=PIROSS-Dynamics_Schoolo-back&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=PIROSS-Dynamics_Schoolo-back)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=PIROSS-Dynamics_Schoolo-back&metric=code_smells&branch=develop)](https://sonarcloud.io/summary/new_code?id=PIROSS-Dynamics_Schoolo-back&branch=develop)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=PIROSS-Dynamics_Schoolo-back&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=PIROSS-Dynamics_Schoolo-back)




🔗 **Lien vers le répertoire Schoolo front:** 
[![Frontend React](https://img.shields.io/badge/Frontend-React-blue?style=for-the-badge&logo=react)](https://github.com/PIROSS-Dynamics/Schoolo-front)



Lancer le projet :

### Prérequis

- **Python** : Assurez-vous d'avoir Python 3.8 ou une version ultérieure pour garantir la compatibilité avec les packages spécifiés dans `requirements.txt` visible dans le repository Schoolo-back. Vous pouvez vérifier votre version avec la commande `python --version`.
- **npm** : Utilisez la version 10.7.0 pour garantir la compatibilité avec le projet frontend. Vous pouvez vérifier votre version avec la commande `npm -v`.

Si vous devez mettre à jour Python, vous pouvez le télécharger depuis [python.org](https://www.python.org/downloads/).


### Cloner les projets dans un dossier commun :

Créer un dossier où cloner (git clone) les deux repository : Schoolo-front et Schoolo-back


git clone https://github.com/PIROSS-Dynamics/Schoolo-front.git

git clone https://github.com/PIROSS-Dynamics/Schoolo-back.git

### INSTALLATION A LA MAIN COMPLET 

### Dans Schoolo-front

Faire npm install depuis le projet Schoolo-front

### Dans Schoolo-back

Depuis le projet Schoolo-back :

Pour éviter des soucis de versions, vous pouvez faire venv\Scripts\activate (Windows) ou source venv/bin/activate (macOs etLinux) avant l'étape suivante

Faire pip install -r requirements.txt 

Puis faire :
python manage.py makemigrations
python manage.py migrate


### Lancement
Lancer le front avec npm start et lancer le back avec python manage.py runserver

### INSTALLATION SIMPLIFIÉ (fichier de build)

Après avoir cloné le front et le back dans un dossier, créer encore sur ce dossier un fichier de build du projet python avec le code suivant :

```python

import subprocess
import os
import platform

def install_react_dependencies():
    print("Installing React dependencies...")
    react_path = os.path.join(os.getcwd(), "Schoolo-front")
    subprocess.run(["npm", "install"], cwd=react_path, shell=(platform.system() == "Windows"))

def start_react():
    print("Starting React frontend...")
    react_path = os.path.join(os.getcwd(), "Schoolo-front")
    subprocess.Popen(["npm", "start"], cwd=react_path, shell=(platform.system() == "Windows"))

def install_django_dependencies():
    print("Installing Django dependencies...")
    django_path = os.path.join(os.getcwd(), "Schoolo-back")
    venv_path = os.path.join(django_path, "venv/bin/activate") if platform.system() != "Windows" else os.path.join(django_path, "venv\\Scripts\\activate")

    if os.path.exists(os.path.join(django_path, "venv")):
        command = f". {venv_path} && pip install -r requirements.txt" if platform.system() != "Windows" else f"{venv_path} && pip install -r requirements.txt"
    else:
        command = f"pip install -r requirements.txt"

    subprocess.run(command, cwd=django_path, shell=True, executable="/bin/bash" if platform.system() != "Windows" else None)

def start_django():
    print("Starting Django backend...")
    django_path = os.path.join(os.getcwd(), "Schoolo-back")
    venv_path = os.path.join(django_path, "venv/bin/activate") if platform.system() != "Windows" else os.path.join(django_path, "venv\\Scripts\\activate")

    if os.path.exists(os.path.join(django_path, "venv")):
        command = f". {venv_path} && python manage.py runserver" if platform.system() != "Windows" else f"{venv_path} && python manage.py runserver"
    else:
        command = "python manage.py runserver"

    subprocess.Popen(command, cwd=django_path, shell=True, executable="/bin/bash" if platform.system() != "Windows" else None)

if __name__ == "__main__":
    # Installer les dépendances
    install_react_dependencies()
    install_django_dependencies()

    # Lancer le projet
    start_react()
    start_django()

    print("Both projects are starting. React and Django logs will appear in their respective terminals.")


```
Lancer ce fichier de build python pour à la fois installer les dépendances et lancer le front et le back.


### Tests 

Des commandes de tests sont disponibles dans le fichier "commandes utiles pour les devs.txt", fichier disponible à la racine de Schoolo-back

