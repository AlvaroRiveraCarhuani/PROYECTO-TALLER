import db

class Publicacion:
    def __init__(self, id_video=None, id_usuario=None, titulo=None, descripcion=None):
        self.id_video = id_video
        self.id_usuario = id_usuario
        self.titulo = titulo
        self.descripcion = descripcion

    def crear_publicacion(self, id_usuario):  # Agregamos el parámetro id_usuario
        if not self.verificar_sesion(id_usuario):
            return  

        self.id_usuario = id_usuario  # Asignamos el id_usuario a la instancia
        self.titulo = input("Introduce el título de la publicación: ")
        self.descripcion = input("Introduce una descripción: ")

        cursor = db.connection.cursor()

        consulta = "INSERT INTO videos (id_usuario, titulo, descripcion) VALUES (%s, %s, %s)"
        cursor.execute(consulta, (self.id_usuario, self.titulo, self.descripcion))
        db.connection.commit()

        print("Publicación creada exitosamente.")
        cursor.close()

    def leer_publicaciones(self):
        cursor = None  
        try:
            cursor = db.connection.cursor()
            consulta = """
                SELECT v.id_video, u.nombre_usuario, v.titulo, v.descripcion 
                FROM videos v 
                JOIN usuarios u ON v.id_usuario = u.id_usuario
            """
            cursor.execute(consulta)
            publicaciones = cursor.fetchall()  

            if publicaciones:
                print("\nPublicaciones disponibles:")
                for publicacion in publicaciones:
                    print(f"ID: {publicacion[0]} | Autor: {publicacion[1]} | Título: {publicacion[2]} | Descripción: {publicacion[3]}")
            else:
                print("\nNo hay publicaciones disponibles.")

        except Exception as e:
            print("Ocurrió un error al leer publicaciones:", e)

        finally:
            if cursor:  
                cursor.close()

    def actualizar_publicacion(self, id_usuario):  # Asegúrate de recibir el parámetro id_usuario
        if not self.verificar_sesion(id_usuario):
            return  

        cursor = db.connection.cursor()
        consulta = """
            SELECT v.id_video, v.titulo, v.descripcion, u.nombre_usuario 
            FROM videos v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            WHERE v.id_usuario = %s
        """
        cursor.execute(consulta, (id_usuario,))
        publicaciones = cursor.fetchall()
        if not publicaciones:
            print("No tienes publicaciones para editar.")
            cursor.close()
            return

        print("\nTus publicaciones:")
        for publicacion in publicaciones:
            print(f"ID: {publicacion[0]} | Título: {publicacion[1]} | Descripción: {publicacion[2]} | Usuario: {publicacion[3]}")

        id_publicacion = input("\nIntroduce el ID de la publicación que deseas editar: ")

        # Verifica si el ID ingresado corresponde a una publicación válida del usuario
        if id_publicacion not in [str(p[0]) for p in publicaciones]:
            print("Error: Selecciona una publicación que te pertenezca.")
            cursor.close()
            return  

        nuevo_titulo = input("Introduce el nuevo título: ")
        nueva_descripcion = input("Introduce la nueva descripción: ")
        consulta_actualizacion = """
            UPDATE videos 
            SET titulo = %s, descripcion = %s 
            WHERE id_video = %s AND id_usuario = %s
        """
        cursor.execute(consulta_actualizacion, (nuevo_titulo, nueva_descripcion, id_publicacion, id_usuario))
        db.connection.commit()

        print("Publicación actualizada exitosamente.")
        cursor.close()

    def eliminar_publicacion(self, id_usuario):  # Asegúrate de recibir el parámetro id_usuario
        if not self.verificar_sesion(id_usuario):
            return 

        cursor = db.connection.cursor()
        consulta = """
            SELECT v.id_video, v.titulo, v.descripcion, u.nombre_usuario 
            FROM videos v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            WHERE v.id_usuario = %s
        """
        cursor.execute(consulta, (id_usuario,))
        publicaciones = cursor.fetchall()
        if not publicaciones:
            print("No tienes publicaciones para eliminar.")
            cursor.close()
            return

        print("\nTus publicaciones:")
        for publicacion in publicaciones:
            print(f"ID: {publicacion[0]} | Título: {publicacion[1]} | Descripción: {publicacion[2]}")

        id_publicacion = input("\nIntroduce el ID de la publicación que deseas eliminar: ")

        if id_publicacion not in [str(p[0]) for p in publicaciones]:
            print("Error: Selecciona una publicación que te pertenezca.")
            cursor.close()
            return  

        consulta_eliminacion = "DELETE FROM videos WHERE id_video = %s AND id_usuario = %s"
        cursor.execute(consulta_eliminacion, (id_publicacion, id_usuario))
        db.connection.commit()

        print("Publicación eliminada exitosamente.")
        cursor.close()

    def buscar_video_por_titulo(self):
        cursor = db.connection.cursor()
        titulo = input("Introduce el título del video que buscas: ")
        consulta = "SELECT v.id_video, u.nombre_usuario, v.titulo, v.descripcion FROM videos v JOIN usuarios u ON v.id_usuario = u.id_usuario WHERE v.titulo LIKE %s"
        cursor.execute(consulta, ("%" + titulo + "%",))
        resultados = cursor.fetchall()

        if resultados:
            print("\nResultados de búsqueda:")
            for resultado in resultados:
                print(f"ID: {resultado[0]} | Autor: {resultado[1]} | Título: {resultado[2]} | Descripción: {resultado[3]}")
        else:
            print("No se encontraron resultados.")
        
        cursor.close()

    def verificar_sesion(self, id_usuario):
        """Verifica si el usuario está autenticado"""
        if not id_usuario:
            print("Debes iniciar sesión para continuar.")
            return False
        return True
