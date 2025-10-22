# CLAUDE.md - Projet de Marketing Prédictif Québécois

## Vue d'ensemble du projet

**Objectif:** Développer un système d'analyse de tendances et de machine learning pour prédire la demande des consommateurs au Québec en temps réel.

**Vision:** Permettre aux entreprises d'offrir au bon moment ce qui est en demande immédiate sur le marché québécois.

## Architecture du Système

### Composantes principales
1. **Collecte de données** - APIs multiples (Google Trends, SEMrush, Ahrefs/Moz)
2. **Stockage centralisé** - Base de données (BigQuery ou alternative)
3. **Traitement et analyse** - Pipeline de données
4. **Visualisation** - Dashboard interactif
5. **Machine Learning** - Modèle prédictif de tendances
6. **Automatisation** - Pipelines automatisés pour mise à jour continue

## Sources de Données

| Plateforme | Avantages | Limitations | Coût |
|------------|-----------|-------------|------|
| Google Trends | Gratuit, données régionales | Moins précis pour niches | Gratuit |
| SEMrush | Détails par localisation | Coût élevé | ~100-200 USD/mois |
| Ahrefs/Moz | Bonnes données SEO | Nécessite abonnement | ~100-200 USD/mois |
| GCP/Vertex AI | ML avancé | Coûts variables | Variable selon usage |

## Tâches où Claude peut vous faire gagner du temps

### 1. Architecture et Design (PRIORITÉ HAUTE)
- [x] Conception détaillée de l'architecture du système
- [x] Schéma de base de données optimisé
- [ ] Diagrammes de flux de données
- [x] Choix technologiques justifiés (frameworks, langages, outils)

### 2. Développement Initial (MVP) ✅ COMPLÉTÉ
- [x] Scripts Python pour extraction Google Trends API
- [x] Pipeline de collecte de données automatisé
- [x] Schéma de base de données et scripts de création
- [x] Prototype de dashboard de visualisation
- [x] Tests unitaires et validation des données

### 3. Machine Learning
- [ ] Preprocessing et nettoyage des données
- [ ] Feature engineering pour modèle prédictif
- [ ] Modèle baseline (simple) pour prédictions
- [ ] Évaluation et métriques de performance
- [ ] Documentation du modèle

### 4. Optimisation des coûts
- [ ] Stratégies pour minimiser coûts GCP
- [ ] Alternatives open-source aux outils payants
- [ ] Plan de scalabilité progressive

### 5. Documentation ✅ COMPLÉTÉ
- [x] Documentation technique complète
- [x] Guide d'installation et déploiement
- [ ] Documentation API (Phase 2)
- [x] Exemples d'utilisation

## 🎉 Accomplissements Phase 1 (COMPLÉTÉ - 2025-10-22)

### ✅ Ce qui a été livré

**Infrastructure complète:**
- ✅ Structure projet Python professionnelle
- ✅ Base de données SQLite avec schéma optimisé
- ✅ Configuration YAML flexible et extensible
- ✅ Scripts d'installation automatisés (Linux/Mac/Windows)

**Collecte de données:**
- ✅ Collecteur Google Trends fonctionnel pour 25 mots-clés
- ✅ 4 catégories de marché: meubles, électroménagers, matelas, couvre-planchers
- ✅ Historique de 12 mois par défaut
- ✅ Rate limiting et gestion d'erreurs robuste
- ✅ Logging complet des opérations

**Dashboard interactif:**
- ✅ Application Streamlit avec 4 onglets de visualisation
- ✅ Graphiques temporels interactifs (Plotly)
- ✅ Comparaison entre catégories
- ✅ Classement des top keywords
- ✅ Export CSV des données
- ✅ Collecte de données depuis l'interface

**Documentation:**
- ✅ Guide d'installation détaillé (docs/INSTALLATION.md)
- ✅ Guide d'utilisation complet (docs/USAGE.md)
- ✅ Documentation MVP (docs/README_MVP.md)
- ✅ Quick Start Guide (QUICKSTART.md)
- ✅ Tests unitaires pour la base de données

**Fichiers utilitaires:**
- ✅ `run_collection.py` - Collecte simple
- ✅ `run_dashboard.py` - Lancement dashboard
- ✅ `check_setup.py` - Vérification installation
- ✅ `setup.sh` & `setup.bat` - Installation automatisée

### 📊 Résultat

Un MVP complètement fonctionnel et prêt à l'emploi en 5 minutes d'installation!

## Par où commencer? (Recommandations)

### Phase 1: MVP avec Google Trends ✅ COMPLÉTÉ
**Durée réelle:** Environ 2 heures avec Claude Code
**Pourquoi:** Gratuit, permet de valider le concept rapidement

