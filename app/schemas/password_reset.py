from pydantic import BaseModel, EmailStr, validator
from app.utils.security import SecurityValidator

class PasswordResetRequest(BaseModel):
    """Schema para solicitar recuperación de contraseña"""
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    """Schema para verificar código OTP"""
    email: EmailStr
    otp_code: str
    
    @validator('otp_code')
    def validate_otp_code(cls, v):
        if not v or len(v) != 6 or not v.isdigit():
            raise ValueError('El código debe ser de 6 dígitos')
        return v

class ResetPasswordRequest(BaseModel):
    """Schema para resetear contraseña"""
    email: EmailStr
    otp_code: str
    new_password: str
    
    @validator('otp_code')
    def validate_otp_code(cls, v):
        if not v or len(v) != 6 or not v.isdigit():
            raise ValueError('El código debe ser de 6 dígitos')
        return v
    
    @validator('new_password')
    def validate_password(cls, v):
        is_valid, message = SecurityValidator.validate_password_strength(v)
        if not is_valid:
            raise ValueError(message)
        return v