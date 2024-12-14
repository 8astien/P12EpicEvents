# Epic Events CRM

Epic Events CRM est une application en ligne de commande développée pour gérer les relations clients de l'entreprise Epic Events. Cet outil permet de simplifier la gestion des clients, des contrats et des événements tout en facilitant la communication et la collaboration entre les différents départements (Commercial, Gestion et Support).

---

## Table des matières
- [Prérequis](#prérequis)
- [Installation](#installation)
  - [Environnement virtuel](#environnement-virtuel)
  - [Configuration de la base de données](#configuration-de-la-base-de-données)
  - [Fichier .env](#fichier-env)
- [Lancer l'application](#lancer-lapplication)

---

## Prérequis

- Python 3.9 ou version supérieure
- Base de données MySQL

---

## Installation

### Environnement virtuel

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/8astien/P12EpicEvents
   cd EpicEvents
   ```

2. Créez un environnement virtuel :
   ```bash
   python3 -m venv venv
   ```

3. Activez l'environnement virtuel :
   - **Linux/macOS :**
     ```bash
     source venv/bin/activate
     ```
   - **Windows :**
     ```bash
     venv\Scripts\activate
     ```

4. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

### Configuration de la base de données

1. Créez une base de données MySQL :
   ```sql
   CREATE DATABASE epic_events;
   USE epic_events;
   ```

2. Exécutez le script `database.sql` pour créer les tables nécessaires :
   ```bash
   mysql -u <utilisateur> -p epic_events < database.sql
   ```

3. (Optionnel) Remplissez la base avec des données de test :
   ```bash
   mysql -u <utilisateur> -p epic_events < dummy_data.sql
   ```

---

### Fichier .env

Pour sécuriser les informations sensibles, l'application utilise un fichier `.env` pour stocker les configurations comme l'URL de connexion à la base de données et d'autres variables sensibles.

1. Créez un fichier `.env` à la racine du projet :
   ```bash
   touch .env
   ```

2. Ajoutez les variables suivantes dans le fichier `.env` :
   ```env
   DATABASE_URL=mysql://<utilisateur>:<motdepasse>@localhost:3306/epic_events
   SENTRY_DSN=https://<votre_dsn_sentry>
   ```

   - Remplacez `<utilisateur>` et `<motdepasse>` par vos identifiants MySQL.
   - Si vous n'utilisez pas Sentry, vous pouvez laisser la variable `SENTRY_DSN` vide.

3. Assurez-vous que le fichier `.env` est ignoré par Git en vérifiant qu'il est listé dans le fichier `.gitignore`.

   ```bash
   echo ".env" >> .gitignore
   ```

---

## Lancer l'application

1. Assurez-vous que la base de données est en cours d'exécution.
2. Activez l'environnement virtuel :
   ```bash
   source venv/bin/activate
   ```
3. Lancez l'application :
   ```bash
   python main.py
   ```

---
