-- Actualizar la contraseña en texto plano para un usuario
-- Reemplaza 'nombre_del_usuario' con el nombre de usuario real
UPDATE usuarios 
SET contraseña = 'Admin123!' 
WHERE nombre_usuario = 'nombre_del_usuario';
