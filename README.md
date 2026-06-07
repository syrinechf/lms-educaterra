# LMS Educaterra

Application bureau développée dans le cadre de mon alternance au CFA Educaterra, spécialisé dans les métiers du sport et de l'animation.

## Présentation

Le CFA Educaterra forme des futurs professionnels du sport et de l'animation (BPJEPS, MAPST, AAN, ASEC). Ce projet vise à digitaliser et centraliser la gestion pédagogique via une application bureau installable sur les postes du CFA.

## Fonctionnalités

### Administrateur
- Gestion des comptes utilisateurs (création, attribution des rôles)
- Visualisation des parcours de formation

### Formateur
- Création et gestion des fiches journalières
- Création et publication de cours
- Création de quiz associés aux cours
- Suivi des apprenants

### Apprenant
- Accès aux cours publiés
- Passage de quiz avec correction automatique
- Suivi des activités sportives
- Tableau de bord de progression

## Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python 3.14 | Langage principal |
| CustomTkinter | Interface graphique bureau |
| MySQL 8 | Base de données |
| mysql-connector-python | Connexion Python ↔ MySQL |
| bcrypt | Hachage sécurisé des mots de passe |
| Git / GitHub | Versioning du code |

## Installation

### Prérequis
- Python 3.11+
- XAMPP ou MAMP (serveur MySQL)
- pip

### Étapes

1. Cloner le dépôt :
```
git clone https://github.com/syrinechf/lms-educaterra.git
cd lms-educaterra
```

2. Installer les dépendances :
```
pip install customtkinter mysql-connector-python bcrypt pyinstaller
```

3. Importer la base de données :
- Démarrer MySQL via XAMPP ou MAMP
- Créer une base `lms_educaterra` dans phpMyAdmin
- Importer le fichier `lms_educaterra.sql`

4. Configurer la connexion dans `database.py` :
```python
connection = mysql.connector.connect(
    host="localhost",
    port=8889,
    user="root",
    password="root",
    database="lms_educaterra"
)
```

5. Lancer l'application :
```
python3 main.py
```

## Comptes de test

| Rôle | Email | Mot de passe |
|---|---|---|
| Administrateur | admin@educaterra.fr | admin123 |
| Formateur | formateur@educaterra.fr | form123 |
| Apprenant | apprenant@educaterra.fr | app123 |

## Structure du projet

```
lms-educaterra/
├── main.py
├── database.py
├── auth.py
├── views/
│   ├── login.py
│   ├── admin.py
│   ├── formateur.py
│   └── apprenant.py
├── modules/
│   ├── quiz.py
│   ├── activites.py
│   └── dashboard.py
└── README.md
```

## Sécurité

- Mots de passe hachés via **bcrypt**
- Requêtes SQL avec **paramètres préparés** (protection injection SQL)
- Contrôle des accès par **rôle** dès la connexion

## Auteur

**Syrine Cherif** — BTS SIO option SLAM  
Alternance CFA Educaterra — Saint-Denis  
Candidat n° 2248916238