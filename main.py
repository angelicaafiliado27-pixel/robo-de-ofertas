import requests
import time
import threading
import http.server
import socketserver

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = "8714375855:AAHULALUU7p9hcp1YUSBAl_bDn5vPbzvZdM"
# Tentaremos postar no canal público primeiro
CANAL_DESTINO = "@ofertasmaepratica"

def enviar_teste( ):
    print("\n--- INICIANDO TESTE DE ENVIO ---")
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CANAL_DESTINO, 
        "text": "🚀 *TESTE DE CONEXÃO:* O Robô da Angelica está ATIVO e pronto para postar ofertas!",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload )
        print(f"Resposta do Telegram: {response.text}")
        if response.status_code == 200:
            print("✅ SUCESSO! A mensagem deve ter aparecido no seu Telegram.")
        else:
            print("❌ ERRO: Verifique se o robô é administrador do canal.")
    except Exception as e:
        print(f"Erro ao enviar: {e}")

if __name__ == "__main__":
    # Servidor para o Render
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    
    # Tenta enviar a mensagem de teste
    enviar_teste()
    
    # Mantém o robô vivo
    while True:
        time.sleep(600)
