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
- [ ] Conception détaillée de l'architecture du système
- [ ] Schéma de base de données optimisé
- [ ] Diagrammes de flux de données
- [ ] Choix technologiques justifiés (frameworks, langages, outils)

### 2. Développement Initial (MVP)
- [ ] Scripts Python pour extraction Google Trends API
- [ ] Pipeline de collecte de données automatisé
- [ ] Schéma de base de données et scripts de création
- [ ] Prototype de dashboard de visualisation
- [ ] Tests unitaires et validation des données

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

### 5. Documentation
- [ ] Documentation technique complète
- [ ] Guide d'installation et déploiement
- [ ] Documentation API
- [ ] Exemples d'utilisation

## Par où commencer? (Recommandations)

### Phase 1: MVP avec Google Trends (2-3 semaines)
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
├── CLAUDE.md              # Ce fichier - documentation de référence
├── README.md              # Description du dépôt
├── docs/                  # Documentation technique (à créer)
├── src/                   # Code source (à créer)
│   ├── data_collection/   # Scripts de collecte
│   ├── preprocessing/     # Nettoyage et transformation
│   ├── models/            # Modèles ML
│   └── dashboard/         # Application de visualisation
├── tests/                 # Tests unitaires (à créer)
├── notebooks/             # Jupyter notebooks pour exploration (à créer)
└── config/                # Fichiers de configuration (à créer)
```

## Prochaines étapes immédiates

**À décider maintenant:**
1. Confirmer la Phase 1 comme point de départ?
2. Quels 3-5 mots-clés/secteurs pilotes voulez-vous cibler?
3. Préférence pour le framework de dashboard?

**Claude peut créer immédiatement:**
- Structure complète du projet Python
- Script de collecte Google Trends fonctionnel
- Dashboard prototype avec visualisations
- Documentation technique

## Notes importantes

- Ce dépôt reste un **terrain de développement malléable**
- Utilisé pour prototypage rapide et documentation
- Qualité > Vitesse (mais Claude Code permet les deux!)
- Toujours poser des questions si quelque chose n'est pas clair

---

**Dernière mise à jour:** 2025-10-22
**Status:** Initialisation du projet
