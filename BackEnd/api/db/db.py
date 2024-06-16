import mysql.connector
from flask import g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="pianoclassification"
        )
    return g.db

def close_db(error):
    if 'db' in g:
        g.db.close()
        del g.db