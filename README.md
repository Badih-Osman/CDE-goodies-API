## Installation

Clonez le dépôt :

```cmd
git clone https://github.com/Badih-Osman/CDE-goodies-API.git
cd CDE-goodies-API
```

Installez Flask :

```cmd
pip install flask
```

## Lancer l'application

Créez la base de données et ajoutez les exemples :

```cmd
python base_de_donnees.py
```

Lancez ensuite le serveur :

```cmd
python application.py
```

L'API sera disponible à l'adresse :

```text
http://127.0.0.1:5000
```

## Tester l'API

Le fichier `testeur_api.html` est une petite interface pour tester les différentes routes de l'API depuis un navigateur.

La clé utilisée par défaut dans le projet est `osman`. Elle est envoyée dans l'en-tête `X-Cle-API`.

**Important :** le testeur utilise des adresses relatives comme `/api/objets`. Il doit donc être servi depuis la même adresse que l'application Flask. Ouvrir directement le fichier HTML avec un double-clic ne suffit pas avec la configuration actuelle.

# Tester avec curl

Vous pouvez aussi tester l'API depuis un terminal.

### 1. Récupérer tous les objets

```cmd
curl http://127.0.0.1:5000/api/objets
```

### 2. Récupérer un objet par son identifiant

```cmd
curl http://127.0.0.1:5000/api/objets/1
```

Remplacez 1 par l'identifiant de l'objet à récupérer.

### 3. Ajouter un objet

Cette opération nécessite la clé API.

```cmd
curl -X POST http://127.0.0.1:5000/api/objets -H "Content-Type: application/json" -H "X-Cle-API: osman" -d "{\"nom\":\"Mug\",\"prix\":600,\"photo\":\"https://example.com/mug.png\",\"club\":\"Club DIY\"}"
```

La réponse contient l'objet créé, notamment son identifiant (id).

### 4. Modifier un objet

Remplacez 1 par l'identifiant de l'objet que vous voulez modifier.

```cmd
curl -X PATCH http://127.0.0.1:5000/api/objets/1 -H "Content-Type: application/json" -H "X-Cle-API: osman" -d "{\"prix\":700,\"nom\":\"Grand mug\"}"
```

Seuls les champs envoyés dans le JSON sont modifiés.

### 5. Supprimer un objet

Remplacez 1 par l'identifiant de l'objet à supprimer.

```cmd
curl -X DELETE http://127.0.0.1:5000/api/objets/1 -H "X-Cle-API: osman"
```

En cas de succès, l'API renvoie le statut HTTP 204.

### 6. Tester la protection par clé API

Essayez par exemple d'ajouter un objet sans envoyer la clé API :

```cmd
curl -X POST http://127.0.0.1:5000/api/objets -H "Content-Type: application/json" -d "{\"nom\":\"Test\",\"prix\":100}"
```

L'API doit répondre avec le statut HTTP 401.
