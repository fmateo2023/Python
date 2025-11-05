from fastapi import APIRouter, Depends
from app.utils.auth_middleware import get_current_user
from app.utils.logger import log_info
from typing import Dict

router = APIRouter(prefix="/api/protected", tags=["Protected Routes"])

@router.get("/profile")
async def get_profile(current_user: Dict = Depends(get_current_user)):
    """
    Endpoint protegido - Obtiene perfil del usuario autenticado
    
    Requiere JWT token válido en el header Authorization: Bearer <token>
    """
    log_info("Acceso a perfil", user_id=current_user['id'])
    
    return {
        "success": True,
        "message": "Perfil obtenido exitosamente",
        "data": {
            "id": current_user['id'],
            "nombre": current_user['nombre'],
            "email": current_user['email'],
            "telefono": current_user['telefono']
        }
    }

@router.get("/dashboard")
async def get_dashboard(current_user: Dict = Depends(get_current_user)):
    """
    Endpoint protegido - Dashboard del usuario
    
    Requiere JWT token válido en el header Authorization: Bearer <token>
    """
    log_info("Acceso a dashboard", user_id=current_user['id'])
    
    return {
        "success": True,
        "message": "Dashboard cargado exitosamente",
        "data": {
            "user": {
                "id": current_user['id'],
                "nombre": current_user['nombre']
            },
            "stats": {
                "login_count": 1,
                "last_login": "2024-01-15 10:30:00"
            }
        }
    }