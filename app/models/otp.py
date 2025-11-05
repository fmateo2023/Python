from app.config.database import get_db_connection
from app.utils.logger import log_info, log_error
from typing import Optional, Dict
from datetime import datetime, timedelta
import random

class OTP:
    """Modelo para operaciones de OTP en la base de datos"""
    
    @staticmethod
    def create(email: str, otp_code: str) -> bool:
        """Crea un nuevo OTP en la base de datos"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Eliminar OTPs anteriores del mismo email
                cursor.execute("DELETE FROM otp_codes WHERE email = %s", (email,))
                
                # Crear nuevo OTP con expiración de 10 minutos
                expires_at = datetime.now() + timedelta(minutes=10)
                cursor.execute(
                    "INSERT INTO otp_codes (email, otp_code, expires_at) VALUES (%s, %s, %s)",
                    (email, otp_code, expires_at)
                )
                connection.commit()
                log_info("OTP creado", email=email, expires_at=expires_at)
                return True
        except Exception as e:
            log_error("Error creando OTP", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def verify(email: str, otp_code: str) -> bool:
        """Verifica si el OTP es válido y no ha expirado"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM otp_codes WHERE email = %s AND otp_code = %s AND expires_at > NOW()",
                    (email, otp_code)
                )
                result = cursor.fetchone()
                
                if result:
                    log_info("OTP verificado exitosamente", email=email)
                    return True
                else:
                    log_info("OTP inválido o expirado", email=email)
                    return False
        except Exception as e:
            log_error("Error verificando OTP", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def delete(email: str) -> bool:
        """Elimina el OTP después de ser usado"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM otp_codes WHERE email = %s", (email,))
                connection.commit()
                log_info("OTP eliminado", email=email)
                return True
        except Exception as e:
            log_error("Error eliminando OTP", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def generate_code() -> str:
        """Genera un código OTP de 6 dígitos"""
        return str(random.randint(100000, 999999))