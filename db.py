import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tiktok_db"
    )
    return connection

if True:
    connection = get_connection()
    print("Conexion esta bien")
