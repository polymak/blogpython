# BlogPython

Un petit projet web complet avec séparation frontend/public et administration backend, réalisé avec Python Django, MySQL et Tailwind CSS.

## Description

BlogPython est une application de blog simple et élégante avec :
- Une partie publique pour afficher les articles
- Une partie administration pour gérer les articles et les utilisateurs
- Design moderne et responsive inspiré de X.com et Instagram.com
- Upload d'images pour les articles
- Authentification admin sécurisée

## Prérequis

- **Python**: 3.12.10
- **MySQL**: 8.1.31
- **WampServer**: Installation locale avec MySQL activé
- **pip**: Pour installer les dépendances Python
- **Navigateur web**: Pour accéder à l'application

## Installation

### 1. Créer la base de données MySQL

1. Ouvrez phpMyAdmin via WampServer (http://localhost/phpmyadmin)
2. Créez une nouvelle base de données nommée `blogpython`
3. Assurez-vous que l'utilisateur `root` n'a pas de mot de passe (par défaut sur WampServer)

### 2. Installer les dépendances Python

Ouvrez un terminal dans le répertoire du projet et exécutez :

```bash
pip install -r requirements.txt
```

### 3. Configurer Django

Le projet est déjà configuré pour utiliser MySQL avec les paramètres suivants :
- Base de données: `blogpython`
- Utilisateur: `root`
- Mot de passe: (vide)
- Hôte: `127.0.0.1`
- Port: `3306`

### 4. Créer les migrations et la base de données

Exécutez les commandes suivantes dans le terminal :

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer l'utilisateur admin par défaut

Exécutez le script de seed pour créer l'utilisateur admin :

```bash
python seed_admin.py
```

Cela créera un utilisateur avec :
- **Username**: `Admin`
- **Password**: `Admin123`
- **Email**: `admin@blogpython.com`

### 6. Lancer le serveur Django

```bash
python manage.py runserver
```

## URLs d'accès

Une fois le serveur lancé, vous pouvez accéder aux différentes parties de l'application :

### Pages Publiques
- **Page d'accueil**: http://127.0.0.1:8000/
- **Page de login**: http://127.0.0.1:8000/login/

### Pages Administration (après connexion)
- **Dashboard**: http://127.0.0.1:8000/admin/dashboard/
- **Liste des blogs**: http://127.0.0.1:8000/admin/blogs/
- **Liste des utilisateurs**: http://127.0.0.1:8000/admin/users/

## Utilisation

### Se connecter à l'administration

1. Allez sur http://127.0.0.1:8000/login/
2. Entrez les identifiants :
   - Username: `Admin`
   - Password: `Admin123`
3. Cliquez sur "Se connecter"

### Gérer les articles

Depuis le dashboard ou directement via http://127.0.0.1:8000/admin/blogs/ :

**Ajouter un article**:
1. Cliquez sur "Nouvel article"
2. Remplissez le titre, le contenu et téléchargez une image (optionnel)
3. Cliquez sur "Enregistrer"

**Modifier un article**:
1. Dans la liste des articles, cliquez sur "Modifier"
2. Apportez vos modifications
3. Cliquez sur "Enregistrer"

**Supprimer un article**:
1. Dans la liste des articles, cliquez sur "Supprimer"
2. Confirmez la suppression

### Gérer les utilisateurs admin

Depuis le dashboard ou directement via http://127.0.0.1:8000/admin/users/ :

**Ajouter un utilisateur**:
1. Cliquez sur "Nouvel utilisateur"
2. Remplissez le nom d'utilisateur, l'email et le mot de passe
3. Cliquez sur "Enregistrer"

**Supprimer un utilisateur**:
1. Dans la liste des utilisateurs, cliquez sur "Supprimer"
2. Confirmez la suppression
3. **Note**: Vous ne pouvez pas supprimer votre propre compte

### Se déconnecter

Cliquez sur "Déconnexion" dans le menu de navigation.

## Structure du projet

```
blogsite/
├── blog/                          # Application Django principale
│   ├── __init__.py
│   ├── admin.py                   # Configuration admin Django
│   ├── apps.py
│   ├── forms.py                   # Formulaires Django
│   ├── models.py                  # Modèles de données
│   ├── urls.py                    # URLs de l'application
│   ├── views.py                   # Vues Django
│   └── templates/                 # Templates HTML
│       └── blog/
│           ├── base.html          # Template de base avec Tailwind
│           ├── home.html          # Page d'accueil publique
│           ├── login.html         # Page de login
│           ├── dashboard.html     # Dashboard admin
│           └── admin/             # Templates admin
│               ├── blog_list.html
│               ├── blog_form.html
│               ├── blog_confirm_delete.html
│               ├── user_list.html
│               ├── user_form.html
│               └── user_confirm_delete.html
├── blogsite/                      # Configuration Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # Configuration (MySQL, static files, etc.)
│   ├── urls.py                    # URLs principales
│   └── wsgi.py
├── media/                         # Images uploadées (créé automatiquement)
├── static/                        # Fichiers statiques
├── manage.py                      # Script de gestion Django
├── seed_admin.py                  # Script de création utilisateur admin
├── requirements.txt               # Dépendances Python
└── README.md                      # Ce fichier
```

## Emplacement des images uploadées

Les images uploadées pour les articles sont stockées dans le dossier `media/blog_images/` à la racine du projet.

## Dépannage

### MySQL refuse la connexion

**Problème**: Erreur de connexion à MySQL
**Solution**:
1. Vérifiez que WampServer est démarré
2. Vérifiez que MySQL est actif (icône vert dans la barre WampServer)
3. Vérifiez que la base de données `blogpython` existe
4. Vérifiez que l'utilisateur `root` n'a pas de mot de passe

### Les images ne s'affichent pas

**Problème**: Les images uploadées ne s'affichent pas
**Solution**:
1. Vérifiez que le dossier `media/` existe à la racine du projet
2. Vérifiez que les permissions sont correctes
3. Redémarrez le serveur Django

### Les migrations échouent

**Problème**: Erreur lors de l'exécution des migrations
**Solution**:
1. Vérifiez que MySQL est accessible
2. Vérifiez que la base de données `blogpython` existe
3. Exécutez `python manage.py migrate --run-syncdb` si nécessaire

### Tailwind CSS ne compile pas

**Problème**: Le style Tailwind n'est pas appliqué
**Solution**:
- Le projet utilise Tailwind CSS via CDN, donc aucune compilation n'est nécessaire
- Vérifiez votre connexion internet pour charger le CDN

## Sécurité

- Le mot de passe admin par défaut est `Admin123` - changez-le en production
- L'application utilise l'authentification Django standard
- Les uploads d'images sont limités aux formats supportés par Pillow

## Technologies utilisées

- **Backend**: Python Django 5.2.8
- **Base de données**: MySQL 8.1.31
- **Frontend**: HTML, CSS avec Tailwind CSS (CDN)
- **Serveur**: Django development server
- **Upload d'images**: Django FileField avec Pillow

## Auteurs

Projet créé selon les spécifications demandées.

## License

Ce projet est open source et disponible sous la license MIT.