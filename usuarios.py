import hashlib #Importamos libreria para hashear las contrasenas de usuarios
import db #Importamos db.py 

class Usuario:
    #Constructor de la clase Usuario
    def __init__(self, id_usuario=None, nombre_usuario=None, email=None, contrasena=None):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.contrasena = contrasena

    def registrar_usuario(self):
        while True: #Bucle infinito hasta que seleccione una opcion valida
            #Si el usuario ingresa 1 retorna al menu
            print("Escribe '1' para regresar al menú")
            #Pedimos al usuario por teclado el nombre, email y contrasena
            nombre_usuario = input("Introduce tu nombre de usuario: ").strip()
            if nombre_usuario == '1':
                return  
            email = input("Introduce tu correo electrónico: ").strip()
            if email == '1':
                return  
            contrasena = input("Introduce tu contraseña: ").strip()
            if contrasena == '1':
                return  
            #Si el usuario no ingreso ninguna seccion se realiza la peticion nuevamente
            if not nombre_usuario or not email or not contrasena:
                print("Todos los campos son obligatorios. Por favor, rellena todos los campos.")
                continue
            #Si el usuario en el email no ingresa @ o . no es valido por que no es un correo electronico
            if "@" not in email or "." not in email:
                print("Por favor, introduce un correo electrónico válido.")
                continue
            #Break Finalizar
            break
        #Creamos una variable para poder hashear la contrasena con la libreria haslib
        contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
        cursor = db.connection.cursor() #Inicializamos el cursor para realizar funciones en la BD
        try:
            consulta = "INSERT INTO usuarios (nombre_usuario, email, contrasena) VALUES (%s, %s, %s)"
            cursor.execute(consulta, (nombre_usuario, email, contrasena_hasheada)) #Ejecutamos el cursor
            db.connection.commit() #Guardamos los cambios realizados con el cursor
            print("Usuario registrado exitosamente.")
        except Exception as e: #Manejo de errores
            print("Error al registrar el usuario:", str(e))
        finally: # Cerramos el cursor para realizar otros cursores
            cursor.close()

    def iniciar_sesion(self):
        while True: #Bucle infinito hasta que seleccione una opcion valida 
            print("Escribe '1' para regresar al menú")
            #Pedimos por teclado el email y contrasena
            email = input("Introduce tu correo electrónico: ").strip()
            if email == '1':
                return None  
            contrasena = input("Introduce tu contraseña : ").strip()
            if contrasena == '1':
                return None  
            #almacenamos la contrasena hasheada con la libreria
            contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
            cursor = None #inicializamos el cursor en none
            usuario = None #inicializamos el usuario en none
            
            try:
                #Realizamos un cursor para realizar funciones en la BD
                cursor = db.connection.cursor() 
                #Realizamos la consulta a la base de datos
                consulta = "SELECT id_usuario, nombre_usuario FROM usuarios WHERE email = %s AND contrasena = %s"
                cursor.execute(consulta, (email, contrasena_hasheada)) #Ejecutamos la consulta
                usuario = cursor.fetchone() #Utilizamos fetchone para obtener solo una fila que de la consulta

                if usuario:
                    #Tuplas usuario[1] y usuario[0]
                    print(f"Bienvenido, {usuario[1]}!")
                    self.id_usuario = usuario[0]  # Guardamos el ID del usuario
                    return self.id_usuario  # Retorna el ID del usuario

                print("Correo electrónico o contraseña incorrectos.")
                return None
            except Exception as e:
                print(f"Error al iniciar sesión: {e}")
                return None
            finally:
                if cursor:
                    cursor.close() #Cerramos el cursor
