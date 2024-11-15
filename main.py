from usuarios import registrar_usuario, iniciar_sesion
from publicaciones import crear_publicacion, leer_publicaciones, actualizar_publicacion, eliminar_publicacion

id_usuario = None

def menu():
    global id_usuario
    while True:
        print(""" 
1. Registrarse
2. Iniciar sesión
3. Crear publicación
4. Ver publicaciones
5. Editar publicación
6. Eliminar publicación
0. Salir
        """)
        opcion = input("Selecciona una opción: ")

        if opcion == "1":

            nombre_usuario = "usuario_prueba"
            email = "usuario@ejemplo.com"
            contrasena = "contrasena_segura123"
            registrar_usuario(nombre_usuario, email, contrasena)
        elif opcion == "2":
            if not id_usuario:  
                email = "usuario@ejemplo.com"
                contrasena = "contrasena_segura123"
                id_usuario = iniciar_sesion(email, contrasena)
            else:
                print(f"Ya estás logueado con ID de usuario: {id_usuario}")
        elif opcion == "3":
            if id_usuario:
                crear_publicacion(id_usuario)
            else:
                print("Debes iniciar sesión para crear una publicación.")
        elif opcion == "4":
            leer_publicaciones()
        elif opcion == "5":
            if id_usuario:
                actualizar_publicacion(id_usuario)
            else:
                print("Debes iniciar sesión para editar una publicación.")
        elif opcion == "6":
            if id_usuario:
                eliminar_publicacion(id_usuario)
            else:
                print("Debes iniciar sesión para eliminar una publicación.")
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Llamada al menú
menu()
