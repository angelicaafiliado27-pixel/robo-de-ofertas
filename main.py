import requests
import time
import threading
import http.server
import socketserver
from bs4 import BeautifulSoup

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = "8714375855:AAHULALUU7p9hcp1YUSBAl_bDn5vPbzvZdM"
CANAL_DESTINO = "@ofertasmaepratica" 
CANAL_FONTE = "https://t.me/s/jgtechofertas" 

TAGS = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

# Filtro ampliado para garantir que as ofertas cheguem!
PALAVRAS_CHAVE = [
    'casa', 'cozinha', 'banheiro', 'quarto', 'lavanderia', 'limpeza', 'organizador',
    'pote', 'mop', 'aspirador', 'airfryer', 'fritadeira', 'cafeteira', 'panela',
    'geladeira', 'maquina', 'lavar', 'infantil', 'bebe', 'brinquedo', 'utilidade',
    'achadinho', 'viral', 'pratico', 'facilita', 'oferta', 'promo', 'desconto'
]

def enviar_telegram(mensagem ):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CANAL_DESTINO, "text": mensagem, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, json=payload )
        print(f"Envio: {res.status_code}")
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
    print("🔎 Iniciando busca forçada de ofertas...")
    ultima_oferta = ""
    
    while True:
        try:
            res = requests.get(CANAL_FONTE, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
            
            if mensagens:
                # Vamos tentar as 3 últimas mensagens para garantir que pegamos algo
                for msg in mensagens[-3:]: 
                    texto_elem = msg.find('div', class_='tgme_widget_message_text')
                    if texto_elem:
                        texto_oferta = texto_elem.get_text().lower()
                        links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                        
                        if links and links[0] != ultima_oferta:
                            # Se tiver qualquer palavra do nicho OU for uma oferta forte
                            if any(p in texto_oferta for p in PALAVRAS_CHAVE):
                                link_com_comissao = converter_link(links[0])
                                msg_final = (
                                    "✨ *OFERTINHA DA ANGÉLICA!* ✨\n\n"
                                    f"{texto_elem.get_text()[:200]}...\n\n"
                                    f"🔗 *COMPRE AQUI:* {link_com_comissao}\n\n"
                                    "⚠️ *Aproveite! Oferta por tempo limitado.*"
                                )
                                enviar_telegram(msg_final)
                                ultima_oferta = links[0]
                                print(f"✅ Oferta enviada: {links[0]}")
                                break # Envia uma e espera o próximo ciclo
        except Exception as e:
            print(f"Erro: {e}")
            
        # Verifica a cada 5 minutos para ser mais rápido no teste!
        time.sleep(300) 

if __name__ == "__main__":
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    enviar_telegram("🤖 *TESTE DE FORÇA BRUTA:* Verificando ofertas agora mesmo!")
    buscar_ofertas()
