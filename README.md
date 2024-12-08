# **Projet SocialMedia**

## **Description**
Ce projet implémente un système de gestion d'un réseau social utilisant une base de données Neo4j pour modéliser et manipuler les relations entre utilisateurs, tweets et autres entités. Il comprend :
- Un backend en **Python** avec des scripts pour gérer les fonctionnalités principales.
- Un serveur **Django** qui agit comme interface entre la base de données et un éventuel frontend.
- L'implémentation d'algorithmes avancés pour analyser les relations et les centralités des utilisateurs.

> **Note :** Le frontend initialement prévu n'a pas pu être implémenté en raison du départ imprévu d'un membre du groupe.

---

## **Fonctionnalités**

### **Gestion des utilisateurs**
- **Créer un utilisateur** : Ajoute un nouvel utilisateur dans la base avec des informations telles que son nom, son pseudo, ses followers, etc.
- **Supprimer un utilisateur** : Supprime un utilisateur ainsi que toutes ses relations associées.
- **Mettre à jour un utilisateur** : Modifie les informations personnelles d'un utilisateur existant.
- **Afficher les attributs d'un utilisateur** : Permet de consulter les informations détaillées d'un utilisateur.
- **Lister tous les utilisateurs** : Affiche les informations de tous les utilisateurs présents dans la base.

### **Gestion des relations**
- **Suivre un utilisateur** : Ajoute une relation `FOLLOWS` entre deux utilisateurs.
- **Arrêter de suivre un utilisateur** : Supprime une relation `FOLLOWS`.

### **Gestion des tweets**
- **Poster un tweet** : Crée un nouveau tweet associé à un utilisateur.
- **Supprimer un tweet** : Supprime un tweet et toutes ses relations associées.
- **Liker un tweet** : Incrémente le compteur de "likes" d'un tweet.

### **Analyses avancées**
- **Distance sociale (poignées de main)** : Calcule le nombre de relations entre deux utilisateurs et affiche le chemin exact entre eux.
- **Statistiques utilisateurs** :
  - Nombre total d'utilisateurs.
  - Moyenne du nombre d'abonnements par utilisateur.
  - Moyenne du nombre de followers par utilisateur.
- **Statistiques tweets** :
  - Nombre total de tweets.
  - Moyenne des likes par tweet.
- **Algorithmes de centralité** *(en cours d'intégration)* :
  - Calcul de la centralité de degré, d'intermédiarité, et de proximité.

---

## **Technologies utilisées**

### **Backend**
- **Python** : Pour implémenter les scripts et les fonctionnalités principales.
- **Django** : Pour créer une API REST qui communique avec la base de données Neo4j.

### **Base de données**
- **Neo4j** : Base de données graphe utilisée pour stocker et gérer les utilisateurs, les relations, et les tweets.

---

## **Installation**

### **Prérequis**
- Python 3.9+
- Neo4j Community Edition ou Enterprise Edition
- Django
- Une instance Neo4j fonctionnelle avec les identifiants corrects (configurable dans le script Python).

### **Étapes**
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/Projet-SocialMedia.git
   cd Projet-SocialMedia

    Installez les dépendances :

pip install -r requirements.txt

Configurez les identifiants Neo4j dans le fichier settings.py ou directement dans les scripts :

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "votre_mot_de_passe")
DATABASE_NAME = "twitter"

Démarrez le serveur Django :

    python manage.py runserver

    Accédez à l'API via http://127.0.0.1:8000.

Structure du projet

Projet-SocialMedia/
│
├── Back/                         # Backend
│   ├── manage.py                 # Point d'entrée Django
│   ├── settings.py               # Configuration Django et Neo4j
│   ├── neo4J_requests.py         # Scripts Python pour interagir avec Neo4j
│   ├── api/                      # Application Django pour l'API REST
│   │   ├── urls.py               # Routes de l'API
│   │   ├── views.py              # Contrôleurs de l'API
│   │   └── serializers.py        # Sérialisation des données
│   └── ...
│
├── requirements.txt              # Dépendances Python
└── README.md                     # Documentation

Limitations

    Le frontend n'a pas été implémenté, en raison du départ imprévu d'un membre clé de l'équipe. Cependant, le backend et l'API REST sont entièrement fonctionnels et prêts pour une intégration avec une interface utilisateur.
