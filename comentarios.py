import db
from publicaciones import leer_publicaciones

def crear_comentario(id_usuario):
    leer_publicaciones()
    id_video = input("Introduce el ID del video en el que deseas comentar: ")
    contenido = input("Escribe tu comentario: ")

    cursor = db.connection.cursor()

    consulta = "INSERT INTO comentarios (id_usuario, id_video, contenido) VALUES (%s, %s, %s)"
    cursor.execute(consulta, (id_usuario, id_video, contenido))
    db.connection.commit()

    print("Comentario creado exitosamente.")
    cursor.close()

def leer_comentarios(id_publicacion):
    leer_publicaciones()
    cursor = db.connection.cursor()
    consulta = """SELECT c.id_comentario, u.nombre_usuario, c.contenido FROM comentarios c 
    JOIN usuarios u ON c.id_usuario = u.id_usuario  WHERE c.id_video = %s """
    cursor.execute(consulta, (id_publicacion,))
    comentarios = cursor.fetchall()

    if not comentarios:
        print("No hay comentarios para esta publicación.")
    else:
        print(f"Comentarios del video {id_publicacion}:")
        for comentario in comentarios:
            # Muestra ID, nombre de usuario y comentario
            print(f"{comentario[0]}. {comentario[1]}: {comentario[2]}")  

    cursor.close()

def actualizar_comentario(id_usuario):
    # Obtener y mostrar los comentarios del usuario
    cursor = db.connection.cursor()
    consulta = """
        SELECT id_comentario, contenido 
        FROM comentarios 
        WHERE id_usuario = %s
    """
    cursor.execute(consulta, (id_usuario,))
    comentarios = cursor.fetchall()

    # Verificar si el usuario tiene comentarios para actualizar
    if not comentarios:
        print("No tienes comentarios para editar.")
        cursor.close()
        return

    print("\nTus comentarios:")
    for comentario in comentarios:
        print(f"ID: {comentario[0]} | Contenido: {comentario[1]}")

    id_comentario = input("\nIntroduce el ID del comentario que deseas editar: ")

    if id_comentario not in [str(c[0]) for c in comentarios]:
        print("Error: Selecciona un comentario que te pertenezca.")
        cursor.close()
        return
    nuevo_contenido = input("Introduce el nuevo contenido del comentario: ")
    # Actualiza el comentario
    consulta_actualizacion = """
        UPDATE comentarios 
        SET contenido = %s 
        WHERE id_comentario = %s AND id_usuario = %s
    """
    cursor.execute(consulta_actualizacion, (nuevo_contenido, id_comentario, id_usuario))
    db.connection.commit()

    print("Comentario actualizado exitosamente.")
    cursor.close()

def eliminar_comentario(id_usuario):
    leer_publicaciones()
    id_publicacion = input("\nIntroduce el ID de la publicación para ver los comentarios: ")

    # Mostrar los comentarios asociados a esa publicación
    cursor = db.connection.cursor()
    consulta = """
        SELECT c.id_comentario, u.nombre_usuario, c.contenido
        FROM comentarios c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.id_video = %s
    """
    cursor.execute(consulta, (id_publicacion,))
    comentarios = cursor.fetchall()
    if not comentarios:
        print("No hay comentarios en esta publicación.")
        cursor.close()
        return

    print("\nComentarios disponibles:")
    for comentario in comentarios:
        print(f"ID: {comentario[0]} | Usuario: {comentario[1]} | Contenido: {comentario[2]}")

    # Solicita el ID del comentario a eliminar
    id_comentario = input("\nIntroduce el ID del comentario que deseas eliminar: ")

    # Verificar si el ID ingresado corresponde a un comentario válido
    if id_comentario not in [str(c[0]) for c in comentarios]:
        print("Error: Selecciona un comentario válido.")
        cursor.close()
        return
    consulta_eliminacion = "DELETE FROM comentarios WHERE id_comentario = %s"
    cursor.execute(consulta_eliminacion, (id_comentario,))
    db.connection.commit()

    print("Comentario eliminado exitosamente.")
    cursor.close()
