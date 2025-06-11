# 📊 Analyseur de Données Excel Intelligent

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.13.3-green)
![License](https://img.shields.io/badge/license-MIT-orange)

</div>

## 🚀 Présentation

Ce logiciel est un outil puissant d'analyse de données Excel qui combine une interface graphique intuitive avec des capacités d'analyse avancées. Il permet aux utilisateurs d'explorer, analyser et visualiser leurs données de manière interactive et intelligente.

## ✨ Fonctionnalités

### 📁 Import et Recherche
- Import facile de fichiers Excel (.xlsx, .xls)
- Barre de recherche intégrée pour trouver rapidement des informations
- Affichage des résultats dans un tableau interactif
- Filtrage et tri des données

### 📊 Analyse Intelligente
- Traitement du langage naturel pour comprendre les requêtes
- Analyse automatique des données
- Regroupement intelligent des données similaires
- Élimination automatique des doublons

### 📈 Visualisations
- Graphiques interactifs et personnalisables
- Différents types de visualisations selon le contexte
- Interface moderne et intuitive
- Export des graphiques

## 🛠️ Installation

### Prérequis
- Python 3.13.3 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_DOSSIER]
```

2. **Créer l'environnement virtuel**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

1. **Lancer l'application**
```bash
python main.py
```

2. **Importer vos données**
   - Cliquez sur "Importer un fichier Excel"
   - Sélectionnez votre fichier Excel

3. **Rechercher des informations**
   - Utilisez la barre de recherche pour trouver des données spécifiques
   - Les résultats s'affichent dans le tableau interactif

4. **Analyser vos données**
   - Entrez votre requête d'analyse dans la zone de texte
   - Les visualisations sont générées automatiquement

## 📁 Structure du Projet

```
📦 projet
 ┣ 📂 analysis
 ┃ ┣ 📜 data_analyzer.py
 ┃ ┗ 📜 visualization.py
 ┣ 📂 gui
 ┃ ┣ 📜 main_window.py
 ┃ ┗ 📜 __init__.py
 ┣ 📜 main.py
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
```

## 🛠️ Technologies Utilisées

- **Interface Graphique** : CustomTkinter
- **Analyse de Données** : Pandas, NumPy
- **Machine Learning** : Scikit-learn
- **Visualisation** : Matplotlib, Seaborn
- **Traitement du Langage** : NLTK

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- Ben Djibril - Développeur Principal

## 🙏 Remerciements

- Merci à tous les contributeurs
- Merci aux bibliothèques open source utilisées
- Merci à la communauté Python

---

<div align="center">
Made with ❤️ by Ben Djibril
</div>
