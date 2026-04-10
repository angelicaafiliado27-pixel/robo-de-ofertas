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

# Lista ampliada para não deixar o robô "mudo"
PALAVRAS_CHAVE = [
    'casa', 'cozinha', 'banheiro', 'quarto', 'lavanderia', 'limpeza', 'organizador',
    'pote', 'mop', 'aspirador', 'airfryer', 'fritadeira', 'cafeteira', 'panela',
    'geladeira', 'maquina', 'lavar', 'infantil', 'bebe', 'brinquedo', 'utilidade',
    'achadinho', 'viral', 'pratico', 'facilita', 'oferta', 'promo', 'desconto',
    'shampoo', 'fralda', 'lenço', 'cesto', 'varal', 'tábua', 'celular', 'smartphone',
    'iphone', 'samsung', 'xiaomi', 'notebook', 'tablet', 'fone', 'smartwatch', 
    'televisão', 'alexa', 'perfume', 'maquiagem', 'skincare', 'beleza', 'shopee', 'amazon'
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
    print("🚀 Robô Mãe Prática: Modo Turbo Ativado!")
    # Limita a memória para as últimas 20 ofertas para permitir repostagens de boas promos
    ofertas_enviadas = [] 
    
    while True:
        for fonte in FONTES:
            try:
                res = requests.get(fonte, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(res.text, 'html.parser')
                mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
                
                if mensagens:
                    # Analisa as 5 últimas mensagens de cada fonte
                    for msg in mensagens[-5:]:
                        texto_elem = msg.find('div', class_='tgme_widget_message_text')
                        if texto_elem:
                            texto_original = texto_elem.get_text()
                            texto_oferta = texto_original.lower()
                            links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                            
                            if links and links[0] not in ofertas_enviadas:
                                # Se tiver palavra do nicho OU for de loja que você ama
                                if any(p in texto_oferta for p in PALAVRAS_CHAVE):
                                    link_com_comissao = converter_link(links[0])
                                    
                                    # Formatação bonita com espaços
                                    texto_formatado = texto_original.replace("A partir de:", "\n\nA partir de:")
                                    if "\n" not in texto_formatado[:50]:
                                        texto_formatado = texto_formatado.replace("R$", "\n\nR$", 1)

                                    msg_final = (
                                        f"😱😱 {texto_formatado[:350]}\n\n"
                                        f"🔗 *COMPRE AQUI:* {link_com_comissao}\n\n"
                                        "⚠️ *Aproveite! Oferta por tempo limitado.*"
                                    )
                                    
                                    enviar_telegram(msg_final)
                                    ofertas_enviadas.append(links[0])
                                    if len(ofertas_enviadas) > 20: ofertas_enviadas.pop(0)
                                    print(f"✅ Oferta enviada: {links[0]}")
            except Exception as e:
                print(f"Erro: {e}")
            time.sleep(5)
        
        # Verifica a cada 5 minutos (300 segundos)
        time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    enviar_telegram("🤖 *Robô Mãe Prática TURBINADO!* \n\nVerificando ofertas a cada 5 minutos com sensibilidade máxima. 🚀✨")
    buscar_ofertas()
