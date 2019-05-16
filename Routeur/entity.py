import pymysql.cursors


class Database:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='juliette', db='python_routeur')
        self.cursor = self.db.cursor()

    def findall(self, table):
        self.cursor.execute('SELECT * FROM {}'.format(table))
        return self.cursor.fetchall()

    def find(self, table, id):
        self.cursor.execute('SELECT * FROM {}'.format(table) + ' WHERE id = %s', id)
        return self.cursor.fetchone()

    def update(self, request, array):
        self.cursor.execute(request, array)
        self.db.commit()

    def create(self, request, array):
        self.cursor.execute(request, array)
        self.db.commit()

        return self.cursor.lastrowid

    def request(self, request):
        self.cursor.execute(request)
        return self.cursor.fetchall()
