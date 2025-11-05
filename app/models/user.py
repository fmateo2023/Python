from app.config.database import get_db_connection
from app.utils.logger import log_info, log_error
from typing import Optional, Dict

class User:
    """Modelo para operaciones de usuario en la base de datos"""
    
    @staticmethod
    def create(nombre: str, email: Optional[str], telefono: Optional[str], hashed_password: str) -> Dict:
        """Crea un nuevo usuario en la base de datos"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                log_info("Creando usuario en BD", email=email, telefono=telefono[:4] + "****" if telefono else None)
                cursor.execute(
                    "INSERT INTO users (nombre, email, telefono, password) VALUES (%s, %s, %s, %s)",
                    (nombre, email, telefono, hashed_password)
                )
                user_id = cursor.lastrowid
                connection.commit()
                log_info("Usuario creado en BD", user_id=user_id)
                return {
                    "id": user_id,
                    "nombre": nombre,
                    "email": email,
                    "telefono": telefono
                }
        except Exception as e:
            log_error("Error creando usuario en BD", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        """Obtiene un usuario por email"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                return cursor.fetchone()
        finally:
            connection.close()
    
    @staticmethod
    def get_by_telefono(telefono: str) -> Optional[Dict]:
        """Obtiene un usuario por teléfono"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE telefono = %s", (telefono,))
                return cursor.fetchone()
        finally:
            connection.close()
    
    @staticmethod
    def get_by_email_or_telefono(email: Optional[str], telefono: Optional[str]) -> Optional[Dict]:
        """Obtiene un usuario por email o teléfono"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                if email and telefono:
                    cursor.execute("SELECT * FROM users WHERE email = %s OR telefono = %s", (email, telefono))
                elif email:
                    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                elif telefono:
                    cursor.execute("SELECT * FROM users WHERE telefono = %s", (telefono,))
                else:
                    return None
                return cursor.fetchone()
        finally:
            connection.close()
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por ID"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, email, telefono FROM users WHERE id = %s", (user_id,))
                return cursor.fetchone()
        finally:
            connection.close()
    
    @staticmethod
    def update_password(user_id: int, hashed_password: str) -> bool:
        """Actualiza la contraseña de un usuario"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET password = %s WHERE id = %s",
                    (hashed_password, user_id)
                )
                connection.commit()
                log_info("Contraseña actualizada en BD", user_id=user_id)
                return cursor.rowcount > 0
        except Exception as e:
            log_error("Error actualizando contraseña en BD", error=e)
            return False
        finally:
            connection.close()