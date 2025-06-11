import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Force le chemin NLTK
nltk.data.path.append(r'C:\\Users\\Ben Djibril\\AppData\\Roaming\\nltk_data')

class DataAnalyzer:
    def __init__(self):
        # Téléchargement des ressources NLTK nécessaires
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            
        self.stop_words = set(stopwords.words('french'))
        
    def analyze(self, df, query):
        """
        Analyse intelligente de la requête utilisateur
        """
        df_cleaned = self._preprocess_data(df)
        query_intent = self._analyze_query(query)

        # Détection automatique de la colonne cible
        colonne_cible = self._detect_column_from_query(df_cleaned, query)
        if not colonne_cible:
            raise Exception(
                "Aucune colonne correspondante trouvée dans la requête. "
                "Merci de préciser la colonne à analyser ou de reformuler."
            )

        # Détection du type de graphique
        chart_type = self._detect_chart_type_from_query(query)

        relevant_columns = [colonne_cible]
        df_grouped = self._group_similar_data(df_cleaned, relevant_columns)

        return {
            'data': df_grouped,
            'columns': relevant_columns,
            'intent': query_intent,
            'chart_type': chart_type
        }
        
    def _preprocess_data(self, df):
        """
        Prétraite les données : nettoyage, normalisation, etc.
        """
        df_cleaned = df.copy()
        
        # Nettoyage de la colonne Âge : extraction du nombre
        if 'Âge' in df_cleaned.columns:
            df_cleaned['Âge'] = df_cleaned['Âge'].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)
        
        # Nettoyage de la colonne Contact : garder le premier numéro
        if 'Contact' in df_cleaned.columns:
            df_cleaned['Contact'] = df_cleaned['Contact'].astype(str).str.split('/|,| ').str[0].str.replace(r'\D', '', regex=True)
        
        # Conversion en minuscules pour les colonnes textuelles
        for col in df_cleaned.select_dtypes(include=['object']).columns:
            df_cleaned[col] = df_cleaned[col].str.lower().fillna('')
            # Limiter la longueur des textes pour l'analyse
            df_cleaned[col] = df_cleaned[col].str.slice(0, 200)
        
        # Suppression des doublons
        df_cleaned = df_cleaned.drop_duplicates()
        
        # Remplacement des valeurs manquantes par une chaîne vide ou 0
        df_cleaned = df_cleaned.fillna('')
        
        return df_cleaned
        
    def _analyze_query(self, query):
        """
        Analyse la requête utilisateur pour comprendre l'intention
        """
        tokens = word_tokenize(query.lower(), language='french')
        tokens = [t for t in tokens if t not in self.stop_words]
        
        # Détection des mots-clés importants
        keywords = {
            'visualisation': ['montrer', 'afficher', 'voir', 'visualiser'],
            'comparaison': ['comparer', 'différence', 'contre'],
            'distribution': ['répartition', 'distribution', 'répartir'],
            'tendance': ['évolution', 'tendance', 'progression']
        }
        
        intent = {
            'type': 'visualisation',  # par défaut
            'columns': [],
            'filters': []
        }
        
        # Analyse des mots-clés
        for token in tokens:
            for intent_type, words in keywords.items():
                if token in words:
                    intent['type'] = intent_type
                    
        return intent
        
    def _detect_column_from_query(self, df, query):
        """
        Détecte la colonne la plus pertinente à partir de la requête utilisateur
        """
        query = query.lower()
        best_col = None
        best_score = 0
        for col in df.columns:
            col_clean = col.lower()
            # Score de similarité simple (nombre de mots en commun)
            score = sum(1 for mot in col_clean.split() if mot in query)
            if score > best_score:
                best_score = score
                best_col = col
        # On considère qu'il faut au moins 1 mot en commun
        if best_score > 0:
            return best_col
        return None
        
    def _select_relevant_columns(self, df, query_intent):
        """
        Sélectionne les colonnes pertinentes pour l'analyse
        """
        # Analyse des types de données
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Sélection des colonnes en fonction de l'intention
        if query_intent['type'] == 'visualisation':
            return list(categorical_cols) + list(numeric_cols)
        elif query_intent['type'] == 'comparaison':
            return list(categorical_cols)
        elif query_intent['type'] == 'distribution':
            return list(numeric_cols)
        elif query_intent['type'] == 'tendance':
            return list(numeric_cols)
            
        return list(df.columns)
        
    def _group_similar_data(self, df, columns):
        """
        Regroupe les données similaires en utilisant le clustering
        """
        df_grouped = df.copy()
        
        # Pour chaque colonne catégorielle
        for col in df_grouped.select_dtypes(include=['object']).columns:
            # Vectorisation TF-IDF
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(df_grouped[col].fillna(''))
            
            # Clustering
            n_clusters = min(5, len(df_grouped[col].unique()))
            kmeans = KMeans(n_clusters=n_clusters)
            clusters = kmeans.fit_predict(tfidf_matrix)
            
            # Remplacement par les valeurs les plus fréquentes dans chaque cluster
            df_grouped[col] = df_grouped[col].map(
                dict(zip(df_grouped[col].unique(), clusters))
            )
            
        return df_grouped 

    def _detect_chart_type_from_query(self, query):
        """
        Détecte le type de graphique demandé dans la requête utilisateur
        """
        query = query.lower()
        if any(word in query for word in ["camembert", "cercle", "circulaire", "pie"]):
            return "pie"
        if any(word in query for word in ["barres", "histogramme", "bar", "colonnes"]):
            return "bar"
        if any(word in query for word in ["ligne", "line"]):
            return "line"
        return None 