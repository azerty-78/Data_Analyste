import customtkinter as ctk
from gui.main_window import MainWindow
import sys
import nltk
import os

def setup_nltk():
    """Configure les ressources NLTK nécessaires"""
    # Configuration du chemin NLTK
    nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
    if not os.path.exists(nltk_data_path):
        os.makedirs(nltk_data_path)
    nltk.data.path.append(nltk_data_path)
    
    # Téléchargement des ressources nécessaires
    required_resources = [
        'punkt',
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords'
    ]
    
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}')
        except LookupError:
            nltk.download(resource, download_dir=nltk_data_path)

def main():
    # Configuration de NLTK
    setup_nltk()
    
    # Configuration du thème
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Création de la fenêtre principale
    app = MainWindow()
    app.title("Analyseur de Données Excel")
    app.geometry("1200x800")
    
    # Lancement de l'application
    app.mainloop()

if __name__ == "__main__":
    main() 