CREATE DATABASE IF NOT EXISTS tiktok_db;
USE tiktok_db;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE videos (
    id_video INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion VARCHAR(500),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE comentarios (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_video INT NOT NULL, 
    contenido VARCHAR(500) NOT NULL,
    fecha_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_video) REFERENCES videos(id_video)
);


--AJUSTES EN LA BASE DE DATOS PARA LA FUNCION CORRECTA DE LA FUNCION NUEVA CREDADA PARA LA ELIMINACION DE USUARIO
-- Seleccionar la base de datos
USE tiktok_db;

-- Eliminar claves foráneas de la tabla comentarios
ALTER TABLE comentarios DROP FOREIGN KEY comentarios_ibfk_1;
ALTER TABLE comentarios DROP FOREIGN KEY comentarios_ibfk_2;

-- Eliminar claves foráneas de la tabla videos
ALTER TABLE videos DROP FOREIGN KEY videos_ibfk_1;

-- Agregar las claves foráneas con ON DELETE CASCADE en la tabla videos
ALTER TABLE videos
ADD CONSTRAINT fk_videos_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;

-- Agregar las claves foráneas con ON DELETE CASCADE en la tabla comentarios
ALTER TABLE comentarios
ADD CONSTRAINT fk_comentarios_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
ADD CONSTRAINT fk_comentarios_videos FOREIGN KEY (id_video) REFERENCES videos(id_video) ON DELETE CASCADE;



--SEGUNDA OPCION SI NO FUNCIONA PERO NO RECOMENDADA PARA EMPRESAS GRANDES PERO PARA EL PROYECTO NO IMPORTA MUCHO
--ELIMINAR LA BASE DE DATOS Y CREARLA NUEVAMENTE CON LOS AJUSTES CON ELIMINACION EN CASCADA


-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS tiktok_db;

-- Seleccionar la base de datos
USE tiktok_db;

-- Crear la tabla usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla videos con la clave foránea a usuarios
CREATE TABLE videos (
    id_video INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion VARCHAR(500),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Crear la tabla comentarios con claves foráneas a usuarios y videos
CREATE TABLE comentarios (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_video INT NOT NULL, 
    contenido VARCHAR(500) NOT NULL,
    fecha_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_video) REFERENCES videos(id_video) ON DELETE CASCADE
);
