# Guide d'Installation - MVP Analyse de Tendances Québec

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour cloner le dépôt)

## Installation Étape par Étape

### 1. Cloner le dépôt

```bash
git clone https://github.com/fil04331/claude-code-assist.git
cd claude-code-assist
```

### 2. Créer un environnement virtuel

**Sur Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Sur Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Créer les dossiers nécessaires

```bash
mkdir -p data logs data/backups
```

### 5. Configuration (Optionnel)

Copier le fichier d'environnement exemple:
```bash
cp .env.example .env
```

Vous pouvez modifier `config/config.yaml` pour:
- Ajouter/retirer des mots-clés
- Changer la période de collecte
- Ajuster les paramètres du dashboard

## Vérification de l'installation

Vérifier que tous les modules sont installés correctement:

```bash
python -c "import streamlit, pandas, plotly, pytrends; print('✓ All modules installed successfully!')"
```

## Prochaines étapes

Une fois l'installation terminée, consultez [USAGE.md](USAGE.md) pour apprendre à utiliser le système.

## Résolution de problèmes

### Erreur: `pytrends` ne s'installe pas

Essayez d'installer manuellement:
```bash
pip install pytrends==4.9.2
```

### Erreur: Permission denied lors de l'installation

Utilisez l'option `--user`:
```bash
pip install --user -r requirements.txt
```

### Erreur: Python version incorrecte

Vérifiez votre version:
```bash
python --version
```

Si nécessaire, utilisez `python3` au lieu de `python`.

## Support

Pour toute question ou problème, ouvrez une issue sur GitHub ou consultez la documentation complète.
