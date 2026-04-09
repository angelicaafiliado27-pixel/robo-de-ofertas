import requests
import time
import threading
import http.server
import socketserver

# --- CONFIGURAÇÕES DE TESTE ---
TOKEN_TELEGRAM = "8714375855:AAHULALUU7p9hcp1YUSBAl_bDn5vPbzvZdM"
CANAL_DESTINO = "@ofertasmaepratica"

def enviar_teste( ):
    print("Enviando mensagem de teste para o Telegram...")
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CANAL_DESTINO, 
        "text": "🚀 *TESTE DE CONEXÃO:* O Robô da Angelica está ATIVO e pronto para postar ofertas!",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload )
        print(f"Resposta do Telegram: {response.text}")
    except Exception as e:
        print(f"Erro ao enviar: {e}")

if __name__ == "__main__":
    # Inicia o servidor para o Render não dar erro
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    
    # Envia a mensagem de teste na hora
    enviar_teste()
    
    # Mantém o robô vivo
    while True:
        time.sleep(600)
