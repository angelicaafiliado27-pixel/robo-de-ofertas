import requests
import time
import threading
import http.server
import socketserver

# --- CONFIGURAÇÕES ---
API_URL = "https://evolution-api-production-6079.up.railway.app"
API_KEY = "d5XnvG8BRGpnLAQO8zkEvLn0"
INSTANCE = "meu-robo"

def gerar_qr_code( ):
    print("\n--- GERANDO QR CODE PARA VOCÊ ---")
    url = f"{API_URL}/instance/connect/{INSTANCE}"
    headers = {"apikey": API_KEY}
    try:
        # Tenta criar a instância primeiro caso ela tenha sumido
        requests.post(f"{API_URL}/instance/create", 
                     json={"instanceName": INSTANCE, "token": API_KEY, "qrcode": True}, 
                     headers=headers)
        
        # Imprime o link direto do QR Code no log
        print(f"\n👉 CLIQUE NESTE LINK PARA ESCANEAR O QR CODE:\n{url}\n")
    except Exception as e:
        print(f"Erro ao gerar QR: {e}")

def buscar_ofertas():
    while True:
        print(f"[{time.strftime('%H:%M:%S')}] Robô vigiando ofertas...")
        # (Lógica de busca simplificada para teste)
        time.sleep(600)

if __name__ == "__main__":
    # Inicia o servidor para o Render não dar erro
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    
    # Gera o QR Code no log
    gerar_qr_code()
    
    # Inicia o robô
    buscar_ofertas()
