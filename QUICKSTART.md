# 🚀 Démarrage Rapide - MVP Analyse Tendances Québec

## Installation Express (5 minutes)

```bash
# 1. Cloner le projet
git clone https://github.com/fil04331/claude-code-assist.git
cd claude-code-assist

# 2. Installer
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OU: venv\Scripts\activate  # Windows

pip install -r requirements.txt
mkdir -p data logs data/backups

# 3. Collecter les données (première fois: 5-10 min)
python run_collection.py

# 4. Lancer le dashboard
python run_dashboard.py
```

Ouvrez votre navigateur: **http://localhost:8501**

## Utilisation Quotidienne

```bash
# Activer l'environnement
source venv/bin/activate

# Mettre à jour les données
python run_collection.py

# Voir le dashboard
python run_dashboard.py
```

## Configuration Rapide

**Ajouter des mots-clés:**
Éditez `config/config.yaml`

**Changer la période:**
Modifiez `timeframe` dans `config/config.yaml`

## Documentation Complète

📚 **[Guide complet dans docs/README_MVP.md](docs/README_MVP.md)**

## Problèmes?

- ❌ **Erreur de module**: `pip install -r requirements.txt`
- ❌ **Pas de données**: Lancez d'abord `python run_collection.py`
- ❌ **Too many requests**: Attendez 1 heure, Google Trends a des limites

---

✨ **Développé avec Claude Code pour le marché québécois**
