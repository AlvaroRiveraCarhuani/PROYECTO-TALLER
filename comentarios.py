import db #Importamos el archivo db.py para poder usarla
from publicaciones import Publicacion #Importamos del archivo publiciones.py la clase Publicacion

class Comentario:
    #Contructor la clase Comentario
    def __init__(self, id_comentario=None, id_usuario=None, id_video=None, contenido=None):
        self.id_comentario = id_comentario
        self.id_usuario = id_usuario
        self.id_video = id_video
        self.contenido = contenido

    def crear_comentario(self, id_usuario):
        if not self.verificar_sesion(id_usuario): #Verificamos si el usuario esta logeado
            return #si no esta logeado hacemos un return para cancelar la funcion
        # Crear una instancia de la clase Publicacion asociada al usuario actual
        publicacion = Publicacion(id_usuario)
        # Mostrar las publicaciones disponibles del usuario para que pueda seleccionar una
        # Esto asegura que el usuario tenga contexto y pueda elegir una publicación válida antes de realizar acciones
        publicacion.leer_publicaciones()
        #Pedimos por teclado que ingrese el id_video para comentar
        self.id_video = input("Introduce el ID del video en el que deseas comentar: ")
        self.contenido = input("Escribe tu comentario: ")
        #Realizamos un cursor para realizar funcionalidades a la BD
        cursor = db.connection.cursor()
        #Realizamos una consulta de la BD para hacer un insert en la tabla comentarios
        consulta = "INSERT INTO comentarios (id_usuario, id_video, contenido) VALUES (%s, %s, %s)"
        cursor.execute(consulta, (id_usuario, self.id_video, self.contenido)) #ejecutamos el cursor de la variable consulta
        db.connection.commit() #Guardamos los cambios del cursor

        print("Comentario creado exitosamente.")
        cursor.close() #Cerramos el cursor

    def leer_comentarios(self, id_video):
        cursor = db.connection.cursor() #Cursor para realizar funcionalidades en la BD
        #Realizamos una consulta usando SELECT  y JOIN para unir las tablas de comentarios y usuarios
        consulta = """SELECT c.id_comentario, u.nombre_usuario, c.contenido 
                      FROM comentarios c 
                      JOIN usuarios u ON c.id_usuario = u.id_usuario  
                      WHERE c.id_video = %s"""
        cursor.execute(consulta, (id_video,)) #Ejecutamos el cursor 
        comentarios = cursor.fetchall() #Mostramos todos los resultados de la consulta
        #si no hay comentarios ingreando la id del video ejecutamos:
        if not comentarios:
            print("No hay comentarios para esta publicación.")
        else:
            print(f"Comentarios del video {id_video}:")
            for comentario in comentarios: #Si existe comentarios realizamos un for para mostrar el:
                #Id_comentario, nombre_usuario, contenido
                print(f"{comentario[0]}. {comentario[1]}: {comentario[2]}")

        cursor.close() #Cerramos el cursor

    def actualizar_comentario(self, id_usuario):
        if not self.verificar_sesion(id_usuario): #Verificamos si el usuario esta logeado
            return 
        #Realizamos un cursor para hacer funcionalidades en la BD
        cursor = db.connection.cursor()
        #Realizamos una consulta para mostrar los comentarios con el nombre y contenido 
        consulta = """SELECT c.id_comentario, u.nombre_usuario, c.contenido 
                      FROM comentarios c 
                      JOIN usuarios u ON c.id_usuario = u.id_usuario"""
        cursor.execute(consulta) #Ejecutamos la consulta
        comentarios = cursor.fetchall() #Mostramos todos los comentarios
        #si no hay comentarios para mostrar ejecutamos: 
        if not comentarios:
            print("No hay comentarios disponibles para editar.")
            cursor.close()
            return
        #Si hay comentarios imprimimos: 
        print("\nComentarios disponibles:")
        for comentario in comentarios: #Realizamos un bucle de la tabla comentarios para mostrar el:
            #id_comentario, nombre_usuario, contenido
            print(f"ID: {comentario[0]} | Usuario: {comentario[1]} | Contenido: {comentario[2]}")
        #Pedimos al usuario ingresar el id_comentario para editar
        id_comentario = input("\nIntroduce el ID del comentario que deseas editar: ")
        #Conficional para verificar si ingreso correctamente la id_comentario
        if id_comentario not in [str(c[0]) for c in comentarios]:
            print("Error: Selecciona un comentario válido.")
            cursor.close()
            return
        #Pedimos al usuario por teclado que ingrese el nuevo comentario
        nuevo_contenido = input("Introduce el nuevo contenido del comentario: ")
        #Realizamos la consulta la BD utilizando UPDATE para acutalizar el comentario 
        consulta_actualizacion = """UPDATE comentarios SET contenido = %s WHERE id_comentario = %s"""
        cursor.execute(consulta_actualizacion, (nuevo_contenido, id_comentario)) #Ejecutamos el cursor para realizar la consulta
        db.connection.commit() #Guardamos los cambios del cursor 
        print("Comentario actualizado exitosamente.")
        cursor.close() #Cerramos el cursor para poder realizar otras funcionalidades en la BD

    def eliminar_comentario(self, id_usuario):
        if not self.verificar_sesion(id_usuario): #Verificamos si el usuario esta logeado
            return # Si el usuario no ha iniciado sesión, detenemos la ejecución de la función

        publicacion = Publicacion(id_usuario) #instanciamos la clase Publicacion en la variable publicacion
        publicacion.leer_publicaciones() #De la variable publicacion que almacena la clase Publicacion ejecutamos la funcion de leer publicaciones
        
        self.id_video = input("\nIntroduce el ID de la publicación para ver los comentarios: ")
        #Realizamos un cursor para poder realizar funciones en la BD
        cursor = db.connection.cursor() 
        #Realizamos la consulta en la BD haciendo un JOIN de las tablas comentarios y usuarios
        consulta = """SELECT c.id_comentario, u.nombre_usuario, c.contenido
                      FROM comentarios c
                      JOIN usuarios u ON c.id_usuario = u.id_usuario
                      WHERE c.id_video = %s"""
        cursor.execute(consulta, (self.id_video,)) #Ejecutamos el cursor que almacena la variable de consulta
        comentarios = cursor.fetchall() #Mostramos con fetchall todos los resultados
        if not comentarios:
            print("No hay comentarios en esta publicación.")
            cursor.close() #Cerramos el cursor
            return
        
        print("\nComentarios disponibles:")
        #Bucle para poder mostrar el id_comentario, nombre_usuario, contenido
        for comentario in comentarios:
            print(f"ID: {comentario[0]} | Usuario: {comentario[1]} | Contenido: {comentario[2]}")

        id_comentario = input("\nIntroduce el ID del comentario que deseas eliminar: ")
        #Condicional para verificar si existe el id_comentario
        if id_comentario not in [str(c[0]) for c in comentarios]:
            print("Error: Selecciona un comentario válido.")
            cursor.close()
            return
        #Consulta usando el DELETE de la tabla comentarios
        consulta_eliminacion = "DELETE FROM comentarios WHERE id_comentario = %s"
        cursor.execute(consulta_eliminacion, (id_comentario,)) #Ejecutamos la consulta
        db.connection.commit() #Guardamos los cambios de la consulta

        print("Comentario eliminado exitosamente.")
        cursor.close() #Cerramos el cursor para 
    #Funcion para verificar si el usuario esta con id_usuario caso contrario no podra realizar diferentes funciones
    def verificar_sesion(self, id_usuario):
        """Verifica que el usuario haya iniciado sesión."""
        if id_usuario is None:
            print("Error: Debes iniciar sesión para realizar esta acción.")
            return False
        return True
