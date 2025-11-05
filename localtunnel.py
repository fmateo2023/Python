#!/usr/bin/env python3
"""
Alternativa usando localtunnel (no requiere instalación)
"""

import subprocess
import sys
import time
import json
import requests

def install_localtunnel():
    """Instala localtunnel via npm"""
    try:
        print("📦 Instalando localtunnel...")
        subprocess.run(['npm', 'install', '-g', 'localtunnel'], check=True)
        return True
    except:
        print("❌ Error: npm no encontrado")
        print("💡 Instala Node.js desde: https://nodejs.org")
        return False

def create_localtunnel(port=8000):
    """Crea túnel con localtunnel"""
    try:
        # Verificar si lt está disponible
        result = subprocess.run(['lt', '--version'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            if not install_localtunnel():
                return
        
        print(f"🔄 Creando túnel localtunnel para puerto {port}...")
        
        # Crear túnel
        cmd = ['lt', '--port', str(port)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
        
        # Esperar un poco para obtener la URL
        time.sleep(3)
        
        print(f"\n{'='*50}")
        print(f"✅ TÚNEL LOCALTUNNEL CREADO")
        print(f"💡 Ejecuta en otra terminal: python main.py")
        print(f"🏠 Local: http://127.0.0.1:{port}")
        print(f"{'='*50}")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Cerrando túnel...")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_localtunnel()