1. **Setup initial**
   - Structure du projet Python
   - Configuration environnement virtuel
   - Dépendances de base

2. **Collecte de données**
   - Script d'extraction Google Trends
   - Stockage local (SQLite ou CSV pour commencer)
   - 3-5 mots-clés pilotes pour le Québec

3. **Visualisation basique**
   - Dashboard simple (Streamlit ou Dash)
   - Graphiques de tendances temporelles
   - Comparaisons entre mots-clés

4. **Première analyse**
   - Identification de patterns
   - Validation de la pertinence des données

### Phase 2: Intégration et ML (3-4 semaines)
1. Ajout d'une source payante (SEMrush ou alternative)
2. Migration vers base de données cloud (BigQuery)
3. Développement modèle ML prédictif simple
4. Automatisation de la collecte

### Phase 3: Production et scalabilité (ongoing)
1. Optimisation du modèle ML
2. Dashboard avancé avec prédictions
3. API pour intégration tierce
4. Monitoring et alertes

## Décisions à prendre ensemble

1. **Hébergement:** GCP, AWS, Azure, ou local?
2. **Base de données:** BigQuery, PostgreSQL, MongoDB?
3. **Framework dashboard:** Streamlit, Dash, React custom?
4. **Budget mensuel:** Quel est le budget acceptable pour les APIs et cloud?
5. **Secteurs cibles:** Quels secteurs commerciaux prioriser au Québec?

## Structure de ce dépôt

```
claude-code-assist/
├── CLAUDE.md                     # Ce fichier - documentation de référence
├── QUICKSTART.md                 # ✅ Guide démarrage rapide (5 min)
├── README.md                     # Description du dépôt
├── .env.example                  # ✅ Template variables d'environnement
├── .gitignore                    # ✅ Configuration git
├── requirements.txt              # ✅ Dépendances Python
├── setup.sh / setup.bat          # ✅ Scripts d'installation automatisés
├── run_collection.py             # ✅ Script de collecte de données
├── run_dashboard.py              # ✅ Script de lancement du dashboard
├── check_setup.py                # ✅ Vérification de l'installation
├── config/
│   └── config.yaml               # ✅ Configuration complète (keywords, settings)
├── docs/                         # ✅ Documentation complète
│   ├── INSTALLATION.md           # ✅ Guide d'installation détaillé
│   ├── USAGE.md                  # ✅ Guide d'utilisation complet
│   └── README_MVP.md             # ✅ Documentation MVP
├── src/                          # ✅ Code source
│   ├── data_collection/          # ✅ Scripts de collecte
│   │   ├── database.py           # ✅ Gestionnaire SQLite
│   │   └── trends_collector.py  # ✅ Collecteur Google Trends
│   ├── dashboard/                # ✅ Application de visualisation
│   │   └── app.py                # ✅ Dashboard Streamlit
│   ├── preprocessing/            # Pour Phase 2
│   └── models/                   # Pour Phase 2
├── tests/                        # ✅ Tests unitaires
│   └── test_database.py          # ✅ Tests de la base de données
├── data/                         # Créé automatiquement
│   ├── trends.db                 # Base de données SQLite
│   └── backups/                  # Sauvegardes
├── logs/                         # Créé automatiquement
│   └── trends_collector.log      # Logs de collecte
└── notebooks/                    # Pour exploration future (Phase 2)
```

## Prochaines étapes - Phase 2

**Maintenant que le MVP fonctionne, décidons:**
1. ✅ Tester le MVP avec les données réelles pendant 1-2 semaines
2. 🔄 Identifier les insights intéressants pour le marché québécois
3. 📊 Décider si on ajoute SEMrush ou autre source payante
4. 🤖 Commencer le développement du modèle ML prédictif
5. ☁️ Évaluer si migration vers cloud (BigQuery) est nécessaire

**Phase 2 peut inclure:**
- Modèle ML pour prédire les tendances futures
- Détection automatique de tendances émergentes
- Alertes par email sur changements significatifs
- API REST pour intégration externe
- Dashboard plus avancé avec prédictions
- Intégration données SEMrush/Ahrefs

## Notes importantes

- Ce dépôt reste un **terrain de développement malléable**
- Utilisé pour prototypage rapide et documentation
- Qualité > Vitesse (mais Claude Code permet les deux!)
- Toujours poser des questions si quelque chose n'est pas clair

---

**Dernière mise à jour:** 2025-10-22
**Status:** ✅ Phase 1 MVP Complété et Fonctionnel
**Prochaine étape:** Tester avec données réelles et planifier Phase 2
