# Guide d'Utilisation - MVP Analyse de Tendances Québec

## Démarrage Rapide

### 1. Collecte des données initiale

Avant d'utiliser le dashboard, vous devez collecter des données Google Trends:

```bash
python run_collection.py
```

Cette première collecte prendra environ **5-10 minutes** et récupérera 12 mois de données historiques pour tous les mots-clés configurés.

**Sortie attendue:**
```
=========================================================
Quebec Market Trends - Data Collection
=========================================================

Initializing collector...
✓ Collector initialized

Starting data collection...
This may take several minutes depending on the number of keywords.

[...]

Collection Complete!
=========================================================
Categories processed: 4
Total keywords: 25
Successful: 25
Records inserted: 9,000
Duration: 356.42 seconds
```

### 2. Lancer le dashboard

Une fois les données collectées, lancez le dashboard:

```bash
python run_dashboard.py
```

Ou directement avec Streamlit:

```bash
streamlit run src/dashboard/app.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse: **http://localhost:8501**

## Utilisation du Dashboard

### Interface principale

Le dashboard est divisé en 4 onglets:

#### 📈 Tendances
- **Vue détaillée par catégorie**: Sélectionnez une catégorie (meubles, électroménagers, etc.) pour voir l'évolution de tous les mots-clés au fil du temps
- **Graphiques interactifs**: Survolez les lignes pour voir les valeurs exactes
- **Métriques**: Intérêt moyen, pic d'intérêt, nombre de mots-clés suivis

#### 🔥 Top Keywords
- **Classement par catégorie**: Voir les mots-clés les plus populaires
- **Comparaison moyenne vs maximum**: Identifier les mots-clés avec les pics les plus élevés
- **Tableaux détaillés**: Données précises pour chaque mot-clé

#### 📊 Comparaison
- **Comparaison entre catégories**: Voir quelle catégorie génère le plus d'intérêt
- **Tendances 30 jours**: Variation récente de l'intérêt par catégorie
- **Statistiques agrégées**: Vue d'ensemble du marché

#### 📋 Données
- **Table complète**: Accès à toutes les données brutes
- **Export CSV**: Télécharger les données pour analyse externe
- **Filtrage et tri**: Organiser les données selon vos besoins

### Barre latérale

#### Collecte de données
- **Bouton "Collecter nouvelles données"**: Lance une nouvelle collecte (mettre à jour les données)
- Utilisez-le quotidiennement ou hebdomadairement pour garder vos données à jour

#### Statistiques
- Vue rapide sur l'état de votre base de données
- Date de la dernière collecte
- Nombre total d'enregistrements

#### Filtres
- **Catégories**: Sélectionnez quelles catégories afficher
- **Période**: Choisissez la plage temporelle (7 jours à 1 an)

## Utilisation Avancée

### Collecte programmatique

Utiliser Python directement pour plus de contrôle:

```python
from src.data_collection.trends_collector import QuebecTrendsCollector

# Initialiser le collecteur
collector = QuebecTrendsCollector()

# Collecter une catégorie spécifique
stats = collector.collect_category('meubles')

# Ou toutes les catégories
all_stats = collector.collect_all_categories()

# Mettre à jour seulement les données anciennes (>1 jour)
update_stats = collector.update_stale_data(days_threshold=1)
```

### Accès direct à la base de données

```python
from src.data_collection.database import TrendsDatabase

# Ouvrir la base de données
db = TrendsDatabase()

# Récupérer des données spécifiques
data = db.get_trends_data(
    keywords=['matelas québec', 'canapé'],
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# Obtenir tous les mots-clés
all_keywords = db.get_all_keywords()

# Statistiques
stats = db.get_summary_stats()
```

### Automatisation avec cron (Linux/Mac)

Pour collecter automatiquement des données chaque jour:

```bash
# Ouvrir crontab
crontab -e

# Ajouter cette ligne pour exécution quotidienne à 2h du matin
0 2 * * * cd /chemin/vers/claude-code-assist && /chemin/vers/venv/bin/python run_collection.py >> logs/cron.log 2>&1
```

### Automatisation avec Task Scheduler (Windows)

1. Ouvrir le Planificateur de tâches
2. Créer une tâche basique
3. Déclencheur: Quotidien à l'heure souhaitée
4. Action: Démarrer un programme
   - Programme: `C:\chemin\vers\venv\Scripts\python.exe`
   - Arguments: `run_collection.py`
   - Dossier: `C:\chemin\vers\claude-code-assist`

## Personnalisation

### Ajouter de nouveaux mots-clés

Éditez `config/config.yaml`:

```yaml
keywords:
  meubles:
    - "meubles québec"
    - "mobilier maison"
    # Ajoutez vos mots-clés ici
    - "nouveau mot-clé"
```

Relancez ensuite la collecte pour obtenir les données du nouveau mot-clé.

### Modifier la période de collecte

Dans `config/config.yaml`:

```yaml
google_trends:
  timeframe: "today 3-m"  # 3 mois au lieu de 12
```

Options disponibles:
- `"today 1-m"` - 1 mois
- `"today 3-m"` - 3 mois
- `"today 12-m"` - 12 mois
- `"today 5-y"` - 5 ans

## Maintenance

### Sauvegarder la base de données

```python
from src.data_collection.database import TrendsDatabase

db = TrendsDatabase()
backup_path = db.backup_database()
print(f"Sauvegarde créée: {backup_path}")
```

Les sauvegardes sont automatiquement créées dans `data/backups/`.

### Nettoyer les logs

```bash
# Supprimer les anciens logs
rm logs/*.log

# Ou garder seulement les plus récents
find logs/ -name "*.log" -mtime +30 -delete
```

## Limites et Bonnes Pratiques

### Limites de Google Trends API

- **Rate limiting**: Google limite le nombre de requêtes. Le système inclut des délais (2 secondes par défaut) entre chaque requête
- **Pas de clé API**: Google Trends ne nécessite pas de clé, mais peut bloquer temporairement en cas d'utilisation excessive
- **Données relatives**: Les valeurs sont sur une échelle de 0-100 (relatif, pas absolu)

### Bonnes pratiques

1. **Collecte régulière**: Collectez des données 1 fois par jour maximum
2. **Patience**: La première collecte est longue, mais les suivantes sont plus rapides
3. **Backup**: Sauvegardez régulièrement votre base de données
4. **Surveillance**: Vérifiez les logs pour détecter les erreurs

## Questions Fréquentes

**Q: Combien de temps prend la première collecte?**
A: 5-10 minutes pour 25 mots-clés sur 12 mois.

**Q: Les données sont-elles en temps réel?**
A: Google Trends a un délai de quelques heures. Les données d'aujourd'hui sont généralement disponibles dans la soirée.

**Q: Puis-je comparer avec d'autres régions?**
A: Oui, modifiez le paramètre `geo` dans `config/config.yaml` (ex: `"CA-ON"` pour Ontario).

**Q: Comment ajouter une nouvelle catégorie?**
A: Ajoutez une section dans `keywords:` dans le fichier config, et ajoutez une couleur dans `visualization.color_scheme`.

**Q: Le dashboard est-il accessible à distance?**
A: Par défaut non. Pour l'accès distant, consultez la documentation Streamlit sur le déploiement.

## Support et Contribution

Pour toute question:
- Consultez les logs dans `logs/trends_collector.log`
- Vérifiez les issues GitHub
- Consultez [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
