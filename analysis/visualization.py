import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

class Visualizer:
    def __init__(self):
        # Configuration du style des graphiques
        plt.style.use('dark_background')  # Utilisation d'un style standard de matplotlib
        self._setup_custom_colors()
        
    def _setup_custom_colors(self):
        """Configure les couleurs personnalisées pour les graphiques"""
        # Palette de couleurs moderne
        self.colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f1c40f',
                      '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b']
        
        # Création d'une colormap personnalisée
        self.cmap = LinearSegmentedColormap.from_list(
            'custom_cmap',
            ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c']
        )
        
        # Configuration des styles Seaborn
        sns.set_palette(self.colors)
        sns.set_style("darkgrid")  # Utilisation d'un style Seaborn standard
        
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
        elif chart_type == 'bar':
            self._create_bar_chart(data, columns, frame)
        elif chart_type == 'line':
            self._create_line_chart(data, columns, frame)
        elif chart_type == 'scatter':
            self._create_scatter_plot(data, columns, frame)
        elif chart_type == 'box':
            self._create_box_plot(data, columns, frame)
        elif chart_type == 'correlation':
            self._create_correlation_matrix(data, columns, frame)
        elif intent['type'] == 'comparison':
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
        
        fig = Figure(figsize=(12, 4 * n_rows), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        
        for i, col in enumerate(columns):
            ax = fig.add_subplot(n_rows, n_cols, i + 1)
            ax.set_facecolor('#2b2b2b')
            
            if df[col].dtype in ['int64', 'float64']:
                # Graphique pour les données numériques
                sns.histplot(data=df, x=col, ax=ax, color=self.colors[i % len(self.colors)])
                ax.set_title(f'Distribution de {col}', color='white')
            else:
                # Graphique pour les données catégorielles
                value_counts = df[col].value_counts().head(10)
                sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette=self.colors)
                ax.set_title(f'Top 10 de {col}', color='white')
                plt.xticks(rotation=45)
                
            # Personnalisation des axes
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            
        fig.tight_layout()
        
        # Intégration dans l'interface
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_pie_chart(self, df, columns, frame):
        """
        Crée un diagramme circulaire (camembert)
        """
        col = columns[0]
        value_counts = df[col].value_counts().head(10)
        
        fig = Figure(figsize=(8, 8), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')
        
        # Création du graphique
        wedges, texts, autotexts = ax.pie(
            value_counts.values,
            labels=value_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=self.colors
        )
        
        # Personnalisation des textes
        plt.setp(autotexts, size=8, weight="bold", color="white")
        plt.setp(texts, size=8, color="white")
        
        ax.set_title(f"Répartition de {col}", color='white')
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_bar_chart(self, df, columns, frame):
        """
        Crée un diagramme en barres
        """
        col = columns[0]
        value_counts = df[col].value_counts().head(10)
        
        fig = Figure(figsize=(10, 6), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')
        
        # Création du graphique
        sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette=self.colors)
        
        # Personnalisation
        ax.set_title(f'Top 10 de {col}', color='white')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        plt.xticks(rotation=45)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_line_chart(self, df, columns, frame):
        """
        Crée un graphique en ligne
        """
        fig = Figure(figsize=(10, 6), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')
        
        for i, col in enumerate(columns):
            if df[col].dtype in ['int64', 'float64']:
                df[col].plot(ax=ax, label=col, color=self.colors[i % len(self.colors)])
                
        # Personnalisation
        ax.set_title('Évolution des valeurs', color='white')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.legend(facecolor='#2b2b2b', edgecolor='none', labelcolor='white')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_scatter_plot(self, df, columns, frame):
        """
        Crée un nuage de points
        """
        if len(columns) < 2:
            return
            
        fig = Figure(figsize=(10, 6), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')
        
        # Création du graphique
        sns.scatterplot(
            data=df,
            x=columns[0],
            y=columns[1],
            ax=ax,
            color=self.colors[0]
        )
        
        # Personnalisation
        ax.set_title(f'Relation entre {columns[0]} et {columns[1]}', color='white')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_box_plot(self, df, columns, frame):
        """
        Crée un diagramme en boîte
        """
        fig = Figure(figsize=(10, 6), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')
        
        # Création du graphique
        sns.boxplot(data=df[columns], ax=ax, palette=self.colors)
        
        # Personnalisation
        ax.set_title('Distribution des valeurs', color='white')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_correlation_matrix(self, df, columns, frame):
        """
        Crée une matrice de corrélation
        """
        # Calcul de la matrice de corrélation
        corr_matrix = df[columns].corr()
        
        fig = Figure(figsize=(10, 8), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')
        
        # Création du graphique
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap=self.cmap,
            ax=ax,
            fmt='.2f',
            square=True
        )
        
        # Personnalisation
        ax.set_title('Matrice de corrélation', color='white')
        ax.tick_params(colors='white')
        
        fig.tight_layout()
        
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