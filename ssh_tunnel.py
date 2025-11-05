#!/usr/bin/env python3
"""
Túneles SSH seguros para antivirus empresariales
Alternativas que no son bloqueadas
"""

import subprocess
import sys
import time

def serveo_tunnel(port=8000):
    """Crea túnel con Serveo (SSH)"""
    print(f"🔄 Creando túnel SSH con Serveo...")
    print("💡 Serveo usa SSH estándar, no es bloqueado por antivirus")
    
    try:
        cmd = ['ssh', '-R', f'80:localhost:{port}', 'serveo.net']
        print(f"Ejecutando: {' '.join(cmd)}")
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
        
        print(f"\n{'='*50}")
        print(f"✅ TÚNEL SSH SERVEO INICIADO")
        print(f"🏠 Local: http://127.0.0.1:{port}")
        print(f"🌐 Público: Verifica la salida del comando")
        print(f"💡 Ejecuta en otra terminal: python main.py")
        print(f"{'='*50}")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Cerrando túnel...")
            process.terminate()
            
    except FileNotFoundError:
        print("❌ SSH no encontrado")
        print("💡 Instala OpenSSH desde Windows Features")
    except Exception as e:
        print(f"❌ Error: {e}")

def localhost_run_tunnel(port=8000):
    """Crea túnel con localhost.run"""
    print(f"🔄 Creando túnel con localhost.run...")
    
    try:
        cmd = ['ssh', '-R', f'80:localhost:{port}', 'localhost.run']
        print(f"Ejecutando: {' '.join(cmd)}")
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
        
        print(f"\n{'='*50}")
        print(f"✅ TÚNEL LOCALHOST.RUN INICIADO")
        print(f"🏠 Local: http://127.0.0.1:{port}")
        print(f"💡 Ejecuta en otra terminal: python main.py")
        print(f"{'='*50}")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Cerrando túnel...")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_options():
    """Muestra opciones disponibles"""
    print("🔧 TÚNELES SSH SEGUROS")
    print("=" * 30)
    print("1. Serveo (Opción 1)")
    print("2. localhost.run (Opción 2)")
    print("3. Red local (Opción 3)")
    print("=" * 30)
    
    choice = input("Selecciona opción (1-3): ").strip()
    
    if choice == "1":
        serveo_tunnel()
    elif choice == "2":
        localhost_run_tunnel()
    elif choice == "3":
        print("💡 Ejecuta: python network_server.py")
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    show_options()