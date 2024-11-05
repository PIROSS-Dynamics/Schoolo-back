import subprocess
import os

def generate_docs():
    docs_folder = "docs"
    input_file = os.path.join(docs_folder, "index.adoc")
    output_html = os.path.join(docs_folder, "output.html")
    output_pdf = os.path.join(docs_folder, "output.pdf")

    # Générer la documentation HTML
    subprocess.run(["asciidoctor", "-o", output_html, input_file], check=True)
    # Générer la documentation PDF
    subprocess.run(["asciidoctor-pdf", "-o", output_pdf, input_file], check=True)

    print("Documentation générée avec succès.")

if __name__ == "__main__":
    generate_docs()
