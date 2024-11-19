import hashlib
import db

def registrar_usuario():
    while True:
        nombre_usuario = input("Introduce tu nombre de usuario: ").strip()
        email = input("Introduce tu correo electrónico: ").strip()
        contrasena = input("Introduce tu contraseña: ").strip()

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

def iniciar_sesion():
    email = input("Introduce tu correo electrónico: ")
    contrasena = input("Introduce tu contraseña: ")

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
            return usuario[0]  

        print("Correo electrónico o contraseña incorrectos.")
        return None
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None
    finally:
        if cursor:
            cursor.close()  
