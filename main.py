import requests
from bs4 import BeautifulSoup
import time
import threading
import http.server
import socketserver

# --- SUAS TAGS JÁ CONFIGURADAS ---
TAGS_AFILIADO = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

CANAL_FONTE = "https://t.me/s/jgtechofertas"

# --- FUNÇÃO DO ROBÔ (O QUE ELE FAZ ) ---
def buscar_e_postar():
    print("🚀 Robô de Ofertas Iniciado!")
    while True:
        print(f"[{time.strftime('%H:%M:%S')}] Verificando novas ofertas...")
        try:
            response = requests.get(CANAL_FONTE, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
            
            for msg in mensagens:
                texto_elem = msg.find('div', class_='tgme_widget_message_text')
                if not texto_elem: continue
                links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                if links:
                    print(f"Oferta encontrada! Link: {links[0]}")
                    # Aqui você conectará sua API de WhatsApp depois
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(300)

# --- SERVIDOR DE MENTIRA (PARA O RENDER NÃO DAR ERRO) ---
def rodar_servidor_falso():
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT ), Handler) as httpd:
        print(f"Servidor de mentira rodando na porta {PORT}" )
        httpd.serve_forever( )

if __name__ == "__main__":
    # Inicia o robô em uma linha separada
    threading.Thread(target=buscar_e_postar, daemon=True).start()
    # Inicia o servidor que o Render exige
    rodar_servidor_falso()
