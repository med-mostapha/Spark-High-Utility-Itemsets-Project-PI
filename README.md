# Développement d'un Algorithme Distribué pour la Découverte de High-Utility Itemsets (HUIM) sur Spark

Ce projet universitaire consiste à concevoir et implémenter un algorithme distribué hautement performant sur **Apache Spark** (via **PySpark**) pour extraire les ensembles d'articles à forte utilité (High-Utility Itemsets) à partir de grandes masses de données (Big Data).

---

## 💡 1. Résumé de la Conception (Core Concepts)

Contrairement au Pattern Mining traditionnel (comme Apriori) qui ne prend en compte que la fréquence, le **HUIM** intègre la notion de profit et de quantité (Utility).

### Le Pipeline de l'Algorithme

1. **Global Pruning (Filtre TWU)** — Premier scan parallèle pour calculer le _Transaction-Weighted Utilization_ (TWU) de chaque article. Élimination immédiate des articles dont le `TWU < MinUtil`.
2. **Construction des Utility-Lists** — Structuration des données restantes dans les Workers sous forme de listes d'utilité (`TID`, `iutil`, `rutil`).
3. **Distributed Mining (DFS)** — Exploration locale et parallèle par chaque Worker via un algorithme de recherche en profondeur (Depth-First Search) avec élagage intelligent pour éviter l'explosion combinatoire.
4. **Aggregation** — Collecte et sauvegarde des High-Utility Itemsets finaux.

---

## 🏗️ 2. Architecture du Projet (Clean Architecture)

Pour éviter le "Spaghetti Code" et travailler proprement en équipe, le code est structuré selon les principes de la Clean Architecture :

```
📂 src
┣ 📂 main
┃  ┣ 📂 domain                       # Noyau : Modèles mathématiques purs et structures de base
┃  ┃ ┣ 📜 __init__.py
┃  ┃ ┣ 📜 models.py                  # Classes fondamentales (Item, Transaction, UtilityList)
┃  ┃ ┗ 📜 math_ops.py                # Opérations mathématiques pures (calcul de l'utilité élémentaire)
┃  ┃
┃  ┣ 📂 core                         # Logique métier : algorithmes distribués de filtrage et de mining
┃  ┃ ┣ 📜 __init__.py
┃  ┃ ┣ 📜 twu_filter.py              # Réduction globale et filtrage initial (Global Pruning via TWU)
┃  ┃ ┣ 📜 utility_list_builder.py    # Construction parallèle des Utility-Lists
┃  ┃ ┗ 📜 hui_miner.py               # Algorithme d'extraction locale (DFS) exécuté sur les Workers Spark
┃  ┃
┃  ┣ 📂 infrastructure               # Adaptateurs : configuration Spark et gestion des E/S
┃  ┃ ┣ 📜 __init__.py
┃  ┃ ┣ 📜 spark_config.py            # Initialisation et optimisation de la SparkSession / du Cluster
┃  ┃ ┣ 📜 data_loader.py             # Chargement des fichiers (SPMF, CSV, Excel) → RDDs/DataFrames
┃  ┃ ┗ 📜 result_storage.py          # Persistance des High-Utility Itemsets extraits
┃  ┃
┃  ┗ 📜 main.py                      # Orchestrateur (Driver) : point d'entrée du pipeline Spark
┃
┗ 📂 tests                           # Tests unitaires de validation
  ┣ 📂 domain
  ┃ ┗ 📜 test_math_ops.py            # Validation des opérations mathématiques
  ┣ 📂 core
  ┃ ┣ 📜 test_twu_filter.py          # Validation de l'étape de réduction globale (TWU)
  ┃ ┣ 📜 test_utility_list_builder.py # Validation de la construction des listes
  ┃ ┗ 📜 test_hui_miner.py           # Validation de l'exactitude de l'extraction DFS
  ┗ 📂 infrastructure
    ┗ 📜 test_data_loader.py         # Validation du chargement distribué Spark
```

---

## 🛠️ 3. Installation et Configuration Rapide

**Prérequis :** Python 3.12+ et Java (OpenJDK 17 ou 11) installés (requis pour Apache Spark).

**1 — Activer l'environnement virtuel :**

```bash
source .venv-pi/bin/activate
```

**2 — Installer les dépendances :**

```bash
pip install -r requirements.txt
```

---

## 📋 4. TODO List / Workflow

- [x] Initialisation du Git et branche `feature/setup`
- [x] Configuration de l'environnement virtuel (`.venv-pi`)
- [x] Rédaction du README.md et architecture cible
- [x] Création du fichier `requirements.txt` (dépendances Spark)
- [x] Implémentation de la couche `domain/models.py`
- [x] Implémentation du chargeur de données `infrastructure/data_loader.py`
- [x] Implémentation du filtre de réduction `core/twu_filter.py`
- [x] Implémentation du cœur distribué `core/hui_miner.py`
- [x] Tests et validation de l'exactitude mathématique (10/10 passed)
- [x] Tests de montée en charge sur un volume de données plus important (1001 lignes)

---

## 🚀 5. How to Run (Guide pour les Amis)

### Run Unit Tests

Vérifier que toute l'architecture distribuée et locale fonctionne sans bug :

```bash
pytest
```

### Run the Pipeline Execution

**Exécution standard (petit jeu de données) :**

```bash
PYTHONPATH=. python3 src/main/main.py
```

**Avec un fichier de données et un seuil personnalisé :**

```bash
PYTHONPATH=. python3 src/main/main.py src/tests/infrastructure/sample.txt 2000.0
```

### Exemple de résultat (1001 lignes / MinUtil = 2000.0)

```
=========================================
🎉 SUCCESS: Extracted 10 High-Utility Itemsets (HUIs)
=========================================
Itemset: [9]  ---> Utility: 2914.9
Itemset: [3]  ---> Utility: 3059.5
Itemset: [10] ---> Utility: 2948.3
Itemset: [6]  ---> Utility: 2771.3
Itemset: [5]  ---> Utility: 2758.0
Itemset: [8]  ---> Utility: 2786.2
Itemset: [1]  ---> Utility: 2987.3
Itemset: [2]  ---> Utility: 3011.6
Itemset: [4]  ---> Utility: 3058.8
Itemset: [7]  ---> Utility: 3434.5
=========================================
```

---

## 📦 6. Stack Technique

| Composant        | Technologie                                         |
| ---------------- | --------------------------------------------------- |
| Langage          | Python 3.12+                                        |
| Moteur distribué | Apache Spark (PySpark)                              |
| Runtime requis   | Java (OpenJDK 11 ou 17)                             |
| Tests            | pytest                                              |
| Architecture     | Clean Architecture (domain / core / infrastructure) |

---

## 📄 7. Licence

_À compléter selon le choix de l'équipe (MIT, GPL, usage académique uniquement, etc.)_
