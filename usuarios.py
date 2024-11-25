import hashlib
import db

class Usuario:
    def __init__(self, id_usuario=None, nombre_usuario=None, email=None, contrasena=None):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.contrasena = contrasena

    def registrar_usuario(self):
        while True:
            print("Escribe '1' para regresar al menú")
            nombre_usuario = input("Introduce tu nombre de usuario: ").strip()
            if nombre_usuario == '1':
                return  
            email = input("Introduce tu correo electrónico: ").strip()
            if email == '1':
                return  
            contrasena = input("Introduce tu contraseña: ").strip()
            if contrasena == '1':
                return  
            if not nombre_usuario or not email or not contrasena:
                print("Todos los campos son obligatorios. Por favor, rellena todos los campos.")
                continue
            if "@" not in email or "." not in email:
                print("Por favor, introduce un correo electrónico válido.")
                continue

            break

        contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
        cursor = db.connection.cursor()
        try:
            consulta = "INSERT INTO usuarios (nombre_usuario, email, contrasena) VALUES (%s, %s, %s)"
            cursor.execute(consulta, (nombre_usuario, email, contrasena_hasheada))
            db.connection.commit()
            print("Usuario registrado exitosamente.")
        except Exception as e:
            print("Error al registrar el usuario:", str(e))
        finally:
            cursor.close()

    def iniciar_sesion(self):
        while True:
            print("Escribe '1' para regresar al menú")
            email = input("Introduce tu correo electrónico: ").strip()
            if email == '1':
                return None  
            contrasena = input("Introduce tu contraseña : ").strip()
            if contrasena == '1':
                return None  

            contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
            cursor = None
            usuario = None

            try:
                cursor = db.connection.cursor()
                consulta = "SELECT id_usuario, nombre_usuario FROM usuarios WHERE email = %s AND contrasena = %s"
                cursor.execute(consulta, (email, contrasena_hasheada))
                usuario = cursor.fetchone()

                cursor.fetchall()

                if usuario:
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
                    cursor.close()

    def verificar_sesion(self):
        if self.id_usuario is None:
            print("Error: Debes iniciar sesión para realizar esta acción.")
            return False
        return True

    def eliminar_perfil(self):
        """Elimina el perfil del usuario actual."""
        if not self.verificar_sesion():
            return

        try:
            cursor = db.connection.cursor()
            confirmacion = input(f"¿Está seguro de que desea eliminar su perfil con ID {self.id_usuario}? (s/n): ").lower()
            if confirmacion == 's':
                consulta = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(consulta, (self.id_usuario,))
                db.connection.commit()
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
            cursor.close()

    def actualizar_perfil(self):
        """Actualiza la información del perfil del usuario en la base de datos."""
        if not self.verificar_sesion():
            return
        
        id_perfil = self.id_usuario  

        cursor = db.connection.cursor()

        try:
            consulta = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(consulta, (id_perfil,))
            perfil = cursor.fetchone()

            if not perfil:
                print("Perfil no encontrado.")
                return

            nuevo_nombre_usuario = input("Introduce el nuevo nombre de usuario (deja en blanco para no cambiarlo): ")
            if nuevo_nombre_usuario == "":
                nuevo_nombre_usuario = perfil[1]  

            nuevo_email = input("Introduce el nuevo correo electrónico (deja en blanco para no cambiarlo): ")
            if nuevo_email == "":
                nuevo_email = perfil[2]  

            consulta_update = """
            UPDATE usuarios
            SET nombre_usuario = %s, email = %s
            WHERE id_usuario = %s
            """
            cursor.execute(consulta_update, (nuevo_nombre_usuario, nuevo_email, id_perfil))
            db.connection.commit()

            print("Perfil actualizado exitosamente.")
        except Exception as e:
            print("Error al actualizar el perfil:", str(e))
        finally:
            cursor.close()

    def visualizar_perfiles(self):
        """Muestra todos los perfiles con su nombre de usuario y cantidad de videos subidos."""
        cursor = db.connection.cursor()
        try:
            consulta = """
            SELECT u.nombre_usuario, COUNT(p.id_video) AS cantidad_videos
            FROM usuarios u
            LEFT JOIN videos p ON u.id_usuario = p.id_usuario
            GROUP BY u.id_usuario
            """
            cursor.execute(consulta)
            perfiles = cursor.fetchall()

            print("\nPerfiles registrados:")
            for perfil in perfiles:
                print(f"- Nombre de usuario: {perfil[0]}, Número de videos: {perfil[1]}")

            nombre_buscar = input("\nIntroduce el nombre de usuario para buscar (deja vacío para no buscar): ").strip()
            if nombre_buscar:
                perfiles_encontrados = [
                    perfil for perfil in perfiles if nombre_buscar.lower() in perfil[0].lower()
                ]
                if perfiles_encontrados:
                    print("\nResultados de búsqueda:")
                    for perfil in perfiles_encontrados:
                        print(f"- Nombre de usuario: {perfil[0]}, Número de videos: {perfil[1]}")
                else:
                    print("\nNo se encontraron perfiles con ese nombre.")
        except Exception as e:
            print("Error al visualizar los perfiles:", str(e))
        finally:
            cursor.close()
