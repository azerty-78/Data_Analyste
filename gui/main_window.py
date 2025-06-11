import customtkinter as ctk
from tkinter import filedialog, ttk
import pandas as pd
from analysis.data_analyzer import DataAnalyzer
from analysis.visualization import Visualizer
import os

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.data_analyzer = DataAnalyzer()
        self.visualizer = Visualizer()
        self.df = None
        
        self._create_widgets()
        self._create_layout()
        self._setup_theme()
        
    def _setup_theme(self):
        """Configure le thème de l'application"""
        # Configuration des couleurs
        self.configure(fg_color="#2b2b2b")
        self.main_frame.configure(fg_color="#2b2b2b")
        
        # Configuration des styles
        self.style = ttk.Style()
        self.style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b"
        )
        self.style.configure(
            "Treeview.Heading",
            background="#3b3b3b",
            foreground="white"
        )
        
    def _create_widgets(self):
        # Frame principal avec onglets
        self.tabview = ctk.CTkTabview(self)
        self.tab_data = self.tabview.add("Données")
        self.tab_analysis = self.tabview.add("Analyse")
        self.tab_visualization = self.tabview.add("Visualisation")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.tab_data)
        
        # Bouton d'import avec icône
        self.import_button = ctk.CTkButton(
            self.main_frame,
            text="📂 Importer un fichier Excel",
            command=self._import_excel,
            height=40
        )
        
        # Frame pour la recherche
        self.search_frame = ctk.CTkFrame(self.main_frame)
        
        # Barre de recherche améliorée
        self.search_label = ctk.CTkLabel(
            self.search_frame,
            text="🔍 Rechercher :"
        )
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Entrez votre recherche...",
            height=35
        )
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Rechercher",
            command=self._search_data,
            height=35
        )
        
        # Tableau de résultats de recherche
        self.search_results_frame = ctk.CTkFrame(self.main_frame)
        self.search_results_label = ctk.CTkLabel(
            self.search_results_frame,
            text="📊 Résultats de la recherche :"
        )
        self.search_results_tree = ttk.Treeview(
            self.search_results_frame,
            columns=[],
            show='headings',
            height=5
        )
        self.search_results_scrollbar = ttk.Scrollbar(
            self.search_results_frame,
            orient="vertical",
            command=self.search_results_tree.yview
        )
        self.search_results_tree.configure(yscrollcommand=self.search_results_scrollbar.set)
        
        # Frame pour les suggestions
        self.suggestions_frame = ctk.CTkFrame(self.tab_analysis)
        self.suggestions_label = ctk.CTkLabel(
            self.suggestions_frame,
            text="💡 Suggestions d'analyse :"
        )
        self.suggestions_list = ctk.CTkScrollableFrame(
            self.suggestions_frame,
            height=200
        )
        
        # Zone de texte pour la requête d'analyse
        self.query_frame = ctk.CTkFrame(self.tab_analysis)
        self.query_label = ctk.CTkLabel(
            self.query_frame,
            text="❓ Entrez votre requête d'analyse :"
        )
        self.query_text = ctk.CTkTextbox(
            self.query_frame,
            height=100
        )
        
        # Bouton d'analyse
        self.analyze_button = ctk.CTkButton(
            self.query_frame,
            text="Analyser",
            command=self._analyze_data,
            height=40
        )
        
        # Zone d'affichage des graphiques
        self.plot_frame = ctk.CTkFrame(self.tab_visualization)
        
    def _create_layout(self):
        # Layout des onglets
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Layout de l'onglet Données
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.import_button.pack(pady=10)
        
        # Layout de la recherche
        self.search_frame.pack(fill="x", padx=20, pady=10)
        self.search_label.pack(side="left", padx=5)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_button.pack(side="left", padx=5)
        
        # Layout des résultats de recherche
        self.search_results_frame.pack(fill="x", padx=20, pady=10)
        self.search_results_label.pack(anchor="w", pady=5)
        self.search_results_tree.pack(side="left", fill="both", expand=True)
        self.search_results_scrollbar.pack(side="right", fill="y")
        
        # Layout de l'onglet Analyse
        self.suggestions_frame.pack(fill="x", padx=20, pady=10)
        self.suggestions_label.pack(anchor="w", pady=5)
        self.suggestions_list.pack(fill="x", padx=5, pady=5)
        
        self.query_frame.pack(fill="x", padx=20, pady=10)
        self.query_label.pack(pady=(20,5))
        self.query_text.pack(fill="x", padx=20)
        self.analyze_button.pack(pady=10)
        
        # Layout de l'onglet Visualisation
        self.plot_frame.pack(fill="both", expand=True, pady=20)
        
    def _import_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            try:
                self.df = pd.read_excel(file_path)
                self.import_button.configure(
                    text=f"📂 Fichier importé : {os.path.basename(file_path)}"
                )
                self._setup_search_results_table()
                self._update_suggestions()
            except Exception as e:
                self._show_error(f"Erreur lors de l'import : {str(e)}")
                
    def _setup_search_results_table(self):
        """Configure le tableau de résultats de recherche"""
        if self.df is not None:
            # Configuration des colonnes
            self.search_results_tree['columns'] = list(self.df.columns)
            for col in self.df.columns:
                self.search_results_tree.heading(col, text=col)
                self.search_results_tree.column(col, width=100)
                
    def _search_data(self):
        """Effectue la recherche dans les données"""
        if self.df is None:
            self._show_error("Veuillez d'abord importer un fichier Excel")
            return
            
        search_term = self.search_entry.get().lower()
        if not search_term:
            return
            
        # Effacer les résultats précédents
        for item in self.search_results_tree.get_children():
            self.search_results_tree.delete(item)
            
        # Recherche dans toutes les colonnes
        mask = pd.DataFrame(False, index=self.df.index, columns=['match'])
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                mask['match'] |= self.df[col].astype(str).str.lower().str.contains(search_term)
            else:
                mask['match'] |= self.df[col].astype(str).str.contains(search_term)
                
        # Affichage des résultats
        results = self.df[mask['match']]
        for _, row in results.iterrows():
            self.search_results_tree.insert('', 'end', values=list(row))
            
    def _update_suggestions(self):
        """Met à jour les suggestions d'analyse"""
        # Nettoyage des suggestions précédentes
        for widget in self.suggestions_list.winfo_children():
            widget.destroy()
            
        if self.df is None:
            return
            
        # Récupération des suggestions
        suggestions = self.data_analyzer.get_suggestions(self.df)
        
        # Création des boutons de suggestion
        for suggestion in suggestions:
            suggestion_frame = ctk.CTkFrame(self.suggestions_list)
            suggestion_frame.pack(fill="x", padx=5, pady=2)
            
            title_label = ctk.CTkLabel(
                suggestion_frame,
                text=suggestion['title'],
                font=("Helvetica", 12, "bold")
            )
            title_label.pack(anchor="w", padx=5, pady=2)
            
            desc_label = ctk.CTkLabel(
                suggestion_frame,
                text=suggestion['description'],
                font=("Helvetica", 10)
            )
            desc_label.pack(anchor="w", padx=5, pady=2)
            
            button = ctk.CTkButton(
                suggestion_frame,
                text="Analyser",
                command=lambda s=suggestion: self._apply_suggestion(s)
            )
            button.pack(anchor="e", padx=5, pady=2)
            
    def _apply_suggestion(self, suggestion):
        """Applique une suggestion d'analyse"""
        # Mise à jour de la zone de texte
        self.query_text.delete("1.0", "end")
        self.query_text.insert("1.0", suggestion['description'])
        
        # Exécution de l'analyse
        self._analyze_data()
        
    def _analyze_data(self):
        if self.df is None:
            self._show_error("Veuillez d'abord importer un fichier Excel")
            return
            
        query = self.query_text.get("1.0", "end-1c")
        if not query:
            self._show_error("Veuillez entrer une requête d'analyse")
            return
            
        try:
            # Analyse des données
            analysis_results = self.data_analyzer.analyze(self.df, query)
            chart_type = analysis_results.get('chart_type')
            
            # Génération des visualisations
            self.visualizer.create_visualizations(
                self.df,
                analysis_results,
                self.plot_frame,
                chart_type=chart_type
            )
        except Exception as e:
            self._show_error(f"Erreur lors de l'analyse : {str(e)}")
            
    def _show_error(self, message):
        """Affiche une fenêtre d'erreur stylisée"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("❌ Erreur")
        error_window.geometry("400x150")
        
        # Configuration du style
        error_window.configure(fg_color="#2b2b2b")
        
        # Message d'erreur
        label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=350,
            font=("Helvetica", 12)
        )
        label.pack(pady=20)
        
        # Bouton de fermeture
        button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            height=35
        )
        button.pack(pady=10) 