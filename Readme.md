Bucket Manager très basique :

Possibilité de:

- Lister ses buckets
- Voir les fichiers présents sur ses buckets
- Upload, Delete, Download des fichiers 

**Setup**

**1 - Faire un environnement virtuel**

```
python3 -m venv .venv
.venv/bin/activate
```

**2 - Installer les dépendances** 

```
pip install -r requirements.txt
```

**3 - Definir les variables d'environnement**

dans ~/.aws/credentials

aws_access_key_id
aws_secret_access_key

dans ~/.aws/config 

region 

**4 - Lancer le projet **

```
flask --app main.py run
```

