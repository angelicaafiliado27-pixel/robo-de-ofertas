import requests
import time
import threading
import http.server
import socketserver
from bs4 import BeautifulSoup

# --- CONFIGURAÇÕES DO SEU ROBÔ ---
TOKEN_TELEGRAM = "8714375855:AAHULALUU7p9hcp1YUSBAl_bDn5vPbzvZdM"
CANAL_DESTINO = "@ofertasmaepratica" 
CANAL_FONTE = "https://t.me/s/jgtechofertas" 

TAGS = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

# --- SUPER LISTA DE FILTROS: MÃE PRÁTICA ---
PALAVRAS_CHAVE = [
    # Cozinha & Organização
    'geladeira', 'pote hermético', 'escorredor', 'tempero', 'utensílio', 'cortador', 'dispenser',
    'air fryer', 'fritadeira', 'cafeteira', 'liquidificador', 'mixer', 'grill', 'sanduicheira',
    'panela elétrica', 'chaleira', 'forno', 'processador', 'espremedor',
    # Lavanderia & Limpeza
    'lavanderia', 'cesto', 'mop', 'rodo spray', 'removedor de pelos', 'limpeza', 'vassoura',
    'máquina de lavar', 'lava e seca', 'tanquinho', 'aspirador', 'robô aspirador', 'vaporizador',
    # Banheiro & Quarto
    'banheiro', 'shampoo', 'escova', 'saboneteira', 'prateleira', 'tapete', 'caixa organizadora',
    'guarda roupa', 'colmeia', 'cabide', 'bolsa', 'maquiagem', 'joia',
    # Beleza & Autocuidado
    'espelho led', 'massageador', 'necessaire', 'escova secadora', 'skincare', 'secador',
    'chapinha', 'modelador', 'alisadora', 'depilador',
    # Utilidades Virais & Dores (O que vende muito! )
    'viral', 'achadinho', 'indispensável', 'útil', 'utilidade doméstica', 'gadget',
    'facilita a rotina', 'inteligente', 'economiza tempo', 'organizada', 'bagunça',
    'prático para mães', 'apartamento', 'economiza espaço', 'ventilador', 'umidificador'
]

def enviar_telegram(mensagem):
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
    print("🚀 Robô Mãe Prática: Curadoria Ativada!")
    ultima_oferta = ""
    
    while True:
        try:
            res = requests.get(CANAL_FONTE, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
            
            if mensagens:
                msg = mensagens[-1]
                texto_elem = msg.find('div', class_='tgme_widget_message_text')
                
                if texto_elem:
                    texto_oferta = texto_elem.get_text().lower()
                    
                    # FILTRO INTELIGENTE DE CATEGORIAS
                    e_do_nicho = any(palavra in texto_oferta for palavra in PALAVRAS_CHAVE)
                    
                    if e_do_nicho:
                        links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                        if links and links[0] != ultima_oferta:
                            link_com_comissao = converter_link(links[0])
                            
                            msg_final = (
                                "✨ *ACHADINHO MÃE PRÁTICA!* ✨\n\n"
                                f"{texto_elem.get_text()[:250]}...\n\n"
                                f"🔗 *COMPRE AQUI:* {link_com_comissao}\n\n"
                                "⚠️ *Aproveite! Oferta por tempo limitado.*"
                            )
                            
                            enviar_telegram(msg_final)
                            ultima_oferta = links[0]
                            print(f"✅ Oferta de Nicho enviada: {links[0]}")
                    else:
                        print("⏭️ Oferta ignorada (não faz parte das categorias selecionadas).")
                        
        except Exception as e:
            print(f"Erro: {e}")
            
        # Verifica a cada 10 minutos para não perder os virais!
        time.sleep(600) 

if __name__ == "__main__":
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    enviar_telegram("🤖 *Robô Mãe Prática 100% CONFIGURADO!* \n\nEstou pronto para garimpar os melhores achadinhos e utilidades para o seu grupo. 🏠✨🚀")
    buscar_ofertas()
