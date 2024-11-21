import db
from publicaciones import Publicacion

class Comentario:
    def __init__(self, id_comentario=None, id_usuario=None, id_video=None, contenido=None):
        self.id_comentario = id_comentario
        self.id_usuario = id_usuario
        self.id_video = id_video
        self.contenido = contenido

    def crear_comentario(self):
        if not self.verificar_sesion(self.id_usuario):
            return  

        # Lee las publicaciones para permitir al usuario elegir una
        publicacion = Publicacion(self.id_usuario)
        publicacion.leer_publicaciones()

        self.id_video = input("Introduce el ID del video en el que deseas comentar: ")
        self.contenido = input("Escribe tu comentario: ")

        cursor = db.connection.cursor()

        consulta = "INSERT INTO comentarios (id_usuario, id_video, contenido) VALUES (%s, %s, %s)"
        cursor.execute(consulta, (self.id_usuario, self.id_video, self.contenido))
        db.connection.commit()

        print("Comentario creado exitosamente.")
        cursor.close()

    def leer_comentarios(self):
        # Lee las publicaciones para permitir al usuario elegir una
        publicacion = Publicacion(self.id_usuario)
        publicacion.leer_publicaciones()

        self.id_video = input("\nIntroduce el ID de la publicación para ver los comentarios: ")

        cursor = db.connection.cursor()
        consulta = """SELECT c.id_comentario, u.nombre_usuario, c.contenido FROM comentarios c 
                      JOIN usuarios u ON c.id_usuario = u.id_usuario  
                      WHERE c.id_video = %s"""
        cursor.execute(consulta, (self.id_video,))
        comentarios = cursor.fetchall()

        if not comentarios:
            print("No hay comentarios para esta publicación.")
        else:
            print(f"Comentarios del video {self.id_video}:")
            for comentario in comentarios:
                # Muestra ID, nombre de usuario y comentario
                print(f"{comentario[0]}. {comentario[1]}: {comentario[2]}")

        cursor.close()

    def actualizar_comentario(self):
        cursor = db.connection.cursor()
        consulta = """
            SELECT c.id_comentario, u.nombre_usuario, c.contenido 
            FROM comentarios c 
            JOIN usuarios u ON c.id_usuario = u.id_usuario
        """
        cursor.execute(consulta)
        comentarios = cursor.fetchall()

        if not comentarios:
            print("No hay comentarios disponibles para editar.")
            cursor.close()
            return

        print("\nComentarios disponibles:")
        for comentario in comentarios:
            print(f"ID: {comentario[0]} | Usuario: {comentario[1]} | Contenido: {comentario[2]}")

        id_comentario = input("\nIntroduce el ID del comentario que deseas editar: ")

        if id_comentario not in [str(c[0]) for c in comentarios]:
            print("Error: Selecciona un comentario válido.")
            cursor.close()
            return

        nuevo_contenido = input("Introduce el nuevo contenido del comentario: ")

        consulta_actualizacion = """
            UPDATE comentarios 
            SET contenido = %s 
            WHERE id_comentario = %s
        """
        cursor.execute(consulta_actualizacion, (nuevo_contenido, id_comentario))
        db.connection.commit()

        print("Comentario actualizado exitosamente.")
        cursor.close()

    def eliminar_comentario(self):
        if not self.verificar_sesion(self.id_usuario):
            return  

        publicacion = Publicacion(self.id_usuario)
        publicacion.leer_publicaciones()

        self.id_video = input("\nIntroduce el ID de la publicación para ver los comentarios: ")

        cursor = db.connection.cursor()
        consulta = """
            SELECT c.id_comentario, u.nombre_usuario, c.contenido
            FROM comentarios c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE c.id_video = %s
        """
        cursor.execute(consulta, (self.id_video,))
        comentarios = cursor.fetchall()

        if not comentarios:
            print("No hay comentarios en esta publicación.")
            cursor.close()
            return

        print("\nComentarios disponibles:")
        for comentario in comentarios:
            print(f"ID: {comentario[0]} | Usuario: {comentario[1]} | Contenido: {comentario[2]}")

        id_comentario = input("\nIntroduce el ID del comentario que deseas eliminar: ")

        if id_comentario not in [str(c[0]) for c in comentarios]:
            print("Error: Selecciona un comentario válido.")
            cursor.close()
            return

        consulta_eliminacion = "DELETE FROM comentarios WHERE id_comentario = %s"
        cursor.execute(consulta_eliminacion, (id_comentario,))
        db.connection.commit()

        print("Comentario eliminado exitosamente.")
        cursor.close()

    def verificar_sesion(self, id_usuario):
        """Verifica que el usuario haya iniciado sesión."""
        if id_usuario is None:
            print("Error: Debes iniciar sesión para realizar esta acción.")
            return False
        return True
