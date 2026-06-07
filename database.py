import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        port=8889,           # ← port MAMP
        user="root",
        password="root",     # ← mot de passe MAMP par défaut
        database="lms_educaterra"
    )
    return connection