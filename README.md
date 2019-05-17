# Python-Routeur
I help my friend for is project with python

If you want to use the file just paste the below code in our shell

```
pip install PyMySQL
```
```
pip install Flask
FLASK_APP=our_app.py
FLASK_ENV=development
```

Change the Database settings in files entity.py in Routeur Folder
```
self.db = pymysql.connect(host='host', user='username', password='password', db='database')
```

Below is the table i use for the script

```
DROP TABLE IF EXISTS database.clients
CREATE TABLE clients (id INT AUTO_INCREMENT PRIMARY KEY, vrf VARCHAR (255), name VARCHAR (64), ip VARCHAR (24), id_ip INT, plage INT, connexion BOOLEAN)
```

After editing the database and creating the table in the database use the code below for run our App

```
flask run
```
