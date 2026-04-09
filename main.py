import requests
from bs4 import BeautifulSoup
import time
import threading
import http.server
import socketserver

# --- CONFIGURAÇÕES FINAIS ---
API_URL = "https://evolution-api-production-6079.up.railway.app"
API_KEY = "123456" # Use a chave que você definiu no Railway (se mudou, coloque aqui )
GROUP_ID = "EvCF9MRL4PGINDWiKlTgA8@g.us"
INSTANCE = "meu-robo"

TAGS = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

def enviar_whatsapp(texto):
    url = f"{API_URL}/message/sendText/{INSTANCE}"
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    payload = {"number": GROUP_ID, "text": texto}
    try:
        requests.post(url, json=payload, headers=headers)
    except: pass

def buscar_ofertas():
    print("🚀 Robô de Ofertas Iniciado!")
    while True:
        try:
            res = requests.get("https://t.me/s/jgtechofertas", headers={'User-Agent': 'Mozilla/5.0'} )
            soup = BeautifulSoup(res.text, 'html.parser')
            mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
            for msg in mensagens:
                texto_elem = msg.find('div', class_='tgme_widget_message_text')
                if not texto_elem: continue
                links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                if links:
                    # Exemplo simples de conversão (Amazon)
                    link = links[0]
                    if "amazon" in link: link += f"?tag={TAGS['amazon']}"
                    msg_final = f"🔥 *OFERTA ENCONTRADA!*\n\n🔗 *COMPRE AQUI:* {link}"
                    enviar_whatsapp(msg_final)
        except: pass
        time.sleep(600)

def rodar_servidor():
    socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=buscar_ofertas, daemon=True).start()
    rodar_servidor()
