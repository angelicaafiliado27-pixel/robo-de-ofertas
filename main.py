import requests
import time
import threading
import http.server
import socketserver
from bs4 import BeautifulSoup

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = "8714375855:AAHULALUU7p9hcp1YUSBAl_bDn5vPbzvZdM"
CANAL_DESTINO = "@ofertasmaepratica" 

FONTES = [
    "https://t.me/s/jgtechofertas",
    "https://t.me/s/achadinhos_da_shopee_oficial"
]

TAGS = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

PALAVRAS_CHAVE = [
    'organizador', 'pote', 'mop', 'aspirador', 'airfryer', 'fritadeira', 'cafeteira', 
    'panela', 'geladeira', 'maquina', 'lavar', 'infantil', 'bebe', 'brinquedo', 
    'utilidade', 'achadinho', 'viral', 'pratico', 'facilita', 'cozinha', 'lavanderia',
    'banheiro', 'quarto', 'limpeza', 'shampoo', 'fralda', 'lenço', 'cesto', 'varal',
    'celular', 'smartphone', 'iphone', 'samsung', 'xiaomi', 'notebook', 'tablet',
    'fone', 'smartwatch', 'televisão', 'alexa', 'perfume', 'maquiagem', 'skincare'
]

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
    elif 'magazineluiza.com.br' in link or 'magalu' in link:
        return f"https://www.magazinevoce.com.br/{TAGS['magalu']}/"
    return link_original

def buscar_ofertas( ):
    print("🚀 Robô Mãe Prática: Ajuste de Visual Ativado!")
    ofertas_enviadas = set()
    
    while True:
        for fonte in FONTES:
            try:
                res = requests.get(fonte, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(res.text, 'html.parser')
                mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
                
                if mensagens:
                    for msg in mensagens[-3:]:
                        texto_elem = msg.find('div', class_='tgme_widget_message_text')
                        if texto_elem:
                            texto_original = texto_elem.get_text()
                            texto_oferta = texto_original.lower()
                            links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                            
                            if links and links[0] not in ofertas_enviadas:
                                if any(p in texto_oferta for p in PALAVRAS_CHAVE):
                                    link_com_comissao = converter_link(links[0])
                                    
                                    # AJUSTE DE ESPAÇAMENTO E VISUAL
                                    # Tenta separar o título do preço se encontrar "A partir de" ou "R$"
                                    texto_formatado = texto_original.replace("A partir de:", "\n\nA partir de:")
                                    if "\n" not in texto_formatado[:50]: # Se não tiver quebra de linha no começo
                                        texto_formatado = texto_formatado.replace("R$", "\n\nR$", 1)

                                    msg_final = (
                                        f"😱😱 {texto_formatado[:300]}\n\n"
                                        f"🔗 *COMPRE AQUI:* {link_com_comissao}\n\n"
                                        "⚠️ *Aproveite! Oferta por tempo limitado.*"
                                    )
                                    
                                    enviar_telegram(msg_final)
                                    ofertas_enviadas.add(links[0])
            except Exception as e:
                print(f"Erro: {e}")
            time.sleep(5)
        time.sleep(600)

if __name__ == "__main__":
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    enviar_telegram("🤖 *Robô Mãe Prática ATUALIZADO!* \n\nVisual das mensagens ajustado para ficar mais limpo e organizado. ✨🏠")
    buscar_ofertas()
