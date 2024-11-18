import db
from usuarios import registrar_usuario, iniciar_sesion
from publicaciones import crear_publicacion, leer_publicaciones, actualizar_publicacion, eliminar_publicacion
from comentarios import leer_comentarios, crear_comentario, actualizar_comentario, eliminar_comentario

# Para controlar el inicio de sesion
id_usuario = None

def menu():
    global id_usuario
    while True:
        print("""
1. Registrarse
2. Iniciar sesión
3. Ver publicaciones
4. Crear publicación
5. Editar publicación
6. Eliminar publicación
7. Ver comentarios
8. Crear comentario
9. Editar comentario
10. Eliminar comentario
0. Salir
        """)
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            id_usuario = iniciar_sesion()
        elif opcion == "3":
            leer_publicaciones()
        elif opcion == "4":
            if id_usuario:
                crear_publicacion(id_usuario)
            else:
                print("Debes iniciar sesión para realizar esta acción.")
        elif opcion == "5":
            if id_usuario:
                actualizar_publicacion(id_usuario)
            else:
                print("Debes iniciar sesión para realizar esta acción.")
        elif opcion == "6":
            if id_usuario:
                eliminar_publicacion(id_usuario)
            else:
                print("Debes iniciar sesión para realizar esta acción.")
        elif opcion == "7":
                leer_publicaciones() 
                id_publicacion = input("\nIntroduce el ID de la publicación para ver los comentarios: ")
                leer_comentarios(id_publicacion)  

        elif opcion == "8":
            if id_usuario:
                crear_comentario(id_usuario)
            else:
                print("Debes iniciar sesión para realizar esta acción.")
        elif opcion == "9":
            if id_usuario:
                actualizar_comentario(id_usuario)
            else:
                print("Debes iniciar sesión para realizar esta acción.")
        elif opcion == "10":
            if id_usuario:
                eliminar_comentario(id_usuario)
            else:
                print("Debes iniciar sesión para realizar esta acción.")
        elif opcion == "0":
            print("Saliendo del programa...")
            break   
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()
