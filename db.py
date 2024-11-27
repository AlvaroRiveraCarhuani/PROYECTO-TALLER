#Importamos la libreria para conexion a la BD de Mysql XAMPP
import mysql.connector
#Funcion para realizar la conexion
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="tiktok_db" #nombre de la BD creada
    )
    return connection
#Condicional para verificar que se realizo la conexion
if True:
    connection = get_connection()
    print("Conexion esta bien")
