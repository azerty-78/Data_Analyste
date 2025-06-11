import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self):
        # Configuration du style des graphiques
        sns.set_theme(style="whitegrid", palette="husl")
        
    def create_visualizations(self, df, analysis_results, frame, chart_type=None):
        """
        Crée les visualisations appropriées en fonction des résultats d'analyse
        """
        # Nettoyage du frame
        for widget in frame.winfo_children():
            widget.destroy()
            
        data = analysis_results['data']
        columns = analysis_results['columns']
        intent = analysis_results['intent']
        
        # Création des graphiques en fonction du type demandé
        if chart_type == 'pie':
            self._create_pie_chart(data, columns, frame)
        elif chart_type == 'bar' or (intent['type'] == 'visualisation' and not chart_type):
            self._create_basic_visualizations(data, columns, frame)
        elif chart_type == 'line':
            self._create_trend_visualizations(data, columns, frame)
        elif intent['type'] == 'comparaison':
            self._create_comparison_visualizations(data, columns, frame)
        elif intent['type'] == 'distribution':
            self._create_distribution_visualizations(data, columns, frame)
        else:
            self._create_basic_visualizations(data, columns, frame)
        
    def _create_basic_visualizations(self, df, columns, frame):
        """
        Crée des visualisations de base pour les données
        """
        # Création d'une grille de graphiques
        n_cols = min(2, len(columns))
        n_rows = (len(columns) + 1) // 2
        
        fig = Figure(figsize=(12, 4 * n_rows))
        
        for i, col in enumerate(columns):
            ax = fig.add_subplot(n_rows, n_cols, i + 1)
            
            if df[col].dtype in ['int64', 'float64']:
                # Graphique pour les données numériques
                sns.histplot(data=df, x=col, ax=ax)
                ax.set_title(f'Distribution de {col}')
            else:
                # Graphique pour les données catégorielles
                value_counts = df[col].value_counts().head(10)
                sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
                ax.set_title(f'Top 10 de {col}')
                plt.xticks(rotation=45)
                
        fig.tight_layout()
        
        # Intégration dans l'interface
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_comparison_visualizations(self, df, columns, frame):
        """
        Crée des visualisations de comparaison
        """
        if len(columns) < 2:
            return
            
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        
        # Création d'un graphique de comparaison
        df_grouped = df.groupby(columns[0])[columns[1]].value_counts().unstack()
        df_grouped.plot(kind='bar', ax=ax)
        
        ax.set_title(f'Comparaison entre {columns[0]} et {columns[1]}')
        plt.xticks(rotation=45)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_distribution_visualizations(self, df, columns, frame):
        """
        Crée des visualisations de distribution
        """
        fig = Figure(figsize=(12, 6))
        
        for i, col in enumerate(columns):
            ax = fig.add_subplot(1, len(columns), i + 1)
            sns.boxplot(data=df, y=col, ax=ax)
            ax.set_title(f'Distribution de {col}')
            
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_trend_visualizations(self, df, columns, frame):
        """
        Crée des visualisations de tendances
        """
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        
        for col in columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col].plot(ax=ax, label=col)
                
        ax.set_title('Évolution des valeurs')
        ax.legend()
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def _create_pie_chart(self, df, columns, frame):
        """
        Crée un diagramme circulaire (camembert) pour la première colonne catégorielle
        """
        col = columns[0]
        value_counts = df[col].value_counts().head(10)
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=140)
        ax.set_title(f"Répartition de {col}")
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True) 