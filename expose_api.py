#!/usr/bin/env python3
"""
Alternativas para exponer API sin ngrok
Opciones compatibles con antivirus empresariales
"""

import subprocess
import sys
import time
import socket
import requests

def get_local_ip():
    """Obtiene la IP local de la máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def check_port_open(port=8000):
    """Verifica si el puerto está abierto"""
    try:
        response = requests.get(f"http://127.0.0.1:{port}", timeout=2)
        return response.status_code == 200
    except:
        return False

def option_localtunnel():
    """Opción 1: LocalTunnel (más seguro para empresas)"""
    print("🔧 OPCIÓN 1: LocalTunnel")
    print("1. Instala Node.js: https://nodejs.org")
    print("2. Ejecuta: npm install -g localtunnel")
    print("3. Ejecuta: lt --port 8000")
    print("✅ Más seguro para antivirus empresariales\n")

def option_serveo():
    """Opción 2: Serveo (SSH tunnel)"""
    print("🔧 OPCIÓN 2: Serveo (SSH)")
    print("Ejecuta: ssh -R 80:localhost:8000 serveo.net")
    print("✅ Usa SSH estándar, no bloqueado por antivirus\n")

def option_localhost_run():
    """Opción 3: localhost.run"""
    print("🔧 OPCIÓN 3: localhost.run")
    print("Ejecuta: ssh -R 80:localhost:8000 localhost.run")
    print("✅ Alternativa SSH simple\n")

def option_network_access():
    """Opción 4: Acceso por red local"""
    local_ip = get_local_ip()
    print("🔧 OPCIÓN 4: Red Local")
    print(f"Tu IP local: {local_ip}")
    print(f"Acceso desde red: http://{local_ip}:8000")
    print("✅ Sin túneles, solo red local\n")

def option_port_forwarding():
    """Opción 5: Port Forwarding del router"""
    print("🔧 OPCIÓN 5: Port Forwarding")
    print("1. Accede a tu router (192.168.1.1)")
    print("2. Busca 'Port Forwarding' o 'Virtual Server'")
    print("3. Redirige puerto 8000 a tu IP local")
    print("4. Usa tu IP pública + puerto")
    print("✅ Solución permanente\n")

def option_cloud_deploy():
    """Opción 6: Deploy en la nube"""
    print("🔧 OPCIÓN 6: Deploy Gratuito")
    print("• Railway: railway.app (conecta GitHub)")
    print("• Render: render.com (conecta GitHub)")
    print("• Vercel: vercel.com (para FastAPI)")
    print("• Heroku: heroku.com (plan gratuito)")
    print("✅ Solución profesional\n")

def main():
    """Muestra todas las opciones disponibles"""
    print("🚀 ALTERNATIVAS PARA EXPONER TU API")
    print("=" * 50)
    
    # Verificar si la API está corriendo
    if check_port_open():
        print("✅ API detectada en puerto 8000")
    else:
        print("⚠️  Ejecuta primero: python main.py")
    
    print()
    
    option_localtunnel()
    option_serveo()
    option_localhost_run()
    option_network_access()
    option_port_forwarding()
    option_cloud_deploy()
    
    print("💡 RECOMENDACIÓN PARA EMPRESAS:")
    print("   Usa LocalTunnel o deploy en Railway/Render")

if __name__ == "__main__":
    main()