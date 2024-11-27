import db

class Publicacion:
    #constructor de la clase publicacion
    def __init__(self, id_video=None, id_usuario=None, titulo=None, descripcion=None):
        self.id_video = id_video
        self.id_usuario = id_usuario
        self.titulo = titulo
        self.descripcion = descripcion

    def crear_publicacion(self, id_usuario):  # Agregamos el parámetro id_usuario
        if not self.verificar_sesion(id_usuario): # Verificamos que el usuario tiene un id
            return  #Si no tiene un id retornamos al menu principal

        self.id_usuario = id_usuario  # Asignamos el id_usuario a la instancia
        #Pedimos al usuario por tecladi el titulo y descripcion del video
        self.titulo = input("Introduce el título de la publicación: ")
        self.descripcion = input("Introduce una descripción: ")
        #asignamos una variable cursor que almacernara la connection.cursor que sirve para poder interactuar con la BD
        cursor = db.connection.cursor()
        #Insertamos en la tabla videos
        consulta = "INSERT INTO videos (id_usuario, titulo, descripcion) VALUES (%s, %s, %s)"
        cursor.execute(consulta, (self.id_usuario, self.titulo, self.descripcion)) #Ejecutamos la consulta
        db.connection.commit() #Guardamos los cambios de la consulta
        #Si todo esta correctamente imprimimos: 
        print("Publicación creada exitosamente.")
        cursor.close() #Cerramos el cursor para para que no vea error al ejecutar otro cursor 

    def leer_publicaciones(self):
        cursor = None  #Inicializamos la variable cursor en None
        try:
            cursor = db.connection.cursor() #inicializamos el cursor
            consulta = """
                SELECT v.id_video, u.nombre_usuario, v.titulo, v.descripcion 
                FROM videos v 
                JOIN usuarios u ON v.id_usuario = u.id_usuario
            """
            cursor.execute(consulta) #ejecutamos la consulta 
            publicaciones = cursor.fetchall()  #fetchall para mostrar todas las publicaciones disponibles

            if publicaciones:
                print("\nPublicaciones disponibles:")
                for publicacion in publicaciones: #Bucle for para imprimir los campos de la tabla publicaciones
                    print(f"ID: {publicacion[0]} | Autor: {publicacion[1]} | Título: {publicacion[2]} | Descripción: {publicacion[3]}")
            else:
                print("\nNo hay publicaciones disponibles.")

        except Exception as e:
            print("Ocurrió un error al leer publicaciones:", e)

        finally:
            if cursor:  
                cursor.close() #Cerrar el cursor

    def actualizar_publicacion(self, id_usuario):  
        if not self.verificar_sesion(id_usuario): #Verficamos que el usuario este con un id
            return  
        #Variable para poder conectarse y hacer funciones en la BD
        cursor = db.connection.cursor()
        consulta = """ 
            SELECT v.id_video, v.titulo, v.descripcion, u.nombre_usuario 
            FROM videos v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            WHERE v.id_usuario = %s
        """ #consultado utilizando join
        cursor.execute(consulta, (id_usuario,)) #Ejecucion del cursor
        publicaciones = cursor.fetchall() #Fetchall para mostrar todas las publicaciones del usuario
        if not publicaciones:
            print("No tienes publicaciones para editar.")
            cursor.close()
            return

        print("\nTus publicaciones:")
        for publicacion in publicaciones: #Buble para mostrar al usuario sus publicaciones
            print(f"ID: {publicacion[0]} | Título: {publicacion[1]} | Descripción: {publicacion[2]} | Usuario: {publicacion[3]}")
        #input para que el usuario ingrese al id_publicacion a editar
        id_publicacion = input("\nIntroduce el ID de la publicación que deseas editar: ")

        # Verifica si el ID ingresado corresponde a una publicación válida del usuario
        if id_publicacion not in [str(p[0]) for p in publicaciones]:
            print("Error: Selecciona una publicación que te pertenezca.")
            cursor.close()
            return  
        #Pedir por teclado
        nuevo_titulo = input("Introduce el nuevo título: ")
        nueva_descripcion = input("Introduce la nueva descripción: ")
        consulta_actualizacion = """
            UPDATE videos 
            SET titulo = %s, descripcion = %s 
            WHERE id_video = %s AND id_usuario = %s
        """
        cursor.execute(consulta_actualizacion, (nuevo_titulo, nueva_descripcion, id_publicacion, id_usuario)) #Ejecutamos la consulta
        db.connection.commit() #Guardamos los cambios de la consulta

        print("Publicación actualizada exitosamente.")
        cursor.close() #Cerramos el cursor
    
    def eliminar_publicacion(self, id_usuario):  
        if not self.verificar_sesion(id_usuario): #Verificamos si el usuario esta logeado
            return 
        #Cursor para realizar funciones con la BD
        cursor = db.connection.cursor()
        consulta = """
            SELECT v.id_video, v.titulo, v.descripcion, u.nombre_usuario 
            FROM videos v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            WHERE v.id_usuario = %s
        """ 
        cursor.execute(consulta, (id_usuario,))
        publicaciones = cursor.fetchall() #Para almacenar todas las publicaciones del usuario con fetchall
        if not publicaciones: #condicional para verificar si el usuario tiene publicaciones
            print("No tienes publicaciones para eliminar.")
            cursor.close() #Cerramos el cursor
            return
        
        print("\nTus publicaciones:")
        for publicacion in publicaciones: #Bucle para mostrar las publicaciones del usuario
            print(f"ID: {publicacion[0]} | Título: {publicacion[1]} | Descripción: {publicacion[2]}")
        #Pedimos por teclado al usuario el id_publicacion que desea eliminar
        id_publicacion = input("\nIntroduce el ID de la publicación que deseas eliminar: ")
        #Condicional para verificar si el usuario ingreso la id_publicacion que le pertenezca
        if id_publicacion not in [str(p[0]) for p in publicaciones]:
            print("Error: Selecciona una publicación que te pertenezca.")
            cursor.close()
            return  
        #consulta para eliminar el video por la id_video de la tabla videos
        consulta_eliminacion = "DELETE FROM videos WHERE id_video = %s AND id_usuario = %s"
        cursor.execute(consulta_eliminacion, (id_publicacion, id_usuario)) #ejecutamos la consulta
        db.connection.commit() #Guardamos la consulta

        print("Publicación eliminada exitosamente.")
        cursor.close() #Cerramos el cursor

    def buscar_video_por_titulo(self):
        cursor = db.connection.cursor() #Cursor para poder hacer funciones en la BD
        titulo = input("Introduce el título del video que buscas: ")
        #consulta usando Like para la busqueda con coincidencias del titulo
        consulta = "SELECT v.id_video, u.nombre_usuario, v.titulo, v.descripcion FROM videos v JOIN usuarios u ON v.id_usuario = u.id_usuario WHERE v.titulo LIKE %s"
        #Realizamos la consulta con el símbolo % en SQL es un comodín que representa "cualquier cosa" (cero o más caracteres)
        cursor.execute(consulta, ("%" + titulo + "%",))
        resultados = cursor.fetchall() #Muestra de todas las coincidencias de la busqueda del titulo
        
        if resultados:
            print("\nResultados de búsqueda:")
            for resultado in resultados: #Bucle para mostrar todas las publicaciones encontradas
                print(f"ID: {resultado[0]} | Autor: {resultado[1]} | Título: {resultado[2]} | Descripción: {resultado[3]}")
        else:
            print("No se encontraron resultados.")
        
        cursor.close()
 #Funcion que sirve para verificar si el usuario esta logeado o con un id_usuario
    def verificar_sesion(self, id_usuario):
        """Verifica si el usuario está autenticado"""
        if not id_usuario:
            print("Debes iniciar sesión para continuar.")
            return False
        return True
