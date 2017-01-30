import sqlite3
from flask import g

DATABASE = 'db/words.db'

class DatabaseManager(object):

    def __init__(self, app, path=DATABASE):
        self.app = app
        self.path = path

    def getDB(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.path)
        return db


    def queryDB(self, query, args=(), one=False):
        cur = self.getDB().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def insertDB(self,table, fields=(), values=()):
        cur = self.getDB()
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            table,
            ', '.join(fields),
            ', '.join(['?'] * len(values))
        )
        cur.execute(query, values)
        cur.commit()

    def closeConnection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()