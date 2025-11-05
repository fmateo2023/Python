from fastapi import HTTPException, status, Request
from app.schemas.password_reset import PasswordResetRequest, VerifyOTPRequest, ResetPasswordRequest
from app.services.password_reset_service import PasswordResetService
from app.utils.logger import log_info, log_error, log_warning
from app.utils.security import rate_limiter
from typing import Dict

class PasswordResetController:
    """Controlador para recuperación de contraseñas"""
    
    @staticmethod
    def request_reset(reset_data: PasswordResetRequest, request: Request) -> Dict:
        """Maneja solicitud de recuperación de contraseña"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="password_reset")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Solicitud de recuperación de contraseña", email=reset_data.email, ip=client_ip)
            
            result = PasswordResetService.request_password_reset(reset_data.email)
            
            return result
            
        except Exception as e:
            log_error("Error en solicitud de recuperación", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def verify_otp(verify_data: VerifyOTPRequest, request: Request) -> Dict:
        """Maneja verificación de código OTP"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="verify_otp")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Verificación de código OTP", email=verify_data.email, ip=client_ip)
            
            result = PasswordResetService.verify_otp_code(verify_data.email, verify_data.otp_code)
            
            if not result["success"]:
                log_warning("Código OTP inválido", email=verify_data.email, ip=client_ip)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            log_error("Error verificando OTP", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def reset_password(reset_data: ResetPasswordRequest, request: Request) -> Dict:
        """Maneja actualización de contraseña"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="reset_password")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Actualización de contraseña", email=reset_data.email, ip=client_ip)
            
            result = PasswordResetService.reset_password(
                reset_data.email, 
                reset_data.otp_code, 
                reset_data.new_password
            )
            
            if not result["success"]:
                log_warning("Error actualizando contraseña", email=reset_data.email, ip=client_ip)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )
            
            log_info("Contraseña actualizada exitosamente", email=reset_data.email, ip=client_ip)
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            log_error("Error reseteando contraseña", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )