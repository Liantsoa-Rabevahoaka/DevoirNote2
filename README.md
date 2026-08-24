Oui, dans ce cas je te conseille clairement **un seul `README.md` à la racine**. C'est beaucoup plus propre pour un dépôt GitHub destiné à être consulté par un professeur : il ouvre le dépôt et comprend immédiatement **le contexte, les deux exercices, l'installation, l'exécution et les résultats attendus**, sans devoir naviguer dans deux README différents.

J'ai aussi corrigé quelques formulations techniques, notamment autour de HMAC : `hmac` est un module Python séparé de `hashlib`, et SHA-3 est présenté comme une famille distincte de SHA-2, même si les deux sont des fonctions de hachage cryptographiques.

Voici une version plus "projet universitaire sérieux + GitHub wow" :

# 🔐 Devoir Note 2 — HMAC, SHA-256 & SHA-3

> **Sécurité, authentification et comparaison des fonctions de hachage cryptographiques**

Ce dépôt présente une étude pratique de plusieurs mécanismes cryptographiques utilisés dans la **gestion d'identité et la protection des données**.

Le devoir est organisé en **deux exercices complémentaires** :

* 🔑 **Exercice 1 — HMAC & effet avalanche**
* 🧬 **Exercice 2 — SHA-256 vs SHA-3-256 (Keccak)**

L'objectif est non seulement de calculer des empreintes cryptographiques, mais également de **mesurer leurs performances, comparer leurs comportements et visualiser les résultats expérimentalement**.

---

## 📚 Sommaire

