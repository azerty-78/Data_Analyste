import customtkinter as ctk
from gui.main_window import MainWindow
import sys

def main():
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