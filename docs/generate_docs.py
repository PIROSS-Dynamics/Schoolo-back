import os
import ast
import subprocess

# Définir le chemin racine du projet (un niveau au-dessus du dossier actuel)
base_dir = os.path.dirname(os.path.dirname(__file__))

def get_apps_structure():
    apps_dir = os.path.join(base_dir, "apps")
    apps_structure = {}

    for app in os.listdir(apps_dir):
        app_path = os.path.join(apps_dir, app)
        if os.path.isdir(app_path):
            # Récupérer les modèles et leurs champs
            models_file = os.path.join(app_path, "models.py")
            models = {}
            if os.path.exists(models_file):
                with open(models_file) as f:
                    tree = ast.parse(f.read())
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef) and any(isinstance(base, ast.Name) and base.id == 'models.Model' for base in node.bases):
                            fields = []
                            for item in node.body:
                                if isinstance(item, ast.Assign) and isinstance(item.value, ast.Call):
                                    field_name = item.targets[0].id
                                    field_type = item.value.func.id
                                    field_options = [f"{kw.arg}={kw.value.value}" for kw in item.value.keywords]
                                    fields.append((field_name, field_type, ", ".join(field_options)))
                            models[node.name] = fields

            # Récupérer les vues et leurs docstrings
            views_file = os.path.join(app_path, "views.py")
            views = {}
            if os.path.exists(views_file):
                with open(views_file) as f:
                    tree = ast.parse(f.read())
                    for node in tree.body:
                        if isinstance(node, ast.FunctionDef):
                            docstring = ast.get_docstring(node)
                            views[node.name] = docstring or "Pas de description disponible."

            # Récupérer les endpoints d'API
            urls_file = os.path.join(app_path, "urls.py")
            urls = []
            if os.path.exists(urls_file):
                with open(urls_file) as f:
                    for line in f:
                        if 'path(' in line or 're_path(' in line:
                            urls.append(line.strip())

            apps_structure[app] = {
                "models": models,
                "views": views,
                "urls": urls
            }
    return apps_structure

def generate_index_adoc():
    # Contenu initial de l'index.adoc
    content = """= Documentation du Projet SCHOOLO
Auteur: Votre Nom <votre.email@example.com>
:toc:
:source-highlighter: coderay

== Introduction

Ceci est la documentation générée automatiquement pour le projet SCHOOLO.

== Guide d'Installation et Configuration

Pour installer et configurer le projet, assurez-vous d'avoir Python et les dépendances listées dans requirements.txt. Voici les principales étapes d'installation :

1. Clonez le dépôt et installez les dépendances.
2. Configurez les variables d'environnement essentielles (comme `DEBUG`, `DATABASES`, etc.).

== Structure des Applications

"""
    # Récupérer la structure des applications
    apps_structure = get_apps_structure()
    for app, details in apps_structure.items():
        content += f"=== Application : {app}\n\n"
        
        # Détail des Modèles
        content += "==== Modèles\n\n"
        if details["models"]:
            for model, fields in details["models"].items():
                content += f"* {model}(models.Model):\n"
                for field_name, field_type, options in fields:
                    content += f"  - {field_name}: {field_type} ({options})\n"
        else:
            content += "_Aucun modèle trouvé._\n"
        
        # Détail des Vues
        content += "\n==== Vues\n\n"
        if details["views"]:
            for view, doc in details["views"].items():
                content += f"* {view}(request):\n  - {doc}\n"
        else:
            content += "_Aucune vue trouvée._\n"
        
        # Détail des Endpoints
        content += "\n==== Endpoints d'API\n\n"
        if details["urls"]:
            for url in details["urls"]:
                content += f"* {url}\n"
        else:
            content += "_Aucun endpoint trouvé._\n"
        
        content += "\n"

    # Section de déploiement
    content += """
== Déploiement

Pour déployer le projet en production :

1. Configurez `DEBUG=False` et `ALLOWED_HOSTS`.
2. Utilisez `python manage.py migrate` pour appliquer les migrations.
3. Utilisez un serveur compatible WSGI, tel que Gunicorn, et configurez un proxy inverse comme Nginx pour gérer les requêtes HTTP.
"""

    # Dossiers et chemins
    docs_folder = os.path.join(base_dir, "docs")
    adoc_folder = os.path.join(docs_folder, "adoc")
    diagram_folder = os.path.join(docs_folder, "diagramme")

    os.makedirs(adoc_folder, exist_ok=True)
    os.makedirs(diagram_folder, exist_ok=True)

    # Génération de l'image PNG depuis le fichier .puml
    puml_file = os.path.join(diagram_folder, "schoolo.puml")
    puml_image = os.path.join(diagram_folder, "schoolo.png")

    if os.path.exists(puml_file):
        # Utilisation de subprocess pour générer l'image
        try:
            subprocess.run(["plantuml", "-tpng", puml_file], check=True)
            content += f"""

== Diagrammes

Diagramme des relations de modèle :

image::{os.path.relpath(puml_image, adoc_folder)}[]
"""
        except subprocess.CalledProcessError:
            content += "\n\n== Diagrammes\n\nErreur lors de la génération de l'image à partir du fichier UML.\n"
    else:
        content += "\n\n== Diagrammes\n\nAucun diagramme UML trouvé.\n"

    # Écriture dans le fichier index.adoc
    index_adoc_path = os.path.join(adoc_folder, "index.adoc")
    with open(index_adoc_path, "w") as f:
        f.write(content)
    
    print("index.adoc généré avec succès.")

def generate_docs():
    docs_folder = os.path.join(base_dir, "docs")
    adoc_folder = os.path.join(docs_folder, "adoc")
    input_file = os.path.join(adoc_folder, "index.adoc")
    output_html = os.path.join(adoc_folder, "docs.html")
    output_pdf = os.path.join(docs_folder, "docs.pdf")

    # Générer la documentation HTML
    subprocess.run(["asciidoctor", "-o", output_html, input_file], check=True)
    # Générer la documentation PDF
    subprocess.run(["asciidoctor-pdf", "-o", output_pdf, input_file], check=True)

    print("Documentation générée avec succès.")

if __name__ == "__main__":
    generate_index_adoc()
    generate_docs()
