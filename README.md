# Développement d'un Algorithme Distribué pour la Découverte de High-Utility Itemsets (HUIM) sur Spark

Ce projet universitaire consiste à concevoir et implémenter un algorithme distribué hautement performant sur **Apache Spark** (via **PySpark**) pour extraire les ensembles d'articles à forte utilité (High-Utility Itemsets) à partir de grandes masses de données (Big Data).

---

## 💡 1. Résumé de la Conception (Core Concepts)

Contrairement au Pattern Mining traditionnel (comme Apriori) qui ne prend en compte que la fréquence, le **HUIM** intègre la notion de profit et de quantité (Utility).

### Le Pipeline de l'Algorithme :

1. **Global Pruning (Filtre TWU) :** Premier scan parallèle pour calculer le _Transaction-Weighted Utilization_ (TWU) de chaque article. Élimination immédiate des articles dont le $TWU < MinUtil$.
2. **Construction des Utility-Lists :** Structuration des données restantes dans les Workers sous forme de listes d'utilité ($TID$, $iutil$, $rutil$).
3. **Distributed Mining (DFS) :** Exploration locale et parallèle par chaque Worker via un algorithme de recherche en profondeur (Depth-First Search) avec élagage intelligent pour éviter l'explosion combinatoire.
4. **Aggregation :** Collecte et sauvegarde des High-Utility Itemsets finaux.

---

## 🏗️ 2. Architecture Propre du Projet (Clean Architecture)

Pour éviter le "Spaghetti Code" et bosser proprement en équipe, le code est structuré selon les principes de la Clean Architecture :

```text
📂 src
┣ 📦 main
┃  ┣ 📂 domain                 # Noyau : Modèles mathématiques purs et structures de base
┃  ┃ ┣ 📜 __init__.py
┃  ┃ ┣ 📜 models.py            # Définition des classes fondamentales (Item, Transaction, UtilityList)
┃  ┃ ┗ 📜 math_ops.py          # Opérations mathématiques pures (calcul de l'utilité élémentaire)
┃  ┃
┃  ┣ 📂 core                   # Logique métier : Algorithmes distribués de filtrage et de Mining
┃  ┃ ┣ 📜 __init__.py
┃  ┃ ┣ 📜 twu_filter.py        # Étape de réduction globale et filtrage initial (Global Pruning via TWU)
┃  ┃ ┣ 📜 utility_list_builder.py # Construction parallèle des structures complexes (Utility-Lists)
┃  ┃ ┗ 📜 hui_miner.py         # Algorithme d'extraction locale (DFS) exécuté sur les Workers Spark
┃  ┃
┃  ┣ 📂 infrastructure         # Adaptateurs : Configuration Spark et gestion des Entrées/Sorties
┃  ┃ ┣ 📜 __init__.py
┃  ┃ ┣ 📜 spark_config.py      # Initialisation et optimisation de la SparkSession et du Cluster
┃  ┃ ┣ 📜 data_loader.py       # Chargement des fichiers (SPMF, CSV, Excel) et conversion en RDDs/DataFrames
┃  ┃ ┗ 📜 result_storage.py    # Persistance et sauvegarde des High-Utility Itemsets extraits
┃  ┃
┃  ┗ 📜 main.py                # Orchestrateur (Driver) : Point d'entrée principal du pipeline Spark
┃
┣ 📂 tests                  # Test
┃ ┣ 📜 __init__.py
┃ ┣ 📂 domain
┃ ┃ ┗ 📜 test_math_ops.py   # Test Opérations mathématiques
┃ ┗ 📂 core
┃   ┗ 📜 test_twu_filter.py # Test Étape de réduction globale
```

## 🛠️ 3. Installation et Configuration Rapide

Pour les membres de l'équipe (Friends) :

1 - Activer l'environnement virtuel :

```text
source .venv-pi/bin/activate
```

2 - Installer les dépendances (À venir) :

```text
pip install -r requirements.txt
```

## 📋 4. TODO List / Workflow Étape par Étape

[x] Initialisation du Git et Branche feature/setup

[x] Configuration de l'environnement virtuel (.venv-pi)

[x] Rédaction du README.md et Architecture cible

[ ] Création du fichier requirements.txt (Dépendances Spark)

[ ] Implémentation de la couche domain/models.py

[ ] Implémentation du chargeur de données infrastructure/data_loader.py

[ ] Implémentation du filtre de réduction core/twu_filter.py

[ ] Implémentation du cœur distribué core/hui_miner.py

[ ] Tests de montée en charge (Scalability) sur gros volumes de données

📦 Root
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
┃
