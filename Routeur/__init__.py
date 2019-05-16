from Routeur.entity import Database
from flask import Flask, render_template, request, redirect

# __name__ == FLASK_APP (Configuré en avance avec le terminal)
app = Flask(__name__)


@app.route('/')
def index():

    # On récupère tous les clients
    datas = Database().findall('clients')

    # Puis on affiche une page html avec les données envoyés
    return render_template('index.html', datas=datas)


@app.route('/user/<int:id>', methods=['POST', 'GET'])
def updateuser(id: int) -> int:
    # Si on reçois une requête avec la méthode POST
    if request.method == 'POST':

        # On récupère le nom entrer
        name = request.form['name']

        # Puis on le met à jour sur la base de donnée
        Database().update('UPDATE clients SET name = %s WHERE id = %s', (name, id))

        # Finalement on fait un redirection sur la page d'acceuil
        return redirect("/", code=302)

    # Ici on récupère l'id se trouvant dans l'url example /user/1 -> clients avec l'id 1
    datas = Database().find('clients', id)

    # Puis on affiche une page html avec les données envoyés
    return render_template('updateuser.html', data=datas)


@app.route('/create/user', methods=['POST', 'GET'])
def createuser():
    # Si on reçois une requête avec la méthode POST
    if request.method == 'POST':

        # On récupère le nom entrer
        name = request.form['name']

        # On récupère tous les id des clients
        clients_id = Database().request('SELECT id FROM clients')

        # Si la taille de la list clients_id est infèrieur à 200, on éxècute le code
        if len(clients_id) <= 200:

            # On récupère le Max id pour changé l'auto_incrément de départ, On fait un COALESCE au cas ou il nous
            # retourne None, on le remplace alors par 0
            auto_increment = Database().request('SELECT COALESCE(MAX(id), 0) FROM clients')

            # Ici CHAUFFER VOS NEURONNES, on transforme en int, ce qui est extrait d'un mapping en str de la list
            # donnée en récupérant que le dernier élement de la list
            finale_auto_increment = int("".join(map(str, auto_increment[-1])))

            if finale_auto_increment < 2:
                # On Alter l'auto increment de la table clients pour start at 2
                Database().request('ALTER TABLE clients AUTO_INCREMENT=2')

            # On récupère le Max id_ip pour changé l'auto_incrément de départ, On fait un COALESCE au cas ou il nous
            # retourne None, on le remplace alors par 0
            id_ip = Database().request('SELECT COALESCE(MAX(id_ip), 0) FROM clients')

            # Ici CHAUFFER VOS NEURONNES, on transforme en int, ce qui est extrait d'un mapping en str de la list
            # donnée en récupérant que le dernier élement de la list
            finale_id_ip = int("".join(map(str, id_ip[-1]))) + 14

            # On crée finalement NOTRE UTILISATEUR
            id = Database().create("INSERT INTO clients (name, connexion) VALUES (%s, False)", name)

            if finale_id_ip < 15:
                # On update l'ip id pour le client qui à l'id 2
                Database().request("UPDATE clients SET id_ip = 15 WHERE id = 2")

                # On récupère le Max id_ip pour changé l'auto_incrément de départ, On fait un COALESCE au cas ou il nous
                # retourne None, on le remplace alors par 0
                id_ip = Database().request('SELECT COALESCE(MAX(id_ip), 0) FROM clients WHERE id = 2')

                # Ici CHAUFFER VOS NEURONNES, on transforme en int, ce qui est extrait d'un mapping en str de la list
                # donnée en récupérant que le dernier élement de la list
                finale_id_ip = int("".join(map(str, id_ip[-1]))) + 15

            # Finalement on update pour remplir tous les champs voulue
            Database().update("UPDATE clients SET ip = '164.166.3.%s', vrf = '65500:%s', plage = 28, id_ip = %s WHERE "
                              "id = %s ", (finale_id_ip, id, finale_id_ip, id))

            # Puis on fait un redirection vers la page d'acceuil
            return redirect("/", code=302)

        # Sinon si la list clients_id est supérieur à 200
        else:
            # On crée un message d'erreur
            message = "Attention ! Vous ne pouvez pas créer d'avantages d'utilisateurs car tous vos addresse ip sont " \
                      "utilisé "

            # Puis on affiche une page html avec le message écrit
            return render_template('createuser.html', message=message)

    # On affiche une page html
    return render_template('createuser.html')


if __name__ == '__main__':
    app.run(debug=True)
