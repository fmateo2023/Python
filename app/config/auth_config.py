# Configuración de autenticación centralizada

# Rutas que NO requieren token JWT (whitelist)
PUBLIC_ENDPOINTS = [
    "/",
    "/docs",
    "/redoc", 
    "/openapi.json",
    "/api/auth/register",
    "/api/auth/login"
]

# Rutas que SÍ requieren token JWT (blacklist)
PROTECTED_ENDPOINTS = [
    "/api/protected/*",
    "/api/users/*",
    "/api/admin/*"
]