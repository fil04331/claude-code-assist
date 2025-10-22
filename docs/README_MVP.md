# MVP - Analyse de Tendances Marché Québécois

## 🎯 Vue d'ensemble

Système d'analyse de tendances Google pour le marché québécois, ciblant les secteurs:
- 🛋️ **Meubles** (canapés, tables, lits, etc.)
- 🔌 **Électroménagers** (réfrigérateurs, laveuses, etc.)
- 🛏️ **Matelas** (matelas, literie, oreillers)
- 🏠 **Couvre-planchers** (bois franc, tapis, céramique)

## ✨ Fonctionnalités

- ✅ Collecte automatisée de données Google Trends
- ✅ Stockage local avec SQLite (pas besoin de cloud)
- ✅ Dashboard interactif Streamlit
- ✅ Visualisations temporelles et comparatives
- ✅ Export de données en CSV
- ✅ Historique de 12 mois par défaut

## 🚀 Démarrage Rapide (5 minutes)

### Installation

```bash
# Cloner et installer
git clone https://github.com/fil04331/claude-code-assist.git
cd claude-code-assist

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Créer dossiers
mkdir -p data logs data/backups
```

### Première utilisation

```bash
# 1. Collecter les données (5-10 minutes la première fois)
python run_collection.py

# 2. Lancer le dashboard
python run_dashboard.py
```

Le dashboard s'ouvre automatiquement à: **http://localhost:8501**

## 📊 Captures d'écran du Dashboard

### Onglet Tendances
Visualisation de l'évolution temporelle des mots-clés par catégorie avec métriques clés.

### Onglet Top Keywords
Classement des mots-clés les plus recherchés avec moyennes et pics d'intérêt.

### Onglet Comparaison
Comparaison de l'intérêt entre les différentes catégories du marché.

### Onglet Données
Accès aux données brutes avec possibilité d'export CSV.

## 📁 Structure du Projet

```
claude-code-assist/
├── config/
│   └── config.yaml              # Configuration (mots-clés, paramètres)
├── data/
│   ├── trends.db                # Base de données SQLite (créée automatiquement)
│   └── backups/                 # Sauvegardes de la base
├── docs/
│   ├── INSTALLATION.md          # Guide d'installation détaillé
│   ├── USAGE.md                 # Guide d'utilisation complet
│   └── README_MVP.md            # Ce fichier
├── logs/
│   └── trends_collector.log     # Logs de collecte
├── src/
│   ├── data_collection/
│   │   ├── database.py          # Gestionnaire SQLite
│   │   └── trends_collector.py  # Collecteur Google Trends
│   └── dashboard/
│       └── app.py               # Application Streamlit
├── run_collection.py            # Script de collecte simple
├── run_dashboard.py             # Script de lancement dashboard
├── requirements.txt             # Dépendances Python
└── CLAUDE.md                    # Documentation de référence du projet
```

## 🔧 Configuration

### Mots-clés personnalisés

Éditez `config/config.yaml` pour ajouter/modifier des mots-clés:

```yaml
keywords:
  meubles:
    - "meubles québec"
    - "votre nouveau mot-clé"
```

### Période de collecte

Modifiez la période dans `config/config.yaml`:

```yaml
google_trends:
  timeframe: "today 12-m"  # 12 mois (modifiable)
```

## 📈 Utilisation Quotidienne

### Mettre à jour les données

```bash
python run_collection.py
```

Recommandé: 1 fois par jour

### Automatiser la collecte

**Linux/Mac (cron):**
```bash
# Exécution quotidienne à 2h du matin
0 2 * * * cd /chemin/projet && /chemin/venv/bin/python run_collection.py
```

**Windows (Task Scheduler):**
Créer une tâche planifiée pointant vers `run_collection.py`

## 💡 Exemples d'Utilisation

### Cas d'usage 1: Identifier les tendances saisonnières

Utilisez l'onglet "Tendances" pour voir:
- Quels meubles sont plus recherchés en été vs hiver
- Pics de recherche pour électroménagers (ex: climatiseurs en juin)
- Intérêt pour matelas (possiblement ventes de fin de saison)

### Cas d'usage 2: Comparer les catégories

L'onglet "Comparaison" permet de:
- Identifier quelle catégorie génère le plus d'intérêt
- Détecter les changements de comportement des consommateurs
- Optimiser l'allocation de budget marketing

### Cas d'usage 3: Découvrir des opportunités

L'onglet "Top Keywords" révèle:
- Quels produits spécifiques sont en forte demande
- Mots-clés avec pics récents (opportunités immédiates)
- Comparaison entre produits similaires

## 📊 Données Collectées

- **Source**: Google Trends
- **Région**: Québec (CA-QC)
- **Langue**: Français
- **Fréquence**: Données hebdomadaires sur 12 mois
- **Métrique**: Intérêt relatif (0-100)

### Interprétation des valeurs

- **100**: Pic de popularité pour le terme
- **50**: Popularité moyenne (moitié du pic)
- **0**: Pas assez de données pour ce terme/période

## 🛠️ Technologies Utilisées

- **Python 3.8+**: Langage principal
- **pytrends**: Wrapper Google Trends API
- **Streamlit**: Framework dashboard interactif
- **Plotly**: Graphiques interactifs
- **Pandas**: Manipulation de données
- **SQLite**: Base de données locale
- **PyYAML**: Configuration

## 🎯 Prochaines Étapes (Phase 2)

- [ ] Intégration SEMrush pour données complémentaires
- [ ] Migration vers BigQuery (cloud)
- [ ] Modèle ML pour prédictions
- [ ] API REST pour intégration externe
- [ ] Alertes automatiques sur tendances émergentes
- [ ] Dashboard avancé avec plus de métriques

## 📝 Documentation Complète

- **[INSTALLATION.md](INSTALLATION.md)**: Guide d'installation détaillé
- **[USAGE.md](USAGE.md)**: Guide d'utilisation complet
- **[CLAUDE.md](../CLAUDE.md)**: Documentation de référence du projet

## 🐛 Résolution de Problèmes

### Erreur lors de la collecte

**Symptôme**: `TooManyRequestsError`

**Solution**: Google Trends limite les requêtes. Attendez 1 heure et réessayez.

### Dashboard ne se lance pas

**Symptôme**: `ModuleNotFoundError`

**Solution**: Vérifiez que l'environnement virtuel est activé et que les dépendances sont installées.

```bash
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

### Pas de données dans le dashboard

**Symptôme**: Message "Aucune donnée dans la base"

**Solution**: Lancez d'abord la collecte:
```bash
python run_collection.py
```

## 📞 Support

- **GitHub Issues**: [Signaler un problème](https://github.com/fil04331/claude-code-assist/issues)
- **Documentation**: Consultez les fichiers dans `docs/`
- **Logs**: Vérifiez `logs/trends_collector.log` pour les détails

## 📜 Licence

Ce projet est un MVP développé en collaboration avec Claude Code.

---

**Développé avec ❤️ pour le marché québécois**

*Dernière mise à jour: 2025-10-22*
