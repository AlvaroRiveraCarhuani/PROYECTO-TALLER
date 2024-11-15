# main.py
from usuarios import registrar_usuario, iniciar_sesion

# Para controlar el inicio de sesión
id_usuario = None

def menu():
    global id_usuario
    while True:
        print("""
1. Registrarse
2. Iniciar sesión
0. Salir
        """)
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            # Simulación de la creación del usuario con valores predefinidos
            nombre_usuario = "usuario_prueba"
            email = "usuario@ejemplo.com"
            contrasena = "contrasena_segura123"
            registrar_usuario(nombre_usuario, email, contrasena)
        elif opcion == "2":
            # Simulación del inicio de sesión con los mismos datos
            if not id_usuario:  # Si el usuario no está logueado
                email = "usuario@ejemplo.com"
                contrasena = "contrasena_segura123"
                id_usuario = iniciar_sesion(email, contrasena)
            else:
                print(f"Ya estás logueado con ID de usuario: {id_usuario}")
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()
