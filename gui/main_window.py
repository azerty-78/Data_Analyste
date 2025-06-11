import customtkinter as ctk
from tkinter import filedialog, ttk
import pandas as pd
from analysis.data_analyzer import DataAnalyzer
from analysis.visualization import Visualizer

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.data_analyzer = DataAnalyzer()
        self.visualizer = Visualizer()
        self.df = None
        
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        
        # Bouton d'import
        self.import_button = ctk.CTkButton(
            self.main_frame,
            text="Importer un fichier Excel",
            command=self._import_excel
        )
        
        # Frame pour la recherche
        self.search_frame = ctk.CTkFrame(self.main_frame)
        
        # Barre de recherche
        self.search_label = ctk.CTkLabel(
            self.search_frame,
            text="Rechercher :"
        )
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Entrez votre recherche..."
        )
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Rechercher",
            command=self._search_data
        )
        
        # Tableau de résultats de recherche
        self.search_results_frame = ctk.CTkFrame(self.main_frame)
        self.search_results_label = ctk.CTkLabel(
            self.search_results_frame,
            text="Résultats de la recherche :"
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
        
        # Zone de texte pour la requête d'analyse
        self.query_label = ctk.CTkLabel(
            self.main_frame,
            text="Entrez votre requête d'analyse :"
        )
        self.query_text = ctk.CTkTextbox(
            self.main_frame,
            height=100
        )
        
        # Bouton d'analyse
        self.analyze_button = ctk.CTkButton(
            self.main_frame,
            text="Analyser",
            command=self._analyze_data
        )
        
        # Zone d'affichage des graphiques
        self.plot_frame = ctk.CTkFrame(self.main_frame)
        
    def _create_layout(self):
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
        
        self.query_label.pack(pady=(20,5))
        self.query_text.pack(fill="x", padx=20)
        self.analyze_button.pack(pady=10)
        self.plot_frame.pack(fill="both", expand=True, pady=20)
        
    def _import_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            try:
                self.df = pd.read_excel(file_path)
                self.import_button.configure(
                    text=f"Fichier importé : {file_path.split('/')[-1]}"
                )
                # Configuration du tableau de résultats
                self._setup_search_results_table()
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
            if not chart_type:
                chart_type = self._ask_chart_type()
                if not chart_type:
                    return
            # Génération des visualisations
            self.visualizer.create_visualizations(
                self.df,
                analysis_results,
                self.plot_frame,
                chart_type=chart_type
            )
        except Exception as e:
            self._show_error(f"Erreur lors de l'analyse : {str(e)}")

    def _ask_chart_type(self):
        """Ouvre une boîte de dialogue pour demander le type de graphique à l'utilisateur"""
        import tkinter.simpledialog
        options = {"Diagramme en barres": "bar", "Diagramme circulaire (camembert)": "pie", "Courbe (ligne)": "line"}
        choice = tkinter.simpledialog.askstring(
            "Type de graphique",
            "Quel type de graphique souhaitez-vous ? (bar, pie, line)",
            parent=self
        )
        if choice:
            choice = choice.lower()
            if "bar" in choice:
                return "bar"
            if "pie" in choice or "camembert" in choice or "cercle" in choice:
                return "pie"
            if "line" in choice or "courbe" in choice or "ligne" in choice:
                return "line"
        return None
            
    def _show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Erreur")
        error_window.geometry("400x100")
        
        label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=350
        )
        label.pack(pady=20)
        
        button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        button.pack(pady=10) 