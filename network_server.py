#!/usr/bin/env python3
"""
Servidor que expone la API en la red local
Alternativa segura para antivirus empresariales
"""

import uvicorn
import socket
from io import StringIO

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

def get_network_info():
    """Obtiene información de red"""
    try:
        # Obtener IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Obtener hostname
        hostname = socket.gethostname()
        
        return local_ip, hostname
    except:
        return "127.0.0.1", "localhost"

def generate_qr_code(url):
    """Genera código QR para acceso móvil"""
    if not QR_AVAILABLE:
        return "📱 QR no disponible (instala: pip install qrcode)"
    
    try:
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        
        # Crear QR en texto
        qr_text = StringIO()
        qr.print_ascii(out=qr_text)
        return qr_text.getvalue()
    except:
        return "📱 Error generando QR"

def start_network_server(port=8000):
    """Inicia servidor accesible desde la red"""
    local_ip, hostname = get_network_info()
    
    print("🌐 SERVIDOR DE RED INICIADO")
    print("=" * 50)
    print(f"🏠 Local: http://127.0.0.1:{port}")
    print(f"🌍 Red: http://{local_ip}:{port}")
    print(f"📱 Móvil: http://{hostname}.local:{port}")
    print(f"📚 Docs: http://{local_ip}:{port}/docs")
    print("=" * 50)
    
    # Generar QR para móviles
    mobile_url = f"http://{local_ip}:{port}"
    qr_code = generate_qr_code(mobile_url)
    print("📱 CÓDIGO QR PARA MÓVIL:")
    print(qr_code)
    
    print("💡 INSTRUCCIONES:")
    print("• Conecta dispositivos a la misma WiFi")
    print("• Usa las URLs de arriba para acceder")
    print("• Escanea el QR con tu móvil")
    print("=" * 50)
    
    # Importar y ejecutar la app
    from main import app
    uvicorn.run(
        app, 
        host="0.0.0.0",  # Permite acceso desde red
        port=port, 
        log_level="info"
    )

if __name__ == "__main__":
    start_network_server()