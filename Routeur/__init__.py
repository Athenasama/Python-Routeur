from Routeur.entity import Database
from flask import Flask, render_template, request, redirect

# __name__ == FLASK_APP
app = Flask(__name__)


@app.route('/')
def index():
    datas = Database().findall('clients')
    return render_template('index.html', datas=datas)


@app.route('/user/<int:id>', methods=['POST', 'GET'])
def user(id):
    if request.method == 'POST':
        name = request.form['name']
        Database().update('UPDATE clients SET name = %s WHERE id = %s', (name, id))
        return redirect("/", code=302)
    datas = Database().find('clients', id)
    return render_template('user.html', data=datas)


@app.route('/create/user', methods=['POST', 'GET'])
def createuser():
    if request.method == 'POST':
        name = request.form['name']
        clients_id = Database().request('SELECT id FROM clients')
        if len(clients_id) <= 200:
            auto_increment = Database().request('SELECT COALESCE(MAX(id), 0) FROM clients')
            finale_auto_increment = int("".join(map(str, auto_increment[-1])))
            if finale_auto_increment < 2:
                Database().request('ALTER TABLE clients AUTO_INCREMENT=2')

            id_ip = Database().request('SELECT COALESCE(MAX(id_ip), 0) FROM clients')
            finale_id_ip = int("".join(map(str, id_ip[-1]))) + 14
            id = Database().create("INSERT INTO clients (name, connexion) VALUES (%s, False)", name)
            if finale_id_ip < 15:
                Database().request("UPDATE clients SET id_ip = 15 WHERE id = 2")
                id_ip = Database().request('SELECT COALESCE(MAX(id_ip), 0) FROM clients WHERE id = 2')
                finale_id_ip = int("".join(map(str, id_ip[-1]))) + 15
            Database().update("UPDATE clients SET ip = '164.166.3.%s', vrf = '65500:%s', plage = 28, id_ip = %s WHERE "
                              "id = %s ", (finale_id_ip, id, finale_id_ip, id))
            return redirect("/", code=302)
        else:
            message = "Attention ! Vous ne pouvez pas créer d'avantages d'utilisateurs car tous vos addresse ip sont " \
                      "utilisé "
            return render_template('createuser.html', message=message)
    return render_template('createuser.html')


if __name__ == '__main__':
    app.run(debug=True)