* [🎯 Objectifs](#-objectifs)
* [📂 Structure du projet](#-structure-du-projet)
* [🛠️ Technologies utilisées](#️-technologies-utilisées)
* [⚙️ Installation](#️-installation)
* [🔑 Exercice 1 — HMAC & SHA-3](#-exercice-1--hmac--sha-3)
* [🧬 Exercice 2 — SHA-256 & SHA-3](#-exercice-2--sha-256--sha-3)
* [▶️ Exécution](#️-exécution)
* [📊 Résultats attendus](#-résultats-attendus)
* [🧹 Fichiers générés](#-fichiers-générés)
* [🛡️ Sécurité](#️-sécurité)
* [🎓 Objectifs pédagogiques](#-objectifs-pédagogiques)
* [🏁 Conclusion](#-conclusion)

---

# 🎯 Objectifs

Ce devoir vise à mettre en pratique plusieurs notions fondamentales de la cryptographie moderne :

### 🔐 Authentification

Comprendre le fonctionnement d'un **HMAC (Hash-based Message Authentication Code)** et son rôle dans l'authentification et l'intégrité des messages.

### 🧮 Hachage cryptographique

Étudier et comparer :

* **SHA-256**
* **SHA-3-256**
* ainsi que les fonctions utilisées dans les expériences HMAC.

### ⚡ Analyse des performances

Mesurer le temps nécessaire au traitement de données de tailles différentes afin d'observer l'évolution des performances.

### 🌪️ Effet avalanche

Mettre en évidence une propriété fondamentale des fonctions de hachage cryptographiques : **une modification minime de l'entrée doit provoquer une modification importante de l'empreinte produite**.

### 📊 Analyse expérimentale

Présenter les résultats sous forme :

* 📈 de courbes ;
* 📋 de tableaux ;
* 🔎 de comparaisons entre algorithmes.

---

# 📂 Structure du projet

Le dépôt est organisé de manière à séparer clairement les deux exercices :

```text
DevoirNote2/
│
├── 📁 Exo1_HMAC/
│   └── 🐍 hmac_exo.py
│
├── 📁 Exo2_SHA/
│   └── 🐍 sha_exo.py
│
├── 📄 README.md
└── 📄 .gitignore
```

Les fichiers générés pendant l'exécution sont volontairement exclus du dépôt afin de garder une structure propre.

---

# 🛠️ Technologies utilisées

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Cryptography](https://img.shields.io/badge/Cryptography-HMAC%20%7C%20SHA--256%20%7C%20SHA--3-8A2BE2?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge\&logo=matplotlib\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge\&logo=pandas\&logoColor=white)

</div>

### Bibliothèques Python

| Bibliothèque | Utilisation                              |
| ------------ | ---------------------------------------- |
| `hashlib`    | SHA-256 et SHA-3-256                     |
| `hmac`       | Génération de codes HMAC                 |
| `matplotlib` | Courbes et visualisations                |
| `pandas`     | Manipulation et présentation des données |
| `tabulate`   | Affichage des tableaux dans le terminal  |

Les modules **`hashlib`** et **`hmac`** font partie de la bibliothèque standard de Python.

---

# ⚙️ Installation

## 1️⃣ Se placer dans le projet

```bash
cd ~/ESTI/ESTI/M1/SIA_803_2026_GestionIdentité/code/DevoirNote2
```

## 2️⃣ Créer un environnement virtuel

Si celui-ci n'existe pas encore :

```bash
python3 -m venv venv
```

## 3️⃣ Activer l'environnement virtuel

Sous Linux / macOS :

```bash
source venv/bin/activate
```

Sous Windows :

```powershell
venv\Scripts\activate
```

## 4️⃣ Installer les dépendances

```bash
pip install matplotlib pandas tabulate
```

---

# 🔑 Exercice 1 — HMAC & effet avalanche

📁 Répertoire : `Exo1_HMAC/`

🐍 Script : `hmac_exo.py`

Cet exercice se concentre sur le **HMAC**, l'intégrité des données et l'effet avalanche des fonctions de hachage.

---

## 1️⃣ HMAC avec une clé secrète

Le programme calcule un HMAC à partir :

* d'un message ;
* d'une clé secrète ;
* d'une fonction de hachage.

Le mécanisme utilisé est basé sur **HMAC-SHA256**.

Conceptuellement :

```text
        Message
           │
           ▼
    ┌─────────────┐
    │   HMAC      │
    │   SHA-256   │ ◄──── Clé secrète
    └─────────────┘
           │
           ▼
     Empreinte HMAC
```

Contrairement à un simple hash, le HMAC utilise une **clé secrète**.

Cela permet notamment de vérifier qu'un message :

* n'a pas été modifié ;
* provient d'une entité possédant la clé secrète.

---

## 2️⃣ Comparaison avec un simple hachage

Le programme illustre également la différence entre :

```text
Hash(message)
```

et :

```text
HMAC(message, clé)
```

Un simple hash ne nécessite aucune clé secrète.

Le HMAC, lui, repose sur une clé connue uniquement des parties autorisées.

Cette comparaison permet de comprendre pourquoi **un hash seul ne constitue pas un mécanisme d'authentification**.

---

## 3️⃣ 📈 Performance du HMAC

Le programme génère des données aléatoires de tailles différentes et mesure le temps nécessaire pour calculer leur HMAC-SHA256.

Les résultats sont ensuite représentés graphiquement :

```text
Temps
  │
  │                    ●
  │               ●
  │          ●
  │      ●
  │  ●
  └──────────────────────────►
          Taille des données
```

L'objectif est d'observer l'évolution du coût de calcul lorsque la quantité de données augmente.

---

## 4️⃣ 📋 HMAC de fichiers

Le programme génère plusieurs fichiers d'échantillonnage dans :

```text
echantillons_hmac/
```

Pour chaque fichier, son HMAC est calculé puis présenté dans un tableau contenant notamment :

| Fichier         | Taille | HMAC-SHA256 |
| --------------- | -----: | ----------- |
| `fichier_1.bin` |   … Ko | `…`         |
| `fichier_2.bin` |   … Ko | `…`         |
| `fichier_3.bin` |   … Ko | `…`         |

Cela permet d'observer concrètement l'utilisation d'un HMAC sur des fichiers plutôt que sur un simple message.

---

# 🌪️ 5️⃣ Effet avalanche

L'effet avalanche est étudié en comparant deux messages presque identiques :

```text
bonjour
Bonjour
```

Une seule lettre change :

```text
b → B
```

Pourtant, les empreintes obtenues doivent être **très différentes**.

Conceptuellement :

```text
"bonjour"
    │
    ▼
████████████████████████████████

"Bonjour"
    │
    ▼
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

Cette propriété est essentielle à la sécurité des fonctions de hachage cryptographiques.

---

# 🧬 Exercice 2 — SHA-256 & SHA-3

📁 Répertoire : `Exo2_SHA/`

🐍 Script : `sha_exo.py`

Le deuxième exercice compare deux fonctions de hachage cryptographiques modernes :

* **SHA-256**
* **SHA-3-256**

---

## 1️⃣ SHA-256

SHA-256 appartient à la famille **SHA-2**.

Il produit une empreinte de :

```text
256 bits = 32 octets = 64 caractères hexadécimaux
```

Exemple conceptuel :

```text
Message
   │
   ▼
SHA-256
   │
   ▼
64 caractères hexadécimaux
```

---

## 2️⃣ SHA-3-256 / Keccak

SHA-3-256 appartient à la famille **SHA-3**, basée sur une construction différente de SHA-2 appelée **Keccak / sponge construction**.

Comme SHA-256, il produit une empreinte de :

```text
256 bits
```

Cependant, **SHA-256 et SHA-3-256 ne sont pas deux implémentations du même algorithme** : ils reposent sur des constructions cryptographiques différentes.

---

## 3️⃣ 🔬 Comparaison des empreintes

Le programme calcule les deux empreintes pour un même message :

```text
                    ┌───────────┐
              ┌────►│ SHA-256   │────► Hash A
              │     └───────────┘
   Message ───┤
              │     ┌───────────┐
              └────►│ SHA-3-256 │────► Hash B
                    └───────────┘
```

Cela permet de constater que deux algorithmes utilisant la même longueur de sortie produisent néanmoins **des empreintes complètement différentes**.

---

# ⚡ 4️⃣ Comparaison des performances

Le programme mesure le temps nécessaire au calcul de :

* SHA-256 ;
* SHA-3-256.

pour différentes tailles de données.

Les résultats sont ensuite représentés sur une courbe comparative.

### Objectif

Observer :

* 📈 l'évolution du temps de calcul ;
* ⚡ les différences de performance ;
* 📦 l'influence de la taille des données.

> Les performances observées dépendent notamment du matériel utilisé, de la version de Python et de l'implémentation cryptographique disponible sur le système.

---

# 📋 5️⃣ Tableau comparatif des fichiers

Plusieurs fichiers sont générés puis analysés.

Pour chaque fichier, le programme affiche les deux empreintes :

| Fichier         | Taille | SHA-256 | SHA-3-256 |
| --------------- | -----: | ------- | --------- |
| `fichier_1.bin` |   … Ko | `…`     | `…`       |
| `fichier_2.bin` |   … Ko | `…`     | `…`       |
| `fichier_3.bin` |   … Ko | `…`     | `…`       |

Cette présentation permet de comparer directement les résultats des deux algorithmes.

---

# ▶️ Exécution

Une fois l'environnement virtuel activé, les deux exercices peuvent être exécutés séparément.

## 🔑 Exercice 1

```bash
python Exo1_HMAC/hmac_exo.py
```

Le programme réalise :

```text
HMAC-SHA256
     ↓
Comparaison avec un hash simple
     ↓
Mesure des performances
     ↓
Génération des fichiers
     ↓
Calcul des HMAC
     ↓
Effet avalanche
```

---

## 🧬 Exercice 2

```bash
python Exo2_SHA/sha_exo.py
```

Le programme réalise :

```text
SHA-256 ────────┐
                ├──► Comparaison
SHA-3-256 ──────┘
       ↓
Mesure des performances
       ↓
Analyse des fichiers
       ↓
Tableau comparatif
```

---

# 📊 Résultats attendus

À l'issue de l'exécution, les programmes permettent d'obtenir plusieurs types de résultats.

### 🔐 Exercice 1

* HMAC d'un message avec une clé secrète ;
* comparaison avec un hash classique ;
* courbe du temps de calcul du HMAC ;
* tableau des fichiers et de leurs HMAC ;
* démonstration de l'effet avalanche.

### 🧬 Exercice 2

* empreinte SHA-256 ;
* empreinte SHA-3-256 ;
* courbe comparative des performances ;
* tableau contenant les deux empreintes pour chaque fichier.

---

# 🧹 Gestion des fichiers générés

Les programmes créent automatiquement des fichiers nécessaires aux expériences.

Les deux répertoires concernés sont :

```text
echantillons_hmac/
echantillons_sha/
```

Afin d'éviter de versionner ces fichiers générés, ils peuvent être ajoutés au `.gitignore`.

### Exemple de `.gitignore`

```gitignore
# Environnement virtuel
venv/

# Fichiers générés par les exercices
echantillons_hmac/
echantillons_sha/

# Python
__pycache__/
*.pyc

# Résultats / visualisations
*.png
*.pdf
*.svg
```

---

# 📌 Synthèse du devoir

| Élément                 | Exercice 1 | Exercice 2 |
| ----------------------- | :--------: | :--------: |
| HMAC avec clé           |      ✅     |      —     |
| Hash simple             |      ✅     |      —     |
| Effet avalanche         |      ✅     |      —     |
| SHA-256                 |      —     |      ✅     |
| SHA-3-256               |      —     |      ✅     |
| Mesure des performances |      ✅     |      ✅     |
| Courbe comparative      |      ✅     |      ✅     |
| Analyse de fichiers     |      ✅     |      ✅     |
| Tableau des empreintes  |      ✅     |      ✅     |

---

# 🎓 Objectifs pédagogiques atteints

À travers ces deux exercices, ce projet permet de mettre en pratique :

* 🔐 les principes du **hachage cryptographique** ;
* 🔑 le fonctionnement du **HMAC** ;
* 🧬 les différences entre **SHA-2 et SHA-3** ;
* 🌪️ le phénomène d'**effet avalanche** ;
* ⏱️ la mesure de performances ;
* 📊 la visualisation de données expérimentales ;
* 📁 le calcul d'empreintes sur des fichiers ;
* 🐍 l'utilisation des bibliothèques cryptographiques de Python.

---

# 🏁 Conclusion

Ce devoir permet de passer d'une approche théorique de la cryptographie à une **expérimentation concrète**.

Les différentes expériences montrent notamment qu'un système de sécurité ne se limite pas à produire une empreinte : il faut également comprendre **le rôle de la clé, les propriétés cryptographiques, les performances et les différences entre les algorithmes**.

> ### 🔐 Hachage pour l'intégrité.
>
> ### 🔑 HMAC pour l'authentification.
>
> ### 🧬 SHA-2 & SHA-3 pour explorer différentes constructions cryptographiques.

---

<div align="center">

## 🚀 Cryptographie × Python × Sécurité

**Devoir Note 2 — Gestion d'identité**

*Étude expérimentale de HMAC, SHA-256 et SHA-3-256*

</div>
