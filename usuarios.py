import hashlib
import db


class Usuario:
    def __init__(self, id_usuario=None, nombre_usuario=None, email=None, contrasena=None):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.contrasena = contrasena

    @staticmethod
    def hash_contrasena(contrasena):
        """Devuelve el hash SHA-256 de una contraseña."""
        return hashlib.sha256(contrasena.encode()).hexdigest()

    def registrar_usuario(self):
        """Registra un nuevo usuario en la base de datos."""
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

        contrasena_hasheada = self.hash_contrasena(contrasena)

        try:
            cursor = db.connection.cursor()
            consulta = "INSERT INTO usuarios (nombre_usuario, email, contrasena) VALUES (%s, %s, %s)"
            cursor.execute(consulta, (nombre_usuario, email, contrasena_hasheada))
            db.connection.commit()
            print("Usuario registrado exitosamente.")
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
        finally:
            cursor.close()

    def iniciar_sesion(self):
        """Inicia sesión en la aplicación."""
        while True:
            print("Escribe '1' para regresar al menú")
            email = input("Introduce tu correo electrónico: ").strip()
            if email == '1':
                return None
            contrasena = input("Introduce tu contraseña: ").strip()
            if contrasena == '1':
                return None

            contrasena_hasheada = self.hash_contrasena(contrasena)

            try:
                cursor = db.connection.cursor()
                consulta = "SELECT id_usuario, nombre_usuario FROM usuarios WHERE email = %s AND contrasena = %s"
                cursor.execute(consulta, (email, contrasena_hasheada))
                usuario = cursor.fetchone()

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
                cursor.close()

    def verificar_sesion(self):
        """Verifica si el usuario está autenticado."""
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
