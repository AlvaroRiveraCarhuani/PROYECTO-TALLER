from usuarios import Usuario #importamos de el archivo usuarios.py la clase Usuario
from publicaciones import Publicacion  #importamos de el archivo publicaciones.py la clase Publicacion
from comentarios import Comentario #importamos de el archivo publicaciones.py la clase Publicacion

class Menu:
    #Constructor para instaciar la clase Usuario, Publicacion, Comentario
    def __init__(self):
        self.id_usuario = None
        self.usuario = Usuario()
        self.publicacion = Publicacion()
        self.comentario = Comentario()
#Funcion con bucle para verficar si el usuario esta logeado o no logeado
    def mostrar_menu(self):
        while True:
            if self.id_usuario:
                self.mostrar_menu_usuario_logueado()
            else:
                self.mostrar_menu_usuario_no_logueado()
#Fucnion para mostrar si el usuario esta logeado , menu para usuarios logueados 
    def mostrar_menu_usuario_logueado(self):
        """Menú para usuarios logueados."""
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
            11. Buscar video por título
            12. Visualizar perfiles de otros usuarios
            13. Actualizar mi perfil
            14. Eliminar mi perfil
            0. Salir
        """)
        opcion = input("Selecciona una opción: ")
        #Pedir al usuario por teclado para que se ejecute diferentes funciones de acuerdo a la opcion
        if opcion == "1":
            self.usuario.registrar_usuario() #Si elige la opcion 2 no ejecuta ninguna funciona ya que se logeo
        elif opcion == "2":
            print("Ya has iniciado sesión.")
        elif opcion == "3":
            self.publicacion.leer_publicaciones()
        elif opcion == "4":
            self.publicacion.crear_publicacion(self.id_usuario)
        elif opcion == "5":
            self.publicacion.actualizar_publicacion(self.id_usuario)
        elif opcion == "6":
            self.publicacion.eliminar_publicacion(self.id_usuario)
        elif opcion == "7":
            self.publicacion.leer_publicaciones()
            id_publicacion = input("\nIntroduce el ID de la publicación para ver los comentarios: ")
            self.comentario.leer_comentarios(id_publicacion)
        elif opcion == "8":
            self.comentario.crear_comentario(self.id_usuario)
        elif opcion == "9":
            self.comentario.actualizar_comentario(self.id_usuario)
        elif opcion == "10":
            self.comentario.eliminar_comentario(self.id_usuario)
        elif opcion == "11":
            self.publicacion.buscar_video_por_titulo()
        elif opcion == "12":
            self.usuario.visualizar_perfiles()  # Llama al método de visualizar perfiles
        elif opcion == "13":
            self.usuario.actualizar_perfil()
        elif opcion == "14":
            self.usuario.eliminar_perfil()
            if self.usuario.id_usuario is None:  # Verifica si el usuario se eliminó
                print("Tu perfil ha sido eliminado. Cerrando sesión...")
                self.id_usuario = None  # Reinicia la sesión para mandarlo al menu usuario no logeado
        elif opcion == "0":
            print("Saliendo del programa...")
            exit()
        else:
            print("Opción no válida. Inténtalo de nuevo.")

#menu par usuarios no logueados 

    def mostrar_menu_usuario_no_logueado(self):
        """Menú para usuarios no logueados."""
        print(""" 
            1. Registrarse
            2. Iniciar sesión
            3. Ver publicaciones
            4. Ver comentarios
            5. Crear comentario
            6. Buscar video por título
            7. Visualizar perfiles de otros usuarios
            0. Salir
        """)
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            self.usuario.registrar_usuario()
        elif opcion == "2":
            self.id_usuario = self.usuario.iniciar_sesion()
        elif opcion == "3":
            self.publicacion.leer_publicaciones()
        elif opcion == "4":
            self.publicacion.leer_publicaciones()
            id_publicacion = input("\nIntroduce el ID de la publicación para ver los comentarios: ")
            self.comentario.leer_comentarios(id_publicacion)
        elif opcion == "5":
            print("\nDebes registrarte o iniciar sesión para crear un comentario.")
            self.mostrar_menu_autenticacion()
        elif opcion == "6":
            self.publicacion.buscar_video_por_titulo()
        elif opcion == "7":
            self.usuario.visualizar_perfiles()  # Llama al método de visualizar perfiles
        elif opcion == "0":
            print("Saliendo de tiktok...")
            exit()
        else:
            print("Opción no válida. Inténtalo de nuevo.")
    #Funcion usada en el menu de usuario no logeado, cuando quiera crear un comentario sin iniciar sesion mandarlo esta funcion
    def mostrar_menu_autenticacion(self):
        """Menú para redirigir a registro o inicio de sesión."""
        while True:
            print(""" 
                1. Registrarse
                2. Iniciar sesión
                0. Volver al menú principal
            """)
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.usuario.registrar_usuario()
                break
            elif opcion == "2":
                self.id_usuario = self.usuario.iniciar_sesion()
                break
            elif opcion == "0":
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
                                
if __name__ == "__main__":
    menu = Menu()
    menu.mostrar_menu()
