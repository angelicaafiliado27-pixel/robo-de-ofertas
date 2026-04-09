import requests
import time
import threading
import http.server
import socketserver
from bs4 import BeautifulSoup

# --- CONFIGURAÇÕES DO SEU ROBÔ ---
TOKEN_TELEGRAM = "8714375855:AAHULALUU7p9hcp1YUSBAl_bDn5vPbzvZdM"
CANAL_DESTINO = "@ofertasmaepratica" # O canal onde o teste funcionou
CANAL_FONTE = "https://t.me/s/jgtechofertas" # Fonte das melhores ofertas do Brasil

TAGS = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

def enviar_telegram(mensagem ):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CANAL_DESTINO, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload )
    except: pass

def converter_link(link_original):
    link = link_original.lower()
    if 'amazon.com.br' in link:
        conector = '&' if '?' in link else '?'
        return f"{link_original}{conector}tag={TAGS['amazon']}"
    elif 'shopee.com.br' in link:
        conector = '&' if '?' in link else '?'
        return f"{link_original}{conector}smtt=0.0.{TAGS['shopee']}"
    elif 'mercadolivre.com.br' in link:
        conector = '&' if '?' in link else '?'
        return f"{link_original}{conector}utm_source=afiliado&utm_campaign={TAGS['mercadolivre']}"
    elif 'magazineluiza.com.br' in link:
        return f"https://www.magazinevoce.com.br/{TAGS['magalu']}/"
    return link_original

def buscar_ofertas( ):
    print("🚀 Robô de Ofertas Maepratica Iniciado!")
    ultima_oferta = ""
    
    while True:
        try:
            print("🔎 Verificando novas ofertas relâmpago...")
            res = requests.get(CANAL_FONTE, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
            
            if mensagens:
                msg = mensagens[-1] # Pega a oferta mais recente postada
                texto_elem = msg.find('div', class_='tgme_widget_message_text')
                
                if texto_elem:
                    links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                    if links and links[0] != ultima_oferta:
                        link_com_comissao = converter_link(links[0])
                        
                        # Monta a mensagem bonita para o seu canal
                        msg_final = (
                            "🔥 *OFERTA RELÂMPAGO ENCONTRADA!*\n\n"
                            f"🔗 *COMPRE AQUI:* {link_com_comissao}\n\n"
                            "⚠️ *Aproveite! Oferta por tempo limitado ou até durar o estoque.*"
                        )
                        
                        enviar_telegram(msg_final)
                        ultima_oferta = links[0]
                        print(f"✅ Oferta enviada: {links[0]}")
        except Exception as e:
            print(f"Erro ao buscar: {e}")
            
        # Espera 1 hora (3600 segundos) para a próxima verificação
        # Se quiser que seja mais rápido, mude para 1800 (30 min) ou 600 (10 min)
        time.sleep(3600) 

if __name__ == "__main__":
    # Servidor para o Render não dar erro
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    
    # Envia aviso de que o robô reiniciou
    enviar_telegram("🤖 *Robô Maepratica Atualizado!* Monitorando ofertas a cada 1 hora.")
    
    # Inicia o loop de busca
    buscar_ofertas()