#Funcion para verificar si el usuario esta logeado o tiene un id_suario
    def verificar_sesion(self):
        if self.id_usuario is None:
            print("Error: Debes iniciar sesión para realizar esta acción.")
            return False
        return True

    def eliminar_perfil(self):
        """Elimina el perfil del usuario actual."""
        if not self.verificar_sesion(): #Ejecutamos la funcion verificar_usuario para saber si el usuario tiene un id para eliminar
            return

        try:
            cursor = db.connection.cursor() #Cursor para poder realizar funciones en la BD
            #Pedimos por teclado al usuario si desea eliminar el perfil
            confirmacion = input(f"¿Está seguro de que desea eliminar su perfil con ID {self.id_usuario}? (s/n): ").lower()
            if confirmacion == 's': 
                consulta = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(consulta, (self.id_usuario,)) #ejecutamos el cursor
                db.connection.commit() #Guardamos los cambios del cursor 
                print("Perfil eliminado exitosamente.")
                # Resetea los datos del usuario después de la eliminación
                self.id_usuario = None
                self.nombre_usuario = None
                self.email = None
                self.contrasena = None
            else:
                print("Operación cancelada.")
        except Exception as e:
            print(f"Error al eliminar el perfil: {e}")
        finally:
            cursor.close() #Cerramos el cursor

    def actualizar_perfil(self):
        """Actualiza la información del perfil del usuario en la base de datos."""
        if not self.verificar_sesion(): #Verificamos si el usuario inicio sesion
            return
        
        id_perfil = self.id_usuario  
        cursor = db.connection.cursor() #Cursor para hacer funciones en la BD

        try:
            #Almacenamos la consulta de usuarios para actualizar el perfil de usuario
            consulta = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(consulta, (id_perfil,)) #Ejecutamos la consulta
            perfil = cursor.fetchone() #Fetchone ya que editamos solo un usuario

            if not perfil:
                print("Perfil no encontrado.")
                return
            #Pedimos por teclado el nuevo nombre y email
            nuevo_nombre_usuario = input("Introduce el nuevo nombre de usuario (deja en blanco para no cambiarlo): ")
            if nuevo_nombre_usuario == "":  #si el usuario no ingresa nada, no modificamos nada del nombre usuario
                nuevo_nombre_usuario = perfil[1]  #almacenamos el nombre sin cambios 

            nuevo_email = input("Introduce el nuevo correo electrónico (deja en blanco para no cambiarlo): ")
            if nuevo_email == "": #si el usuario no ingresa nada, no modificamos nada del nombre usuario
                nuevo_email = perfil[2]  #Almacenamos el email sin cambios

            consulta_update = """ 
            UPDATE usuarios
            SET nombre_usuario = %s, email = %s
            WHERE id_usuario = %s
            """ #Ejecutamos el update a la base de datos con los cambios realizados
            cursor.execute(consulta_update, (nuevo_nombre_usuario, nuevo_email, id_perfil))
            db.connection.commit() #Guardamos los cambios realizados

            print("Perfil actualizado exitosamente.")
        except Exception as e:
            print("Error al actualizar el perfil:", str(e))
        finally:
            cursor.close() #Cerramos el cursor
    def visualizar_perfiles(self):
        """Muestra todos los perfiles con su nombre de usuario y cantidad de videos subidos."""
        cursor = db.connection.cursor() #Usamos un cursor para realizar funciones en la BD
        try: #Realizamos la consulta usando join para mostrar el nnombre_usuario y la cantidad de videos del usuario
            consulta = """
            SELECT u.nombre_usuario, COUNT(p.id_video) AS cantidad_videos
            FROM usuarios u
            LEFT JOIN videos p ON u.id_usuario = p.id_usuario
            GROUP BY u.id_usuario
            """
            cursor.execute(consulta) #Ejecutamos la consulta
            perfiles = cursor.fetchall() #Fetchall para mostrar todos los datos de la consulta

            print("\nPerfiles registrados:")
            for perfil in perfiles: #For para mmostrar todos los perfiles registrados
                print(f"- Nombre de usuario: {perfil[0]}, Número de videos: {perfil[1]}")
            #Pedimos al usuario si desea buscar un usuario por su nombre
            nombre_buscar = input("\nIntroduce el nombre de usuario para buscar (deja vacío para no buscar): ").strip()
            if nombre_buscar: #Condicional y bucle de busqueda para encontrar el nombre ingresado por teclado
                perfiles_encontrados = [ 
                    perfil for perfil in perfiles if nombre_buscar.lower() in perfil[0].lower()
                ]
                if perfiles_encontrados:
                    print("\nResultados de búsqueda:") #Imprimir los datos de la busqueda
                    for perfil in perfiles_encontrados:
                        print(f"- Nombre de usuario: {perfil[0]}, Número de videos: {perfil[1]}")
                else:
                    print("\nNo se encontraron perfiles con ese nombre.")
        except Exception as e:
            print("Error al visualizar los perfiles:", str(e))
        finally:
            cursor.close() #Cerramos el cursor
